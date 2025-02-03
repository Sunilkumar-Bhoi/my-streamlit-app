import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from utils import clean_text

def makers_details():
    st.subheader("Meet the Makers")
    
    makers = [
        {"name": "Modi Yatri", "linkedin": "https://www.linkedin.com/in/yatri-modi-607825315"},
        {"name": "Bhoi Sunilkumar", "linkedin": "https://www.linkedin.com/in/sunil-bhoi-00104a251"},
    ]

    for maker in makers:
        st.write(f"**{maker['name']}**")
        st.markdown(f"[LinkedIn Profile]({maker['linkedin']})")


def get_in_touch():
    st.markdown("**Want to get in touch?**")  
    st.markdown("For further inquiries, feel free to email us at: [bhois0648@gmail.com](mailto:bhois0648@gmail.com)")


def feedback_form():
    st.title("Feedback Form")
    st.markdown("We value your feedback! Please share your thoughts to help us improve.")
    
    st.markdown("---")

    feedback = st.text_area("**Please leave your feedback here:**", height=150)

    if st.button("Submit Feedback"):
        if feedback:
            with open("feedback.txt", "a") as f:
                f.write(feedback + "\n")
            st.success("Thank you for your feedback! 😊")
        else:
            st.error("Please enter your feedback before submitting.")


def create_streamlit_app(llm, clean_text):
    st.title("📰 News Article Summarizer")
    st.markdown("""
        Enter the URL of a news article, and this tool will generate a concise summary.
        """)
    st.markdown("---")
   
   
    
    url_input = st.text_input("Enter a URL:", value="Please Enter a Link", help="Paste a valid news article URL here.")
    submit_button = st.button("🚀 Summarize Now")

    if submit_button and url_input:
        with st.spinner("Hold tight! Great things take time... 🌟"): 
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                
                json_res = llm.news_extract(data)
                samary = llm.write_summaries(json_res)
                
                st.success("Summary generated!")
                st.code(samary, language='markdown')
                
            except Exception as e:
                st.error(f"An Error Occurred: {e}")
            

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title=" News Article Summarizer", page_icon="📰")
    create_streamlit_app(chain, clean_text)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Feedback"):
            feedback_form() 

    with col2:
        if st.button("Meet the Makers"):
            makers_details()
    
    with col3:
        if st.button("Get in Touch"):
            get_in_touch()
