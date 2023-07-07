import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader


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


def main():
    load_dotenv()
    st.set_page_config(page_title="NLP-PDFs-LangChain",page_icon=":notebook_with_decorative_cover:")
    st.header("NLP-PDFs-LangChain :ledger:")
    st.text_input("Ask questions to the PDFs")

    with st.sidebar:
        st.subheader("Documents")
        
        docs = st.file_uploader("Upload your PDFs",accept_multiple_files=True)
        
        if st.button("Process the PDFs"):
            with st.spinner("Processing the PDFs"):
                raw_text = get_text_from_pdf(docs)
                st.write(raw_text)


if __name__=='__main__':
    main()