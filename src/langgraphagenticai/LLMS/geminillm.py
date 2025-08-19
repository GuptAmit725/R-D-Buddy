import os
import asyncio
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


class GeminiLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_models(self):
        try:
            gemini_api_key = self.user_controls_input["GEMINI_API_KEY"]
            selectd_model = self.user_controls_input["selected_gemini_model"]
            if gemini_api_key=="" and os.environ["GEMINI_API_KEY"]=="":
                st.error("Error: Kindly provide the api key.")

            llm = ChatGoogleGenerativeAI(api_key = gemini_api_key, model = selectd_model)
        except Exception as e:
            raise ValueError(f"Error occured with exception: {e}")
        
        return llm
    
    def get_embeddings(self, query):
        # Set API key as environment variable
        os.environ["GOOGLE_API_KEY"] = self.user_controls_input["GEMINI_API_KEY"]
        gemini_model = "models/embedding-001"
        try:
            embeddings_model = GoogleGenerativeAIEmbeddings(model=gemini_model)
            return embeddings_model.embed_query(query)
        except Exception as e:
            raise ValueError(f"Error occured with exception: {e}")