
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = loader.load().pop().page_content
            st.write("🔹 Raw data type:", type(data))

            data = clean_text(data)
            st.write("🔹 Cleaned text type:", type(data))

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            st.write("🔹 Jobs type:", type(jobs))
            st.write("🔹 Jobs data:", jobs)

            for job in jobs:
                st.write("🔹 Job entry type:", type(job))
                skills = job.get('skills', [])
                st.write("🔹 Skills type:", type(skills))
                links = portfolio.query_links(skills)
                st.write("🔹 Links type:", type(links))
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

