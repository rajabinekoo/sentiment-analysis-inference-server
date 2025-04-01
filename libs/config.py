class Configs:
    CoolColumn = "cool"
    FunnyColumn = "funny"
    UsefulColumn = "useful"
    PositiveLabel = 1.0
    NegativeLabel = 0.0
    NeutralLabel = 2.0
    PositiveWordsCount = "positive_word_counts"
    NegativeWordsCount = "negative_word_counts"
    NeutralWordsCount = "neutral_word_counts"
    ReviewTable = "reviews_bucketed"
    StatisticTable = "statistics"


statistic_valid_keys = [
    "positive", "negative", "neutral", "f1-score", "accuracy",
    # confusion matrix
    "cm-[0][0]", "cm-[0][1]", "cm-[0][2]",
    "cm-[1][0]", "cm-[1][1]", "cm-[1][2]",
    "cm-[2][0]", "cm-[2][1]", "cm-[2][2]",
]
