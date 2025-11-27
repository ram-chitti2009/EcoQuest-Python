# LangChain logic
from typing import List
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from langchain_google_genai import ChatGoogleGenerativeAI



user_memories = {}


def get_user_memory(user_id: str) -> List:
    """
    Retrieve or create a conversation memory for a user.
    Returns a list of messages for conversation history.
    """
    if user_id not in user_memories:
        user_memories[user_id] = []
    return user_memories[user_id]



def process_context(docs: List[Document]):
    """
    Summarize or filter documents for context.
    For now, just concatenate snippets. You can add summarization here.
    """
    return "\n\n".join([doc.page_content for doc in docs])



def sustainability_chatbot_response(
        user_id: str,
        query: str,
        context_docs: List[Document]
) -> str:
    """
    Generate a response from the sustainability chatbot using LangChain and Google Generative AI (Gemini).
    """
    import os
    # Retrieve or create user memory
    memory = get_user_memory(user_id)

    # Process context documents
    context = process_context(context_docs)

    # Build messages with history
    messages = [
        SystemMessage(content="You are a sustainability expert. Use the provided context to answer user questions accurately and concisely.")
    ]
    
    # Add conversation history
    messages.extend(memory)
    
    # Add current query with context
    messages.append(HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}"))

    # Use Gemini via Google Generative AI
    api_key = os.getenv("GEMINI_API_KEY")
    chat = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=1.0,
        max_retries=2,
        google_api_key=api_key,
    )
    
    response = chat.invoke(messages)

    # Save conversation context
    memory.append(HumanMessage(content=query))
    memory.append(AIMessage(content=str(response.content)))

    if response:
        if isinstance(response.content, str):
            return response.content
        else:
            return str(response.content)
    return "No response from Gemini API."