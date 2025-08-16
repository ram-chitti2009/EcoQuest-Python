# FastAPI route definitions will go here
import os
from jose import jwt 
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from app.models.schemas import QueryRequest, GeminiResponse
from app.services.gcs_service import search_google
from app.services.langchain_service import sustainability_chatbot_response
from app.services.trash_detection import classify_and_advise
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
def get_current_user(request: Request):
    auth = request.headers.get("authorization")
    print(f"[DEBUG] Auth header: {auth}")
    
    if not auth or not auth.startswith("Bearer "):
        print("[DEBUG] Missing or invalid auth header format")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth.split(" ")[1]
    print(f"[DEBUG] Extracted token: {token[:50]}...")

    if SUPABASE_JWT_SECRET is None:
        print("[DEBUG] JWT secret is None")
        raise HTTPException(status_code=500, detail="JWT secret not configured")

    try:
        print(f"[DEBUG] Using JWT secret: {SUPABASE_JWT_SECRET[:10]}...")
        # Skip audience validation by adding options
        payload = jwt.decode(
            token, 
            SUPABASE_JWT_SECRET, 
            algorithms=["HS256"],
            options={"verify_aud": False} #this will skip audience validation which will resolve our auth issues
        )
        print(f"[DEBUG] Decoded payload: {payload}")
        user_id = payload.get("sub")
        if not user_id:
            print("[DEBUG] No 'sub' claim in token")
            raise HTTPException(status_code=401, detail="Invalid token")
        print(f"[DEBUG] User ID extracted: {user_id}")
        return user_id
    except Exception as e:
        print(f"[DEBUG] JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token") from e
    




router = APIRouter()

@router.post("/ask", response_model=GeminiResponse)
async def ask_bot(request: QueryRequest, user_id: str = Depends(get_current_user)):
    print(f"[DEBUG] Request data: {request}")
    print(f"[DEBUG] Query: {request.query}")
    print(f"[DEBUG] User ID: {user_id}")
    
    search_results = search_google(request.query)
    print("[Google Custom Search results]:", search_results)
    
    answer = sustainability_chatbot_response(user_id, request.query, search_results)
    print(f"[DEBUG] Answer type: {type(answer)}")
    print(f"[DEBUG] Answer content: {answer}")
    
    response = GeminiResponse(answer=answer)
    print(f"[DEBUG] Response object: {response}")
    
    return response

@router.post("/classify-trash")
async def classify_trash(file:UploadFile = File(...), 
                         user_id: str = Depends(get_current_user)):
    """
    Endpoint to classify trash using an uploaded image.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    
    # Call the trash detection service
    answer = classify_and_advise(temp_path, user_id)
    
    # Clean up the temporary file
    os.remove(temp_path)

    return answer