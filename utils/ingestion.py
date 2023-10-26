import os
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as pinecone_store
import pinecone

####

pinecone.init(api_key=os.environ["PINECODE_API_KEY"], environment="gcp-starter")

def ingest_docs(path)->None:
    text_loader_kwargs={'autodetect_encoding': True}
    loader = DirectoryLoader(path, loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    raw_docs = loader.load()
    print(f"Loaded {len(raw_docs)} documents")  

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
    docs = text_splitter.split_documents(documents=raw_docs)
    print(f"Split into {len(docs)} documents")

    for doc in docs:
        old_path1 = doc.metadata['source']
        new_path1 = old_path1.replace(path, "https:/")
        doc.metadata.update({'source': new_path1})
        old_path2 = doc.metadata['source']
        new_path2 = old_path2.replace(".txt", ".html")
        doc.metadata.update({'source': new_path2})

    embeddings = OpenAIEmbeddings()
    pinecone_store.from_documents(documents=docs, embedding=embeddings, index_name="pytorch-doc-index")
    print("Indexed documents")


if __name__ == "__main__":
    ingest_docs("../cleaned/cleaned-pytorch-docs")