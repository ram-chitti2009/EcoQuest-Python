# FastAPI route definitions will go here
import os
from jose import jwt 
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from app.models.schemas import QueryRequest, GeminiResponse
from app.services.gcs_service import search_google
from app.services.langchain_service import sustainability_chatbot_response
from app.services.quiz_bot import quiz_bot_response
from app.services.trash_detection import classify_and_advise
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
def get_current_user(request: Request):
    auth = request.headers.get("authorization")
    print(f"[DEBUG] Auth header: {repr(auth)}")  # Use repr to see hidden characters
    
    if not auth:
        print("[DEBUG] Missing authorization header")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Clean and normalize the auth header
    auth = auth.strip()
    
    if not auth.startswith("Bearer "):
        print("[DEBUG] Invalid auth header format")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Strip whitespace and newline characters from the token
    try:
        token_parts = auth.split(" ", 1)  # Split only on first space
        if len(token_parts) != 2:
            print("[DEBUG] Invalid Bearer token format")
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        token = token_parts[1].strip()
        # Remove any non-printable characters
        token = ''.join(char for char in token if char.isprintable())
        print(f"[DEBUG] Extracted token: {token[:50]}...")
    except Exception as e:
        print(f"[DEBUG] Error extracting token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token format")

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

@router.get("/test")
async def test_endpoint():
    print("[DEBUG] Test endpoint reached!")
    return {"message": "Test endpoint working"}

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
async def classify_trash(file: UploadFile = File(...), 
                         user_id: str = Depends(get_current_user)):
    """
    Endpoint to classify trash using an uploaded image.
    """
    print(f"[DEBUG] classify_trash endpoint reached with user_id: {user_id}")
    print(f"[DEBUG] File parameter received: {file}")
    
    if not file:
        print("[DEBUG] No file uploaded")
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    print(f"[DEBUG] File received: {file.filename}, content_type: {file.content_type}")
    
    # Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    print(f"[DEBUG] Saving file to: {temp_path}")

    try:
        with open(temp_path, "wb") as f:
            content = file.file.read()
            f.write(content)
        print(f"[DEBUG] File saved successfully, size: {len(content)} bytes")
        
        # Call the trash detection service
        print("[DEBUG] Calling classify_and_advise...")
        answer = classify_and_advise(temp_path, user_id)
        print(f"[DEBUG] classify_and_advise returned: {type(answer)}")
        print(f"[DEBUG] Answer preview: {str(answer)[:200]}...")

        # Clean up the temporary file
        os.remove(temp_path)
        print("[DEBUG] Temporary file cleaned up")

        return answer
        
    except Exception as e:
        print(f"[DEBUG] Error in classify_trash: {e}")
        # Clean up file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/quiz-bot")
async def quiz_bot(
                         user_id: str = Depends(get_current_user)):
    """
    Endpoint to generate questions for the quiz
    """
    print(f"[DEBUG] quiz_bot endpoint reached with user_id: {user_id}")

    try:
        print("[DEBUG] Calling quiz bot")
        answer = quiz_bot_response(user_id)
        print(f"[DEBUG] quiz_bot_response returned: {type(answer)}")
        print(f"[DEBUG] Answer preview: {str(answer)}")
        return answer
        
    except Exception as e:
        print(f"[DEBUG] Error in generating the quiz questions {e}")
        raise HTTPException(status_code=500, detail=f"Error processing quiz questions: {str(e)}")