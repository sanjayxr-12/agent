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