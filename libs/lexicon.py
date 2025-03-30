from pyspark.sql import DataFrame
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import col, first
from pyspark.sql.connect.session import SparkSession
from pyspark.sql.functions import lower, regexp_replace, split, explode, udf

from libs.config import Configs


class Lexicon:
    def __init__(self, file_path: str):
        self.polarities = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        word = parts[0]
                        try:
                            compound_polarity = float(parts[1])
                            self.polarities[word] = compound_polarity
                        except ValueError:
                            print(f"Warning: Could not convert polarity to float for word '{word}': '{parts[1]}'")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_sentiment_words_count_feature(self, spark: SparkSession, df: DataFrame) -> DataFrame:
        vader_broadcast = spark.sparkContext.broadcast(self.polarities)

        def get_sentiment(word):
            if word not in vader_broadcast.value:
                return -0.1
            value = vader_broadcast.value.get(word)
            if value > 0.1:
                return 1.0
            if value < -0.1:
                return 0.0
            return 2.0

        sentiment_udf = udf(get_sentiment, DoubleType())

        words_df = df.select("id", split(regexp_replace(lower(col("body")), "[^a-zA-Z\\s]", ""), "\\s+").alias("words")) \
            .withColumn("word", explode(col("words"))) \
            .filter(col("word") != "")

        sentiment_df = words_df.withColumn("sentiment_value", sentiment_udf(col("word"))) \
            .filter(col("sentiment_value") != -0.1)

        sentiment_counts_df = sentiment_df.groupBy("id", "sentiment_value").count() \
            .groupBy("id") \
            .pivot("sentiment_value", [1.0, 0.0, 2.0]) \
            .agg(first("count")) \
            .withColumnRenamed("1.0", Configs.PositiveWordsCount) \
            .withColumnRenamed("0.0", Configs.NegativeWordsCount) \
            .withColumnRenamed("2.0", Configs.NeutralWordsCount) \
            .fillna(0)

        return df.join(sentiment_counts_df, "id", "left").fillna(0).drop("id")


vader_lexicon = Lexicon("resources/vader_lexicon.txt")
