# import os
# from typing import Optional, Any, Union
# from google import genai
# from google.genai import types 
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI  # <--- NEW IMPORT

# load_dotenv()

# API_KEY = os.getenv("GOOGLE_API_KEY")
# DEFAULT_MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")

# if not API_KEY:
#     print("Warning: GOOGLE_API_KEY not set.")
#     client = None
# else:
#     client = genai.Client(api_key=API_KEY)

# def get_chat_model(model_name: str = "gemini-2.0-flash"):
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise RuntimeError("GOOGLE_API_KEY not configured")
        
#     return ChatGoogleGenerativeAI(
#         model=model_name,
#         google_api_key=api_key,
#         temperature=0,
#         max_retries=5,    
#         request_timeout=30 
#     )

# async def generate_text(
#     prompt: str,
#     *,
#     model_name: Optional[str] = None,
#     system_instruction: Optional[str] = None,
#     response_schema: Optional[Any] = None,
# ) -> Union[str, Any]:
    
#     if not client:
#         raise RuntimeError("GOOGLE_API_KEY not configured")

#     mime_type = "application/json" if response_schema else None
    
#     config = types.GenerateContentConfig(
#         system_instruction=system_instruction,
#         temperature=0.7 if not response_schema else 0.0,
#         response_mime_type=mime_type,
#         response_schema=response_schema, 
#     )
#     try:
#         response = await client.aio.models.generate_content(
#             model=model_name or DEFAULT_MODEL,
#             contents=prompt,
#             config=config,
#         )
#         if response_schema:
#             return response.parsed
        
#         return response.text if response.text else ""

#     except Exception as e:
#         print(f"Gemini API Error: {e}")
#         return None if response_schema else ""


import os
from langchain_groq import ChatGroq  
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile" 

def get_chat_model(model_name: str = DEFAULT_MODEL):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not configured")
        
    return ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=0,
        max_retries=2,
        request_timeout=30 
    )

async def generate_text(prompt: str):
    model = get_chat_model()
    response = await model.ainvoke(prompt)
    return response.content