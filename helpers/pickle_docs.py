import pickle
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import subprocess

def download_docs(docs_url: str, output_name: str):
    """
    recursively download docs using wget
    Uses command in the style of:
    !wget -r -A.html -P rtdocs https://langchain.readthedocs.io/en/latest/
    !wget -r -A.html -P {output_name} {docs_url}
    """
    # !wget -r -A.html -P {output_name} {docs_url}
    command = f"wget -r -A.html -P {output_name} {docs_url}"
    subprocess.run(command, shell=True)

def ingest_docs(docs_loc: str="rtdocs", docs_name: str='langchain'):
    """Get documents from web pages."""
    loader = ReadTheDocsLoader(docs_loc, features='html.parser')
    print(loader)
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    print(raw_documents)
    documents = text_splitter.split_documents(raw_documents)
    print(documents)
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(documents, embeddings)
    
    query = "Create a document loader"
    docs = vectorstore.similarity_search(query)
    
    print(docs[0].page_content)

    # Save vectorstore
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

ingest_docs()