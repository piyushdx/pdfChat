
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from config import config, environment, ip_config
import re
from ultrabot import UltraBot
import os
app = Flask(__name__)
CORS(app, support_credentials=True)
from pdf_utils import PDFUtils
import os
import shutil

global pdf_utils
pdf_utils = None

ultrabot = UltraBot()

def initialize_pdf_utils():
    global pdf_utils
    if pdf_utils is None:
        if os.path.exists("db"):
            persist_directory = "db"
            pdf_folder_path = "ChatBotUI/static/pdf"
            pdf_utils = PDFUtils(pdf_folder_path, persist_directory)
            pdf_utils.initialize_qa_chain()
            print("we just initialized qa chain with new embedings...")
    return pdf_utils


@app.route('/UltraBot_clear_cache')
@cross_origin(supports_credentials=True)
def UltraBot_clear_cache():
    return ultrabot.clear_cache()

flag = True
@app.route('/UltraBot_get_response', methods=['POST'])
@cross_origin(supports_credentials=True)
def UltraBot_get_response():
    pdf_utils = initialize_pdf_utils()
    return ultrabot.get_response(request.get_json(),pdf_utils)

import os
import shutil

def delete_folder_if_exists(folder_path):
    """
    Check if a folder exists and delete it if it does.
    
    Args:
        folder_path (str): The path to the folder to check and delete.
    
    Returns:
        bool: True if the folder was deleted or didn't exist, False if there was an error.
    """
    try:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Delete the folder and its contents
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been deleted.")
        else:
            print(f"The folder '{folder_path}' does not exist.")
        return True
    except Exception as e:
        print(f"An error occurred while deleting the folder: {e}")
        return False

def create_vector_database():
  persist_directory = "db"
  pdf_folder_path = "ChatBotUI/static/pdf"
  pdf_utils = PDFUtils(pdf_folder_path, persist_directory)
  pdf_utils.create_vector_db_from_pdfs()

@app.route("/convert", methods=["POST"])
@cross_origin(supports_credentials=True)
def upload_file():
    uploaded_file = request.files["pdf"]
    global pdf_utils
    if uploaded_file:
        # Do something with the uploaded file (e.g., save it)
        path = "ChatBotUI/static/pdf/uploaded.pdf"
        uploaded_file.save(path)
        print("file is saved")
        persist_directory = "db"
        delete_folder_if_exists(persist_directory)
        pdf_utils = None
        # Create an instance of PDFUtils class
        create_vector_database()
        # app = Flask(__name__)


        # Use When you want to create a db
        return jsonify({"response": "your Pdf Uploaded Successfully."})
    else:
        return jsonify({"message": "No file uploaded."}), 400

if __name__ == '__main__':
    IP = ip_config[environment]
    response_port = config['BotApplication']['Backend']  # response API
    app.run(host='0.0.0.0', port=response_port)

