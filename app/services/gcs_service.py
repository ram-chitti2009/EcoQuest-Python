# Google Custom Search logic
import os
import requests
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv('.env.local')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GCS_SEARCH_ENGINE_ID = os.getenv("GCS_SEARCH_ENGINE_ID")

def search_google(query: str, num_results: int = 5) -> List[Document]:
    print(f"[DEBUG] GOOGLE_API_KEY: {GOOGLE_API_KEY[:10] if GOOGLE_API_KEY else 'None'}...")
    print(f"[DEBUG] GCS_SEARCH_ENGINE_ID: {GCS_SEARCH_ENGINE_ID}")

    if not GOOGLE_API_KEY or not GCS_SEARCH_ENGINE_ID:
        print("[WARNING] Missing Google Custom Search credentials, returning empty results")
        return []
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GCS_SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results
    }
    try:
        response = requests.get(url, params=params)
        print(f"[DEBUG] Google Search response status: {response.status_code}")
        
        if response.status_code == 403:
            print(f"[ERROR] Google Search 403 error: {response.text}")
            return []  # Return empty results instead of crashing
            
        response.raise_for_status()
        items = response.json().get("items", [])
        docs = []
        for item in items:
            content = item.get("snippet", "")
            metadata = {"title": item.get("title", ""), "link": item.get("link", "")}
            docs.append(Document(page_content=content, metadata=metadata))
        return docs
    except Exception as e:
        print(f"[ERROR] Google Search failed: {e}")
        return []  # Return empty results instead of crashing
