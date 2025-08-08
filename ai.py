import openai
import os
from flask import Flask, render_template, request, jsonify
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Your existing document loading and vector store creation (from previous code)
def load_documents(data_folder):
    documents = []
    for file in os.listdir(data_folder):
        if file.endswith('.pdf'):
            loader = PyPDFLoader(os.path.join(data_folder, file))
            documents.extend(loader.load())
    return documents

def create_vector_store(documents):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

# Load data once when the app starts
data_folder = "path/to/your/documents"  # Replace with your folder path
docs = load_documents(data_folder)
vector_store = create_vector_store(docs)

# Enhanced chatbot response (using your trained version)
def trained_chatbot_response(user_input):
    llm = OpenAI()
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vector_store.as_retriever())
    return qa_chain.run(user_input)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = trained_chatbot_response(user_input)  # Or use chatbot_response for basic version
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
