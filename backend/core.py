import os 
from typing import Any
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone as pinecone_store
import pinecone

pinecone.init(api_key=os.environ["PINECODE_API_KEY"], environment="gcp-starter")
INDEX_NAME = "pytorch-doc-index"

def run_llm(query:str) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = pinecone_store.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(model="gpt-4",verbose=True, temperature=0)
    qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)
    return qa({"query": query})

if __name__ == "__main__":
    print(run_llm("How do I use the torch.nn module?"))

