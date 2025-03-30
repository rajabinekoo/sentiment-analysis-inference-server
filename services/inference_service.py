from typing import List

from libs.spark import spark_app
from dto.inference import InferenceDTO, InferenceResponse


def sentiment_analysis_inference(body: InferenceDTO) -> List[InferenceResponse]:
    data = spark_app.generate_inference_input_data(body.queries)
    predictions_py = spark_app.model.transform(data)
    prediction_list = [row.prediction for row in predictions_py.select("prediction").collect()]
    result = []
    for i in range(0, len(prediction_list)):
        result.append(InferenceResponse(body.queries[i], prediction_list[i]))
    return result
