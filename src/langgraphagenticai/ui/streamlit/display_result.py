import json
import uuid
import streamlit as st
from src.langgraphagenticai.DynamoDB_Ops.dynamo_db_ops import DynamoDBOps
from src.langgraphagenticai.LLMS.geminillm import GeminiLLM
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message, user_control):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.user_controls_input = user_control
        
    # def insert_chat_message(self, message):
    #     """
    #     Inserts a chat message into the session state.
    #     :param message: The message to insert.
    #     """
    #     try:
    #         dynamodb_ops = DynamoDBOps(user_controls_input=self.user_controls_input)

    #         embedding = dynamodb_ops.get_embeddings(message)
    #         session_id = str(uuid.uuid4())  # Generate a unique session ID
    #         response = dynamodb_ops.save_chat_message(
    #             session_id=session_id,
    #             user_msg=message,
    #             embeddings=embedding
    #         )
    #     except Exception as e:
    #         print(f"Error: While inserting chat message: {e}")
    #         st.error(f"Error: While inserting chat message: {e}")

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if st.button("End Session"):
            st.session_chat = []
            st.success("Chat session ended.")
            st.stop()

        try:
            for msg in st.session_state.get("messages", []):
                if isinstance(msg, HumanMessage):
                    # with st.chat_message("user"):
                    #     st.write(msg.content)
                    pass
                elif isinstance(msg, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(msg.content)
        except Exception as e:
            print(f"Error: While initiating the chat: {e}")
            pass

        try:
            if usecase == "Basic Chatbot":
                for event in graph.stream({'messages': st.session_state["messages"]}):
                    print(event.values())
                    for value in event.values():
                        print(value["messages"])
                        # with st.chat_message("user"):
                        #     st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
                            st.session_state["messages"].append(AIMessage(content=value["messages"].content))

            if usecase == "Call or Put":
                frequency = user_message
                with st.spinner("Analyzing the news..."): 
                    print(4)
                    result = graph.invoke({"messages": frequency})
                    print(5)
                    print("Final Result: ", result)
                try:
                    news_sentiment = f"C:/Users/amit.co.gupta/Desktop/project_profile_matching/AGENTICAICHATBOT_MODEL/src/CompanyNews/{frequency}_sentiment.md"
                    with open(news_sentiment, "r") as f:
                        md_content = f.read()

                    st.markdown(md_content, unsafe_allow_html=True)
                except Exception as e:
                    print(f"Error: While Call or Put: {e}")
                    st.error(f"Error: While Call or Put: {e}")

            if usecase == "arXiv Tutor":
                try:
                    for event in graph.stream({'messages': st.session_state["messages"]}):
                        for value in event.values():
                            if not isinstance(value["messages"],list):
                                with st.chat_message("assistant"):
                                    print(1234)
                                    st.write(value["messages"].content)
                                    # self.insert_chat_message(value["messages"].content)
                                    print(12345)
                                    st.session_state["messages"].append(AIMessage(content=value["messages"].content))
                                    print(123456)
                            else:
                                with st.chat_message("assistant"):
                                    st.write(value["messages"][-1].content)
                                    # self.insert_chat_message(value["messages"][-1].content  )
                                    print(12345)
                                    st.session_state["messages"].append(AIMessage(content=value["messages"][-1].content))
                                    print(123456)
                except Exception as e:
                    print(f"Error: During chat flow: {e}")
        except Exception as e:
            print(f"Error: During graph invoking: {e}")
