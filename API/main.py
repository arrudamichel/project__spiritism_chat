from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
from langchain_core.load import loads

#from langchain.llms import OpenAI

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain_community.llms import Ollama
#from langchain.embeddings.huggingface import HuggingFaceEmbeddings
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

llm = Ollama(model="llama3.1")



# import os
# mypath = '../data'

# epub_files = [file for file in os.listdir(mypath) if file.endswith('.epub')]
# epub_files

# data = []
# for file_name in epub_files:
#     print(file_name)
#     loader = UnstructuredEPubLoader("../data/" + file_name)
#     data.append(loader.load())

# list_concat = [item for sublist in data for item in sublist]

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(list_concat)

embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-l6-v2",     # Provide the pre-trained model's path
)

# vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)


# Set the directory where the data was persisted
persist_directory = "../vectodb"

# Load the existing Chroma DB from the persistence directory
vectorstore = Chroma(
    collection_name="spiritism_db",
    persist_directory=persist_directory,
    embedding_function=embedding_function
)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()

### Contextualize question ###
contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


### Answer question ###
qa_system_prompt = """You are an assistant for question-answering tasks. \
You must answer just using the given context. \
Use the following pieces of retrieved context to answer the question. \
Always answer in Portuguese. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# Define o formato de entrada dos dados usando Pydantic
class ModelInput(BaseModel):
    prompt: str
    session: str

# Rota para inferência do modelo
@app.post("/predict/")
async def predict(input_data: ModelInput):
    prompt = input_data.prompt
    session = input_data.session
    
    # Faz a previsão usando o modelo LLM
    response = conversational_rag_chain.invoke(
                        {"input": prompt},
                        config={"configurable": {"session_id": session}},
                    )["answer"]

    return {"response": response}

