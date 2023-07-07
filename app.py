import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from html_template import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_text_from_pdf(docs):
    """
    THIS FUNCTION EXTRACTS TEXT FROM PDF USING PDFREADER AND RETURNS TEXT
    """
    text=""
    for pdf in docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunk(text):
    """
    THIS FUNCTION SPLITS THE RAW TEXT INTO CHUNKS USING LANGCHAIN'S CHARACTER TEXT SPLITTER AND RETURNS CHUNKS"
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        # seperator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(split_text):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vector_store = FAISS.from_texts(texts=split_text,embedding=embeddings)
    pass

def get_conversation_chain(vector_store):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="NLP-PDFs-LangChain",page_icon=":notebook_with_decorative_cover:")
    st.write(css,unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("NLP-PDFs-LangChain :ledger:")
    user_question = st.text_input("Ask questions to the PDFs")
   
    if user_question:
        handle_userinput(user_question)

    
    with st.sidebar:
        st.subheader("Documents")
        
        docs = st.file_uploader("Upload your PDFs",accept_multiple_files=True)
        
        if st.button("Process the PDFs"):
            with st.spinner("Processing the PDFs"):
                raw_text = get_text_from_pdf(docs)
                # st.write(raw_text)
                split_text = get_text_chunk(raw_text)

                vector_store = get_vector_store(split_text)

                st.session_state.conversation = get_conversation_chain(vector_store)

if __name__=='__main__':
    main()