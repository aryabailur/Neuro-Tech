from vector_store import retrieve
from vector_store import store_papers
from paper_fetcher import Paper_fetcher
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage
from dotenv import load_dotenv
load_dotenv()
gemini_api=os.getenv("GOOGLE_API_KEY")


llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=gemini_api)
def synthesize(query,chat_history=None):
    list_papers=Paper_fetcher(query)
    vector_db=store_papers(papers=list_papers)
    search_results=retrieve(query,vector_db=vector_db)
    search_result_list=[]
    for paper in search_results:
        chunk_with_title=f"Paper:{paper.metadata['title']}\n\n{paper.page_content}"
        search_result_list.append(chunk_with_title)

    retrieved_context="\n\n".join(search_result_list)
    
    history_section = ""
    if chat_history:
        recent = chat_history[-3:]
        for exchange in recent:
            history_section += f"User asked: {exchange['query']}\nAgent answered: {exchange['response'][:500]}\n\n"
        history_section = f"Previous conversation:\n{history_section}"
    
    system_instruction = SystemMessage(content="""You are an expert neuroscience and BCI research analyst. 
    Your job is to synthesize information from multiple research papers and provide structured, 
    accurate summaries. Always cite which paper each finding comes from using the title. 
    If information is not present in the provided papers, say so explicitly — do not hallucinate.""")

    human_prompt = HumanMessage(content=f"""{history_section} Here are relevant research paper chunks:

    {retrieved_context}

Based on these papers, provide a structured analysis covering:
1. Key methods and approaches used
2. Main findings and results  
3. Limitations acknowledged by the authors
4. Open problems or future work mentioned
5. How these papers relate to each other

Always reference the paper title when making a specific claim.""")
    response=llm.invoke([system_instruction,human_prompt])
    content=response.content
    
    return content

