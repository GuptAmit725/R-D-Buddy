import uuid
import boto3
from decimal import Decimal
from datetime import datetime
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.langgraphagenticai.LLMS.geminillm import GeminiLLM

# DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # e.g., us-east-1
table = dynamodb.Table('ChatHistory')

class DynamoDBOps:
    """
    Class to handle DynamoDB operations for storing chat history and embeddings.
    """ 
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_embeddings(self, query: str):
        """
        Returns the embeddings object for the Gemini model.
        :param query: The query string to get embeddings for.
        :return: Embeddings object.
        """
        gemini_obj = GeminiLLM(self.user_controls_input)
        try:
            embeddings = gemini_obj.get_embeddings(query)
        except Exception as e:
            raise ValueError(f"Error occurred while getting embeddings: {e}")   
        return embeddings

    def save_chat_message(self, session_id: str, user_msg: str, embeddings: list):
        """
        Saves the chat message to DynamoDB.
        :param session_id: Unique identifier for the session.
        :param user_msg: User's message.
        :param embeddings: List of embeddings for the user message.
        """
        timestamp = datetime.utcnow().isoformat()

        try:
            response = table.put_item(
                Item={
                    'SessionId': session_id,
                    'Timestamp': timestamp,
                    'Message': user_msg,
                    'Embeddings': [Decimal(str(x)) for x in embeddings]  # Convert embeddings to Decimal for DynamoDB compatibility
                }
            )
            print(f"Saved chat at {timestamp}")
            return response
        except Exception as e:
            print("Error saving chat:", str(e))
            return None
        
# dynamodb_ops = DynamoDBOps(user_controls_input={
#     "GEMINI_API_KEY": "AIzaSyBjgyob0DV8TtNC8GmUEOlGc6YiPOGo0uA",
#     "selected_gemini_model": "models/embedding-001"  # Example model, adjust as needed
# })

# embedding = dynamodb_ops.get_embeddings("What is the capital of France?")
# session_id = str(uuid.uuid4())  # Generate a unique session ID
# response = dynamodb_ops.save_chat_message(
#     session_id=session_id,                      
#     user_msg="What is the capital of France?",
#     bot_reply="The capital of France is Paris.",
#     embeddings=embedding
# )