from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Create uploads folder if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    if file and file.filename.endswith('.pdf'):
        # Process the PDF file here
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return 'File uploaded successfully', 200
    
    return 'Invalid file type', 400

if __name__ == "__main__":
    app.run(debug=True, port=5002)