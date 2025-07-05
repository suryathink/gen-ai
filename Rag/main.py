from dotenv import load_dotenv

from pathlib import Path # using this module we get path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()


pdf_Path = Path(__file__).parent / "nodejs.pdf"

# Loading
loader = PyPDFLoader(file_path = pdf_Path)
docs = loader.load() # Read pdf file

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap= 400, #chunk_overlap -> we do it for context
)

split_docs = text_splitter.split_documents(documents=docs)


# Vector Embeddings
embedding_model = OpenAIEmbeddings(
   model="text-embedding-3-large",
)

# using embedding model create embeddings of split_docs and store in DB

vector_store = QdrantVectorStore.from_documents(
    documents = split_docs,
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding = embedding_model
)

print("Indexing of documents done...")

