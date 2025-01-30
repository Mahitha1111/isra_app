import streamlit as st
from PyPDF2 import PdfReader
#import os
import pandas as pd
import re
# Function to extract data from PDF
def extract_data_from_pdf(file):
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    text=""
    for i in range(0, number_of_pages):
        page = reader.pages[i]
        text=text+page.extract_text()
    text_list=text.split("\n")
    text_list[2]=text_list[2][9:]
    #delete last two elements of the list
    text_list.pop()
    text_list.pop()

    # Input text


    # Regex patterns
    name_pattern = r"^(.+)$"
    dob_gender_pattern = r"^(\d{4})\s([MF])$"
    place_pattern = r"^[A-Z0-9]+(.+)$"
    dist_pattern = r"^([A-Z]+)[A-Z]*$"

    # Extract Name
    name = re.search(name_pattern, text, re.MULTILINE).group(1).strip()

    # Extract DOB and Gender
    dob_gender_match = re.search(dob_gender_pattern, text, re.MULTILINE)
    dob = dob_gender_match.group(1)
    gender = dob_gender_match.group(2)

    # Extract Place
    place = re.search(place_pattern, text, re.MULTILINE).group(1).strip()
    place=text_list[2]

    # Extract District
    #dist = re.search(dist_pattern, text, re.MULTILINE).group(1).title()

    # Print the extracted information
    print(f"Name: {name}")
    print(f"DOB: {dob}")
    print(f"Gender: {gender}")
    print(f"Place: {place}")

    # Here you would implement logic to extract name, dob, etc. from the text
    # For demonstration, let's assume we extract dummy data
    #Form Date
    #Team Member 
    #Beneficiary Name
    #Gender
    #DOB
    #Area
    #Mobile 
    #Religion 
    #Caste
    #Occupation 
    #Cards Apply
    #Scheme Apply
    #Family Income
    #Differently Abled
    #Proof of Evidence
    return {
        "Benficiary Name": name,
        "DOB": dob,
        "Gender": gender,
        "Area": place,
    }

# Initialize session state for storing extracted data
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# File uploader for multiple PDF files
uploaded_files = st.file_uploader("Upload your PDFs here:", type="pdf", accept_multiple_files=True)

# Process uploaded files
if uploaded_files:
    st.session_state.pdf_data = [extract_data_from_pdf(file) for file in uploaded_files]
    st.session_state.current_index = 0  # Reset index after new upload

# Navigation buttons
if st.session_state.pdf_data:
    if st.button("Back") and st.session_state.current_index > 0:
        st.session_state.current_index -= 1
    if st.button("Forward") and st.session_state.current_index < len(st.session_state.pdf_data) - 1:
        st.session_state.current_index += 1

    # Display current data card
    current_data = st.session_state.pdf_data[st.session_state.current_index]
    
    # Editable form for the extracted data
    with st.form(key='data_card_form'):
        name = st.text_input("Benficiary Name", value=current_data["Benficiary Name"])
        dob = st.text_input("Date of Birth", value=(current_data["DOB"]))
        gender = st.text_input("Gender", value=current_data["Gender"])
        place = st.text_input("Area", value=current_data["Area"])
        
        # Submit button to save changes (you can implement saving logic here)
        submit_button = st.form_submit_button("Save Changes")
        if submit_button:
            # Update the session state with edited values
            st.session_state.pdf_data[st.session_state.current_index] = {
                "Benficiary Name": {name},
                "DOB": {dob},
                "Gender": {gender},
                "Area": {place},
                
            }
            st.success("Changes saved!")

# Display the current index and total number of cards
if st.session_state.pdf_data:
    total_cards = len(st.session_state.pdf_data)
    st.write(f"Viewing {st.session_state.current_index + 1} of {total_cards} data cards.")
