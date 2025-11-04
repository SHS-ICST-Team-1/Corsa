from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import pdfplumber
import os

app = Flask(__name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')
    
if not os.path.exists('extractedFiles'):
    os.makedirs('extractedFiles')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Analyze the PDF immediately after upload
        try:
            extracted_content, output_file = read_coursebook_pdf(filename)
            
            return jsonify({
                'success': True,
                'message': 'File uploaded and analyzed successfully',
                'filename': filename,
                'extracted_file': output_file,
                'preview': extracted_content[:500] + "..." if len(extracted_content) > 500 else extracted_content
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'PDF analysis failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

def read_coursebook_pdf(filename):
    file_path = os.path.join('uploads', filename)
    
    if not os.path.exists(file_path):
        return "File not found", None
    
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            print(f"Analyzing pdf: {filename} ({len(pdf.pages)} pages)")
            
            for page_num, page in enumerate(pdf.pages):

                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {page_num + 1} ---\n{page_text}\n\n"

                tables = page.extract_tables()
                if tables:
                    text += f"--- Tables on Page {page_num + 1} ---\n"
                    for i, table in enumerate(tables):
                        text += f"Table {i+1}:\n"
                        for row in table:
                            clean_row = [str(cell) if cell is not None else "" for cell in row]
                            text += " | ".join(clean_row) + "\n"
                        text += "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return f"Error: {e}", None
    output_filename = f"extracted_{filename.replace('.pdf', '')}.txt"
    output_path = os.path.join('extractedFiles', output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Content saved as path '{output_path}'")
    
    return text, output_filename

if __name__ == "__main__":
    app.run(debug=True, port=5002)