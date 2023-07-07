import streamlit as st

def main():
    st.set_page_config(page_title="NLP-PDFs-LangChain",page_icon=":notebook_with_decorative_cover:")
    st.header("NLP-PDFs-LangChain :ledger:")
    st.text_input("Ask questions to the PDFs")

    with st.sidebar:
        st.subheader("Documents")
        st.file_uploader("Upload your PDFs")
        st.button("Process the PDFs")


if __name__=='__main__':
    main()