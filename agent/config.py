from instructor import from_openai
# import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from os import getenv

from agent.schemas import ClientBase

######################################################################
#                            LLM Clients                             #
######################################################################

BASE_DIR = Path(__file__).resolve().parent

DOTENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=DOTENV_PATH)

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
GEMINI_API_KEY = getenv("GOOGLE_API_KEY")

GPT35TURBO = "gpt-3.5-turbo"
GPT4oMINI = "gpt-4o-mini"
GEMINI = "models/gemini-1.5-flash-latest"

OPENAI_CLIENT = from_openai(OpenAI(api_key=OPENAI_API_KEY))
# GEMINI_CLIENT = from_gemini(
#     client=genai.GenerativeModel(
#         model_name=GEMINI,
#     )
# )

CLIENTS = [
    # ClientBase(client=GEMINI_CLIENT, model=GEMINI),
    ClientBase(client=OPENAI_CLIENT, model=GPT35TURBO),
    ClientBase(client=OPENAI_CLIENT, model=GPT4oMINI),
]
