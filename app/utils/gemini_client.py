import os
from typing import Optional, Any, Union, Type
from google import genai
from google.genai import types  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

DEFAULT_MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash") 

if not API_KEY:
    print("Warning: GOOGLE_API_KEY not set.")
    client = None
else:
    client = genai.Client(api_key=API_KEY)

async def generate_text(
    prompt: str,
    *,
    model_name: Optional[str] = None,
    system_instruction: Optional[str] = None,
    response_schema: Optional[Any] = None,
) -> Union[str, Any]:
    
    if not client:
        raise RuntimeError("GOOGLE_API_KEY not configured")

    mime_type = "application/json" if response_schema else None
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7 if not response_schema else 0.0,
        response_mime_type=mime_type,
        response_schema=response_schema, 
    )
    try:
        response = await client.aio.models.generate_content(
            model=model_name or DEFAULT_MODEL,
            contents=prompt,
            config=config,
        )
        if response_schema:
            return response.parsed
        
        return response.text if response.text else ""

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None if response_schema else ""