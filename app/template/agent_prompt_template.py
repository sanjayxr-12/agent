from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

guardrails_template = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a content safety filter. Analyze the following user message. "
        "If it contains hate speech, violence, sexual content, or malicious intent, respond strictly with 'UNSAFE'. "
        "If it is a normal query (even if it's about database/SQL), respond with 'SAFE'."
    )),
    ("human", "{question}"),
])

agent_template = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a MySQL Expert. Use the provided tools.\n"
        "### DATABASE SCHEMA ###\n{schema}\n\n"
        "IMPORTANT RULES:\n"
        "1. NEVER guess column names. Check the schema.\n"
        "2. If a tool returns an error TWICE, STOP trying and tell the user you cannot find the answer.\n" 
        "3. Do not run the same failed query multiple times."
    )),
    MessagesPlaceholder(variable_name="messages") 
])