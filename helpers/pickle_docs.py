# import pickle
import os
from langchain.document_loaders import ReadTheDocsLoader, GitbookLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import subprocess

os.environ["OPENAI_API_KEY"] = "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"


def download_docs(docs_url: str, output_name: str):
    """
    recursively download docs using wget
    Uses command in the style of:
    !wget -r -A.html -P rtdocs https://langchain.readthedocs.io/en/latest/
    !wget -r -A.html -P {output_name} {docs_url}
    """
    # !wget -r -A.html -P {output_name} {docs_url}
    # command = f"wget -erobots=off -r -A.html -P {output_name} {docs_url}"
    command = f'wget --recursive --no-parent --random-wait --limit-rate=200k --wait=1 -e robots=off --no-check-certificate -U "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" -P {output_name} {docs_url}'
    subprocess.run(command, shell=True)


def ingest_docs(docs_loc: str = "rtdocs", docs_name: str = "langchain", gitbook=False):
    """Get documents from web pages."""
    if gitbook:
        loader = GitbookLoader(docs_loc, load_all_paths=True)
    else:
        loader = ReadTheDocsLoader(docs_loc, features="html.parser")
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    print("raw docs")
    print(raw_documents)
    documents = text_splitter.split_documents(raw_documents)
    print("docs")
    print(documents)
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(documents, embeddings)

    query = "Create a document loader"
    docs = vectorstore.similarity_search(query)

    print(docs[0].page_content)

    # Save vectorstore as txt file
    vectorstore.save_local(f"{docs_name}_faiss_index")


# download_docs('https://docs.airstack.xyz', 'airstack')
# download_docs('https://python.langchain.com/', 'langchain')
ingest_docs(
    docs_loc="https://docs.airstack.xyz", docs_name="airstack_baby", gitbook=True
)

""" embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local('airstack_faiss_index', embeddings)
print(vectorstore) """
