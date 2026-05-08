from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
import os

persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")


def store_papers(papers):

    text_split=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    list_papers=[]
    for paper in papers:
        paper_content=Document(
            page_content=paper.page_content,
            metadata={"author":paper.metadata["author"],"title":paper.metadata["title"],"published":paper.metadata["published"]}
        )
        list_papers.append(paper_content)

    split_docs=text_split.split_documents(list_papers)

   

   

    if persist_dir == "none":
        # In-memory only — for Streamlit Cloud
        vector_db = Chroma.from_documents(
            documents=split_docs,
            embedding=model
        )
    else:
        # Persistent — for local development
        vector_db = Chroma.from_documents(
            documents=split_docs,
            embedding=model,
            persist_directory=persist_dir
        )

    return vector_db

def retrieve(query,vector_db):
    search_results=vector_db.max_marginal_relevance_search(query=query, k=3, fetch_k=10)

    return search_results
