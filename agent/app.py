import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

question = input("Ask a question: ")

messages = [
    ("system", SYSTEM_PROMPT),
    ("human", question)
]

response = llm.invoke(messages)

print(response.content)