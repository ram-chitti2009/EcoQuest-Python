# LangChain logic
from typing import List
import langchain
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI



user_memories = {}


def get_user_memory(user_id:str) -> ConversationBufferMemory:
    """
    Retrieve or create a conversation memory for a user.
    """
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(return_messages=True)
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

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a sustainability expert. Use the provided context to answer user questions accurately and concisely."),
        ("human", "Context:\n{context}\n\nQuestion: {query}")
    ])

    formatted_prompt = prompt.format_messages(context=context, query=query)

    # Use Gemini via Google Generative AI
    api_key = os.getenv("GEMINI_API_KEY")
    chat = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=1.0,
        max_retries=2,
        google_api_key=api_key,
    )
    response = chat.invoke(formatted_prompt)

    # Save conversation context
    memory.save_context({"input": query}, {"output": str(response.content)})

    if response:
        if isinstance(response.content, str):
            return response.content
        else:
            return str(response.content)
    return "No response from Gemini API."