import streamlit as st
from src.langgraphagenticai.ui.streamlit.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.geminillm import GeminiLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlit.display_result import DisplayResultStreamlit
from src.langgraphagenticai.state.state import State
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


def load_langgraph_agenticai_app():
    """
    Loads and run the agentic ai app.
    """
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    print("User Input: ",user_input)
    print("Seesion States: ", st.session_state)

    if not user_input:
        st.error("Error: Failed to load the UI.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
        company_name = st.session_state.COMPANY_NAME
        if company_name:
            print("Company Name: ",company_name)
    else:
        user_message = st.chat_input("input your message:")

    if user_message:
        st.session_state["messages"].append(HumanMessage(content = user_message))

    print("User Message: ",user_message)
    
    if user_message:
        obj_llm_config = GeminiLLM(user_controls_input=user_input)
        model = obj_llm_config.get_llm_models()
        if not model:
            st.error("Error: LLM model could not be found.")
            return
        
        usecase = user_input.get("selected_usecase")
        if usecase=="Call or Put":
            graph_builder = GraphBuilder(company_name, model)
        elif usecase == "arXiv Tutor":
            arxiv_id = st.session_state.ARXIV_ID
            graph_builder = GraphBuilder(arxiv_id, model)
        else:
            graph_builder = GraphBuilder("",model)
            
        try:
            print(1)
            graph = graph_builder.setup_graph(usecase)
            print(2)
            DisplayResultStreamlit(usecase=usecase, graph=graph, user_message=user_message, user_control=user_input).display_result_on_ui()
            print(3)
        except Exception as e:
            print(f"Error: Graph setup failed : {e}")
            st.error(f"Error: Graph setup failed : {e}")
            return