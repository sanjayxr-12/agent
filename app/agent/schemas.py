from pydantic import BaseModel, Field

class SQLGeneratorOutput(BaseModel):
    sql_query: str = Field(
        ..., 
        description="The raw SQL query to execute. Do not wrap in markdown."
    )
    explanation: str = Field(
        ..., 
        description="A one-sentence explanation of what this query fetches."
    )

class SafetyAssessment(BaseModel):
    is_safe: bool = Field(..., description="True if the content is safe to process, False if it contains hate speech, violence, or malicious intent.")
    reason: str = Field(..., description="A brief explanation of why the content is considered safe or unsafe.")