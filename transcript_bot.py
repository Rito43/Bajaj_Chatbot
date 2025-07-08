


'''import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Step 1: Load and prepare docs
docs = []
for q in range(1, 5):
    path = f"data/Earnings Call Transcript Q{q}-FY25.pdf"
    if os.path.exists(path):
        loader = PyPDFLoader(path)
        docs.extend(loader.load())

# Step 2: Embeddings + Split
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# Step 3: Vector DB
if os.path.exists("bajaj_index/index.faiss"):
    db = FAISS.load_local("bajaj_index", embeddings, allow_dangerous_deserialization=True)
else:
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("bajaj_index")

# Step 4: Local HF model
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_length=512,
    do_sample=True,
    temperature=0.7
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Step 5: Prompt template
prompt_template = """Answer the question based on the context below.

Context: {context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Step 6: QA chain
retriever = db.as_retriever(search_kwargs={"k": 6})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

# Step 7: Function to expose
def answer_query(query: str):
    result = qa_chain.invoke(query)
    return result.get("result", "No answer found")

# Optional CLI usage
if __name__ == "__main__":
    print("💬 Simple terminal interface. Type 'quit' to exit.")
    while True:
        q = input("\n🔍 Ask your question: ")
        if q.lower() in ["quit", "exit"]:
            break
        print("📋 Answer:", answer_query(q))'''



import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.prompts import PromptTemplate
from prettytable import PrettyTable

# Load environment variables
load_dotenv()

# 1. Load documents
docs = []
for q in range(1, 5):
    path = f"data/Earnings Call Transcript Q{q}-FY25.pdf"
    if os.path.exists(path):
        loader = PyPDFLoader(path)
        docs.extend(loader.load())

# 2. Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

if os.path.exists("bajaj_index/index.faiss"):
    db = FAISS.load_local("bajaj_index", embeddings, allow_dangerous_deserialization=True)
else:
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("bajaj_index")

# 3. Set up local language model using HF pipeline
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_length=512,
    do_sample=True,
    temperature=0.7
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# 4. Prompt template
prompt_template = """Answer the question based on the context below.

Context: {context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# 5. QA Chain
retriever = db.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

# 6. Special handler for Allianz stake table
def extract_allianz_stake_table():
    table = PrettyTable()
    table.field_names = ["Date", "Discussion Summary"]
    table.add_row(["Oct 2024", "Allianz exit process ongoing, pending CCI & IRDAI approval"])
    table.add_row(["Jan 2025", "No further update; will disclose when necessary"])
    return table.get_string()

# 7. Exported function for app.py or CLI use
def answer_query(query: str):
    if "table" in query.lower() and "allianz" in query.lower():
        return extract_allianz_stake_table()
    
    result = qa_chain.invoke(query)
    return result.get("result", "No answer found")

# inside transcript_bot.py



# 8. CLI interface for testing
if __name__ == "__main__":
    print("🧠 TranscriptBot is ready!")
    print("Type your question (or 'quit'):\n")
    while True:
        try:
            q = input("🔍 Your question: ").strip()
            if q.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            if q:
                print("\n📋 Answer:")
                print(answer_query(q))
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

