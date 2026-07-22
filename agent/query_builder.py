from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

TRANSLATE_PROMPT = """You convert business questions into Cube.dev query JSON.
Only use measures/dimensions that exist in this schema:
{schema}

Return ONLY valid JSON in Cube's query format, e.g.:
{{"measures": ["Orders.totalRevenue"], "filters": [{{"member": "Orders.region", "operator": "equals", "values": ["Europe"]}}]}}

No explanation, no markdown fences — raw JSON only."""

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

def build_query(question: str, schema: dict) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", TRANSLATE_PROMPT),
        ("human", "{question}")
    ])
    chain = prompt | llm
    result = chain.invoke({"schema": json.dumps(schema), "question": question})
    text = result.content.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)