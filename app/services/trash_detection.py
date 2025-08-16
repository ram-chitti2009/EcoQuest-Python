import os
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

from app.services.langchain_service import sustainability_chatbot_response


load_dotenv(dotenv_path=".env.local")

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=os.getenv("ROBOFLOW_API_KEY")
)

def identify_object(image_path: str):
    try:
        result = CLIENT.infer(image_path, model_id="trash-detection-ujrn0/1")
        print("[Roboflow identify_object result]:", result)
        return result
    except Exception as e:
        print(f"Error during object identification: {e}")
        return None



def trash_detection(image_path: str):
    try:
        result = CLIENT.infer(image_path, model_id="waste-segregation-d2vj9/5")
        print("[Roboflow trash_detection result]:", result)
        return result
    except Exception as e:
        print(f"Error during trash detection: {e}")
        return None


def classify_and_advise(image_path, user_id):
    detection_result = trash_detection(image_path)
    if detection_result is None:
        return "Error in trash detection."
    object_result = identify_object(image_path)
    if object_result is None:
        return "Error in object identification."
    from langchain.schema import Document

    context = f"Trash segregation result: {detection_result}, Object identification result: {object_result}"
    query = (
        "Based on the trash segregation and detection result above, "
        "what is the object, what type of waste is this and how should it be disposed of in an environmentally friendly way?" \
        "Elucidate on it, and tell the user how to dispose of it properly."
    )

    answer = sustainability_chatbot_response(user_id, query, [Document(page_content=context)])
    return answer

