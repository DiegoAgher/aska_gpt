import os
import PyPDF2
import json
import base64
import streamlit as st

from utils import ask_question, get_example_db

# Constants
QUEUE_SIZE_THRESHOLD = 2
from constants import text_queue
# Queue to store the text

# Function to store the text in the queue
def store_text(text):
    text_queue.append(text)
    if len(text_queue) >= QUEUE_SIZE_THRESHOLD:
        process_queue()

# Function to process the text queue and create a JSON file
def process_queue(filename):
    # Process the text queue here
    # Create a JSON file with the processed data

    with open(filename, 'w') as f:
        for item in text_queue:
            f.write(json.dumps(item) + "\n")
    # Clear the text queue
    text_queue.clear()

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="500" height="700" type="application/pdf">'
    #= F"<embed src="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" width="400" height="400">

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

    return

def contact_page():
    st.title("Contact Page")


def pdf_page():
    st.title("PDF Selector for fine tune")

    if st.button("Render PDF"):
        file_path = "dall-e_.pdf"#st.selectbox('file to upload', pdf_files)
        with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'

        st.markdown(pdf_display, unsafe_allow_html=True)

    selected_text = st.text_area("Selected Text")
    if st.button("Store Text"):
        store_text(selected_text)
        st.success("Text stored successfully!")
        st.write(len(text_queue))

    with st.form(key='columns_in_form'):
        c1, c2 = st.columns(2)
        with c1:
            prompt = st.text_input("Prompt")
        with c2:
            complete = st.text_input("Complete")        

        submitButton = st.form_submit_button(label='Create prompt')

        if submitButton:
            if len(text_queue) >= QUEUE_SIZE_THRESHOLD:
                st.warning("Queue is ready for processing.")
            text_queue.append({"prompt":prompt, "completion":complete})

            st.success("Text stored successfully!")

    if st.button("Click to Process Queue"):
        process_queue()
        st.success("Queue processed successfully!")


def question_page():
    st.title("Ask ChatGPT a question")
    
    selected_text = st.text_area("Question")
    if st.button("Ask"):
        answer = ask_question(selected_text)
        st.success("Question asked successfully!")
        st.write(answer)

def custom_question_doc():
    db = get_example_db()
    st.title("Custom Question formatter")
    st.write("Here is a template builder for your question")
    
    with st.form("my_form"):
        intro_options = ["You are an expert salesman in our company, ", "As an experiences engineer,"]

        selected_intro = st.selectbox("Select your intro", intro_options)

        prompt = selected_intro

        solve_options =["I want to recommend our best seller", "I want to recommend product that solves task 'a'",
                        "What is our best selling product?"]

        selected_solve = st.selectbox("Select your intro", solve_options)
        prompt = prompt + selected_solve

        st.write("Our database", db)

        db_str = db.to_string()
        prompt = prompt + " considering our database:\n------\n" + db_str + " \n------\n "
        st.write("Your question: ")
        st.write(prompt)
        prompt = prompt + ".\n be clear and concise in your answer."

        submitted = st.form_submit_button("Submit")
        if submitted:
            print("right after click")
            print(prompt)
            answer = ask_question(prompt)
            st.success("Question asked successfully!")
            st.write(answer)

# Streamlit app
def main():
    st.sidebar.title("Navigation")
    page_options = ["Home", "Ask a question", "Custom Question formatter"]

    selected_page = st.sidebar.radio("Go to", page_options)

    if selected_page == "Home":
        pdf_page()
    elif selected_page == "Ask a question":
        question_page()
    elif selected_page == "Custom Question formatter":
        custom_question_doc()
    

# Run the Streamlit app
if __name__ == '__main__':
    main()

