PDF Data Extractor Backend Service

from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_data_from_pdf(file):
    try:
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ""
        for i in range(0, number_of_pages):
            page = reader.pages[i]
            text = text + page.extract_text()
        
        text_list = text.split("\n")
        text_list[2] = text_list[2][9:]
        text_list[2] = re.sub(r'[0-9]+', '', text_list[2])
        text_list[2] = re.sub(r'-', '', text_list[2])
        text_list[2] = re.sub(r' ', '', text_list[2]) 
        text_list.pop()
        text_list.pop()

        # Regex patterns
        name_pattern = r"^(.+)$"
        dob_gender_pattern = r"^(\d{4})\s([MF])$"
        place_pattern = r"^[A-Z0-9]+(.+)$"

        # Extract data
        name = re.search(name_pattern, text, re.MULTILINE).group(1).strip()
        dob_gender_match = re.search(dob_gender_pattern, text, re.MULTILINE)
        dob = dob_gender_match.group(1)
        gender = dob_gender_match.group(2)
        place = text_list[2]

        # Return extracted data
        return {
            "beneficiaryName": name,
            "dob": dob,
            "gender": gender,
            "area": place,
            "formDate": "",
            "teamMember": "",
            "mobile": "",
            "religion": "",
            "caste": "",
            "occupation": "",
            "cardsApply": "",
            "schemeApply": "",
            "familyIncome": "",
            "differentlyAbled": "",
            "proofOfEvidence": ""
        }
    except Exception as e:
        return {
            "error": str(e),
            "beneficiaryName": "",
            "dob": "",
            "gender": "",
            "area": "",
            "formDate": "",
            "teamMember": "",
            "mobile": "",
            "religion": "",
            "caste": "",
            "occupation": "",
            "cardsApply": "",
            "schemeApply": "",
            "familyIncome": "",
            "differentlyAbled": "",
            "proofOfEvidence": ""
        }

@app.route('/api/extract-pdf', methods=['POST'])
def extract_pdf():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files[]')
    extracted_data = []
    
    for file in files:
        if file.filename == '':
            continue
        if file and file.filename.endswith('.pdf'):
            data = extract_data_from_pdf(file)
            extracted_data.append(data)
    
    return jsonify(extracted_data)

@app.route('/api/save-data', methods=['POST'])
def save_data():
    data = request.json
    # Here you would implement logic to save the data to a database
    # For now, we'll just return the data
    return jsonify({'status': 'success', 'data': data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
