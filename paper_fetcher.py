from langchain_community.document_loaders import ArxivLoader
import ssl
ssl._create_default_https_context=ssl._create_unverified_context
import arxiv
from langchain_core.documents import Document
import streamlit as st

@st.cache_data(show_spinner=False)
def Paper_fetcher(query):
   try:
      client = arxiv.Client()
      search = arxiv.Search(
        query=query,
        max_results=5,
        sort_by=arxiv.SortCriterion.Relevance
        )
    
      docs = []
    # This fetches the metadata and summary text ONLY
      for result in client.results(search):
          doc = Document(
            page_content=result.summary, 
            metadata={
                "title": result.title,
                "author": ", ".join(a.name for a in result.authors),
                "published": result.published.strftime("%Y-%m-%d")
            }
        )
          docs.append(doc)
    
      return docs
   except Exception as e:
      print("arxiv error",e)
      return []
      
   

if __name__=="__main__":
   results=Paper_fetcher("EEG motor intent classification")
   for paper in results:
      print(paper.metadata["title"])



      
      
   
   
