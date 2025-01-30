# import streamlit as st
# import PyPDF2

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# # Function to create an editable data card
# def display_editable_data_card(data):
#     st.subheader("Extracted Information (Editable)")
#     edited_data = {}
#     for key, value in data.items():
#         # Use a text input for each key-value pair
#         edited_data[key] = st.text_input(f"{key}", value, key=key)
#     return edited_data

# # Main Streamlit app
# def main():
#     # Set the title and description
#     st.title("📄 PDF Information Extractor")
#     st.write("Upload a PDF document to extract and edit information.")

#     # File uploader for PDF
#     uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_uploader")

#     if uploaded_file is not None:
#         # Extract text from PDF
#         extracted_text = extract_text_from_pdf(uploaded_file)

#         # Display extracted text in a scrollable area
#         st.subheader("Extracted Text from PDF")
#         st.text_area("Extracted Text", extracted_text, height=200, key="extracted_text_area")

#         # Parse extracted text into key-value pairs (customize as needed)
#         # Example: Assume the text contains lines like "Key: Value"
#         data = {}
#         for line in extracted_text.split("\n"):
#             if ":" in line:
#                 key, value = line.split(":", 1)
#                 data[key.strip()] = value.strip()

#         # Display editable data card
#         st.markdown("---")
#         edited_data = display_editable_data_card(data)

#         # Save edited data
#         if st.button("💾 Save Edits", key="save_button"):
#             st.success("Edited Data Saved!")
#             st.json(edited_data)

# # Run the app
# if __name__ == "__main__":
#     main()
# import streamlit as st
# import PyPDF2

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# # Function to create an editable data card for a single PDF
# def display_editable_data_card(data, file_name):
#     st.subheader(f"📄 Extracted Information from {file_name}")
#     edited_data = {}
#     for key, value in data.items():
#         # Use a text input for each key-value pair
#         edited_data[key] = st.text_input(f"{key}", value, key=f"{file_name}_{key}")
#     return edited_data

# # Main Streamlit app
# def main():
#     # Set the title and description
#     st.title("📄 PDF Information Extractor")
#     st.write("Upload multiple PDF documents to extract and edit information.")

#     # File uploader for multiple PDFs
#     uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True, key="pdf_uploader")

#     if uploaded_files:
#         # Process each uploaded file
#         for uploaded_file in uploaded_files:
#             # Extract text from PDF
#             extracted_text = extract_text_from_pdf(uploaded_file)

#             # Display extracted text in a scrollable area
#             st.subheader(f"📄 Extracted Text from {uploaded_file.name}")
#             st.text_area("Extracted Text", extracted_text, height=200, key=f"extracted_text_{uploaded_file.name}")

#             # Parse extracted text into key-value pairs (customize as needed)
#             # Example: Assume the text contains lines like "Key: Value"
#             data = {}
#             for line in extracted_text.split("\n"):
#                 if ":" in line:
#                     key, value = line.split(":", 1)
#                     data[key.strip()] = value.strip()

#             # Display editable data card for this file
#             st.markdown("---")
#             edited_data = display_editable_data_card(data, uploaded_file.name)

#             # Save edited data for this file
#             if st.button(f"💾 Save Edits for {uploaded_file.name}", key=f"save_button_{uploaded_file.name}"):
#                 st.success(f"Edited Data Saved for {uploaded_file.name}!")
#                 st.json(edited_data)

#             # Add a separator between files
#             st.markdown("---")

# # Run the app
# if __name__ == "__main__":
#     main()
import streamlit as st
import PyPDF2

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to create an editable data card for a single PDF
def display_editable_data_card(data, file_name):
    st.subheader(f"📄 Extracted Information from {file_name}")
    edited_data = {}
    for key, value in data.items():
        # Use a text input for each key-value pair
        edited_data[key] = st.text_input(f"{key}", value, key=f"{file_name}_{key}")
    return edited_data

# Main Streamlit app
def main():
    # Set the title and description
    st.title("📄 PDF Information Extractor")
    st.write("Upload multiple PDF documents to extract and edit information.")

    # Initialize session state for current card index
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # File uploader for multiple PDFs
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True, key="pdf_uploader")

    if uploaded_files:
        # Extract text from all uploaded files and store in session state
        if "extracted_data" not in st.session_state:
            st.session_state.extracted_data = []
            for uploaded_file in uploaded_files:
                extracted_text = extract_text_from_pdf(uploaded_file)
                data = {}
                for line in extracted_text.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        data[key.strip()] = value.strip()
                st.session_state.extracted_data.append({
                    "file_name": uploaded_file.name,
                    "data": data
                })

        # Display navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_index == 0):
                st.session_state.current_index -= 1
        with col2:
            if st.button("➡️ Next", disabled=st.session_state.current_index == len(uploaded_files) - 1):
                st.session_state.current_index += 1

        # Display current card
        current_data = st.session_state.extracted_data[st.session_state.current_index]
        edited_data = display_editable_data_card(current_data["data"], current_data["file_name"])

        # Save edited data for the current card
        if st.button("💾 Save Edits", key=f"save_button_{current_data['file_name']}"):
            st.success(f"Edited Data Saved for {current_data['file_name']}!")
            st.json(edited_data)

# Run the app
if __name__ == "__main__":
    main()