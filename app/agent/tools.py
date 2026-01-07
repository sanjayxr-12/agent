from langchain_core.tools import tool
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import text
from app.core.mysql_database import get_db_session

class SQLInput(BaseModel):
    query: str = Field(description="The SQL query to execute. Must be a SELECT statement.")
    @field_validator('query')
    def check_read_only(cls, v: str) -> str:
        command = v.strip().split()[0].upper()
        if command != "SELECT":
            raise ValueError("Security Alert: Only SELECT statements are allowed.")
        return v

@tool("list_tables")
async def list_tables() -> str:
    """ 
    Fetches the database schema (table names and columns) so the AI knows what tables exist. 
    """  
    schema_info = []
    async for session in get_db_session():
        result = await session.execute(text("SHOW TABLES;"))
        tables = result.scalars().all()
        
        for table in tables:
            columns_result = await session.execute(text(f"DESCRIBE {table};"))
            columns = columns_result.fetchall()
            col_names = [f"{col[0]} ({col[1]})" for col in columns]
            schema_info.append(f"Table: {table}\nColumns: {', '.join(col_names)}")
            
    return "\n\n".join(schema_info)


@tool("execute_sql", args_schema=SQLInput)
async def execute_sql(query: str) -> str:
    """
    Executes a read-only SQL query against the MySQL database.
    Returns the rows as a string or an error message.
    """ 
    try:
        async for session in get_db_session():
            result = await session.execute(text(query))
            keys = result.keys()
            rows = [dict(zip(keys, row)) for row in result.fetchall()]
            
            if not rows:
                return "No data found."
            return str(rows)

    except Exception as e:
        return f"Database Error: {str(e)}"