from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate  # ✅ updated import
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"  # ✅ fixed typo (decsription -> description)
)

# OpenAI route
add_routes(
    app,
    ChatOpenAI(),
    path="/openai"
)

model = ChatOpenAI(model="gpt-4o")

# Ollama llama2
llm = Ollama(model="llama2")

prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} for a 5-year-old child with 100 words")

add_routes(
    app,
    prompt1 | model,
    path="/essay"
)

add_routes(
    app,
    prompt2 | llm,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)
