import os
import warnings
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load API key from .env
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

directory_path = os.getenv("DIRECTORY_PATH", "./your-codebase")

# Step 1: Load and filter Node.js project files
print("Loading codebase (excluding node_modules, dist, etc.)...")
exclude_dirs = {'node_modules', 'dist', 'build', '.git', '__pycache__', 'coverage'}
included_extensions = {'.js', '.ts', '.json', '.md'}
base_path = Path(directory_path)

code_files = [
    f for f in base_path.rglob("*")
    if f.suffix in included_extensions and not any(part in exclude_dirs for part in f.parts)
]

# Load documents
documents = []
for file_path in code_files:
    try:
        loader = TextLoader(str(file_path), encoding='utf-8')
        documents.extend(loader.load())
        print(f"Loaded file: {file_path}")
    except Exception as e:
        print(f"Skipped {file_path}: {e}")

# Step 2: Split into manageable chunks
print("Splitting documents...")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)

if not docs:
    print("No valid project files were loaded. Please check your file filters or directory path.")
    exit(1)

# Step 3: Embed and index using FAISS
print("Generating embeddings...")
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding)
retriever = vectorstore.as_retriever(search_type="similarity", k=5)

# Step 4: Setup LLM QA chain
print("Initializing QA chain...")
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4", temperature=0),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Step 5: Start interactive Q&A
print("\nCodebase Navigator Ready. Ask a question about the Node.js project.\n")
while True:
    query = input(">> ")
    if query.lower() in ["exit", "quit"]:
        print("Exiting. Goodbye!")
        break
    result = qa_chain(query)
    print("\nAnswer:\n", result["result"])
    print("\nSources:")
    for doc in result["source_documents"]:
        print("-", doc.metadata.get("source", "Unknown"))
    print("\n---\n")
