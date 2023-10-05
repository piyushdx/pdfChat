import openai
from flask import jsonify
import os
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

openai.api_key = os.environ.get("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

class UltraBot():
    def __init__(self):
        self.history = []

    def clear_cache(self):
        self.history = []
        return jsonify({"status": "True"})

    def get_response(self, data,pdf_utils):
        query = data["query"]
        response = pdf_utils.chat_with_pdf_single_query(query,self.history)
        self.history.append((query,response))
        print("final_response:", response)
        return jsonify({"response": response})