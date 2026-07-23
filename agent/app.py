import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

question = input("Ask a question: ")

messages = [
    ("system", SYSTEM_PROMPT),
    ("human", question)
]

response = llm.invoke(messages)

print(response.content)