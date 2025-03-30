import os

from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import monotonically_increasing_id

from libs.lexicon import vader_lexicon


class SparkApp:
    def __init__(self):
        self.spark = None
        self.model = None

    def init(self):
        self.spark = SparkSession.builder.appName("ModelInferenceApp").master("local[*]").getOrCreate()

        model_path = f"file://{os.getenv('S3_LOCAL_MODEL_DIR')}"

        try:
            self.model = PipelineModel.load(model_path)
            print(f"Model loaded")
        except Exception as e:
            print(f"Error loading model: {e}")

    def generate_inference_input_data(self, data: list[str]) -> DataFrame:
        input_data = self.spark.createDataFrame([tuple([d]) for d in data]) \
            .toDF("body") \
            .withColumn("id", monotonically_increasing_id())
        return vader_lexicon.extract_sentiment_words_count_feature(self.spark, input_data)


spark_app = SparkApp()
