
import streamlit as st
import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema import Document


# Load environment variables
load_dotenv()
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
# DATA_FILE = os.path.join(os.getcwd(), "eds_data.txt")
# DATA_FILE = os.path.join(os.getcwd(), "deds_data.txt")

# Initialize session state if not already present
if 'store' not in st.session_state:
    st.session_state.store = {}

# Helper function to read text files
def read_text_files(directory, allowed_extensions={".css", ".js", ".html"}):
    all_text = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(allowed_extensions)):
                file_path = os.path.join(root, file)
                print(file_path,"hhhhhhhhh")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        print(content,"h1hhhhhhhh")
                        all_text.append(Document(page_content=content))
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")  # Handle encoding issues
    return all_text  # Return a list of Document objects

# Load and preprocess text data
def load_and_preprocess_data():
    loaded_data = read_text_files("data")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(loaded_data)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Define the path for the FAISS index
faiss_index_path = "faiss_index"

# Check if the FAISS index already exists
if os.path.exists(faiss_index_path):
    # If it exists, load the FAISS index
    print("tes","tcs12")
    db = FAISS.load_local(faiss_index_path, embeddings,allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
else:
    # Otherwise, generate embeddings, save the FAISS index, and set up retriever
    documents = load_and_preprocess_data()
    print(documents,"tcs123")
    db = FAISS.from_documents(documents=documents, embedding=embeddings)
    db.save_local(faiss_index_path)
    retriever = db.as_retriever()

# Function to get session history
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

context_prompt_system = (
    "Given a chat history and the latest user question, "
    "which might reference context in the chat history, "
    "formulate a standalone question that can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed, otherwise return it as is."
)

# Define chat history context with enhanced system prompts
history_context = ChatPromptTemplate([
    ("system", context_prompt_system),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

# Initialize LLM (Language Model)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

# Create history aware retriever
chat_history_retriever = create_history_aware_retriever(llm, retriever, history_context)

# Main QA retriever
system_prompt = (
    "You are an assistant designed to convert code-related queries into UI code using the company's proprietary UI library, 'EDS'. "
    "When a user provides code or asks for a UI component, you must convert it into the corresponding 'EDS' code, "
    "which includes the proper classes and CSS styles from the 'EDS' library. Do not return generic or common CSS classes or styles, "
    "only those defined by 'EDS'. Ensure the response contains the complete HTML, with embedded CSS inside the `<head>`, "
    "and relevant 'EDS' components and styles.\n\n"
    "- Always use 'EDS' classes and styles (e.g., .form-check-inline, .btn-check) when converting code. Do not provide generic or unrelated styles.\n"
    "- If the user requests a UI component, convert it into 'EDS' code. Ensure that the appropriate 'EDS' components and styles are applied.\n"
    "- If the requested component or style does not exist in 'EDS', respond with 'I don’t know.' Do not create generic CSS for missing components.\n"
    "- Provide complete, working HTML code with 'EDS' classes and embedded CSS within the `<head>` section.\n"
    "- Always ensure that the response adheres to the structure and style defined by the 'EDS' library.\n"
    "- If the user asks for something generic (e.g., 'HTML form', 'button', 'checkbox'), provide an 'EDS' style version using proper components and styles, "
    "including inline CSS in the `<head>` section if necessary.\n\n"
    "Example:\n"
    "User provides a checkbox form with generic classes:\n"
    "Return HTML using 'EDS' classes such as `.form-check-inline` and `.btn-check` and ensure the CSS inside the `<head>` section corresponds to 'EDS' styles.\n\n"
    "If you're unsure, respond with 'I don’t know'. Keep answers concise, using only 'EDS' components and styles relevant to the query.\n\n{context}"
)



qa_context = ChatPromptTemplate([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

qa_retriever = create_stuff_documents_chain(llm, qa_context)

# Combine the retrievers
merge_retriever = create_retrieval_chain(chat_history_retriever, qa_retriever)

# Create runnable retriever with message history
rag_retriever = RunnableWithMessageHistory(
    merge_retriever,
    get_session_history=get_session_history,
    input_messages_key="input",
    output_messages_key="answer",
    history_messages_key="chat_history"
)

# Streamlit UI setup
st.title("EDS CODE TRANSLATOR")

# Input text box for user query
input_text = st.text_input("Enter your query")

if input_text:
    session_history = get_session_history(session_id="test123")
    
    # Get response and related documents
    response = rag_retriever.invoke({"input": input_text}, config={"configurable": {"session_id": "test123"}})
    
    # Add user message to chat history
    session_history.add_user_message(input_text)
    
    # Add AI response to chat history
    session_history.add_ai_message(response["answer"])
    
    # Display the answer
    st.subheader("Answer:")
    st.write(response["answer"])
    
    # Display related documents
    st.subheader("Related Documents:")
    source_docs = response.get("context", [])
    if source_docs:
        with st.expander("View Source Documents"):
            for i, doc in enumerate(source_docs):
                st.write(f"#### Document {i + 1}:")
                st.write(doc.page_content)

# Display chat history in a formatted way
st.subheader("Chat History:")
chat_container = st.container()

# Display each message in the chat history
for message in get_session_history("test123").messages:
    if message.type == "human":
        with chat_container:
            st.markdown(
                f"""
                <div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-bottom: 10px; text-align: left;">
                    <strong>You:</strong> {message.content}
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif message.type == "ai":
        with chat_container:
            st.markdown(
                f"""
                <div style="background-color: #e2f0ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; text-align: left;">
                    <strong>AI:</strong> {message.content}
                </div>
                """,
                unsafe_allow_html=True,
            )
