import os
import PyPDF2
import json
import base64
import streamlit as st

from utils import ask_question

# Constants
QUEUE_SIZE_THRESHOLD = 3
from constants import text_queue
# Queue to store the text

# Function to store the text in the queue
def store_text(text):
    text_queue.append(text)
    if len(text_queue) >= QUEUE_SIZE_THRESHOLD:
        process_queue()

# Function to process the text queue and create a JSON file
def process_queue():
    # Process the text queue here
    # Create a JSON file with the processed data
    processed_data = {"data": text_queue}  # Placeholder for processed data
    with open("processed_data.json", "w") as file:
        json.dump(processed_data, file)
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
    st.title("PDF Selector for propmts")

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

    # Check if the queue is ready for processing
    if len(text_queue) >= QUEUE_SIZE_THRESHOLD:
        st.warning("Queue is ready for processing. Click the 'Process Queue' button.")
        if st.button("Process Queue"):
            process_queue()
            st.success("Queue processed successfully!")

def question_page():
    st.title("Ask the model a question")
    
    selected_text = st.text_area("Question")
    if st.button("Ask"):
        answer = ask_question(selected_text)
        st.success("Question asked successfully!")
        st.write(answer)

# Streamlit app
def main():
    st.sidebar.title("Navigation")
    page_options = ["Home", "Ask a question", "Contact"]

    selected_page = st.sidebar.radio("Go to", page_options)

    if selected_page == "Home":
        pdf_page()
    elif selected_page == "Ask a question":
        question_page()
    elif selected_page == "Contact":
        contact_page()

    
    #pdf_files = [x for x in os.listdir() if x.endswith(".pdf")]
    
    # Upload PDF file
    

    #if file_path is not None:
        # Read PDF file
        #pdf_reader = PyPDF2.PdfFileReader(uploaded_file)

        #num_pages = pdf_reader.numPages
        
        # Display PDF content
        #st.write(f"Number of pages: {num_pages}")
        
        #for page_num in range(num_pages):
        #    page = pdf_reader.getPage(page_num)
        #    st.write(page.extractText())
        #displayPDF(file_path)
        
        #st.write("---")
        
        # Text box for copying selected parts of the PDF
    
    
    

# Run the Streamlit app
if __name__ == '__main__':
    main()

