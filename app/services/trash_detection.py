import os
import json
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
    from langchain_core.documents import Document

    context = f"Trash segregation result: {detection_result}, Object identification result: {object_result}"
    query = (
        """Based on the trash segregation and detection result above, formulate a response in the format of like this. just include the json data in the response dont include anything else
         const mockAnalysisData = {
    litterType: "Plastic Bottle",
    confidence: 94,
    quantity: "1 item",
    recyclable: true,
    hazardLevel: "Low",
    recommendations: [
      "Remove the plastic bottle and place it in a recycling bin",
      "Check for recycling symbol (usually #1 PET) on the bottom",
      "Rinse the bottle if it contained sugary drinks before recycling",
      "Consider reporting this location as a frequent littering spot",
    ],
    environmentalImpact: {
      decompositionTime: "450 years",
      carbonFootprint: "82g CO2 equivalent",
      wildlifeRisk: "Medium - can harm marine life if reaches waterways",
    },
  }
        """
        
    )

    answer = sustainability_chatbot_response(user_id, query, [Document(page_content=context)])
    
    # Clean up the response - remove markdown formatting and "json" text
    if isinstance(answer, str):
        # Remove ```json and ``` markers
        cleaned_answer = answer.replace('```json', '').replace('```', '').strip()
        
        # If it starts with "json", remove that too
        if cleaned_answer.lower().startswith('json'):
            cleaned_answer = cleaned_answer[4:].strip()
        
        # Try to parse and return as JSON object
        try:
            return json.loads(cleaned_answer)
        except json.JSONDecodeError:
            print(f"[DEBUG] Failed to parse JSON, returning cleaned string: {cleaned_answer[:100]}...")
            return {"error": "Invalid JSON response", "raw_response": cleaned_answer}
    
    return answer

