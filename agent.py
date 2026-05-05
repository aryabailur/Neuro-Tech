from dotenv import load_dotenv
import os
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
llm= ChatGoogleGenerativeAI(model='gemini-2.5-flash')
response=llm.invoke("what is motor imagery in neurotechnology")
print(response.content)
