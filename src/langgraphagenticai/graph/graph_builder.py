from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.nodes.chatbot_nodes import ChatBotNodes
# from src.langgraphagenticai.nodes.company_news_nodes import CompanyNewsNode
from src.langgraphagenticai.nodes.arxiv_article_nodes import ArxivNodes

class GraphBuilder:
    def __init__(self, company, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        self.company = company

    def chatbot_build_graph(self):
        """
        Builds a chatbot graph using LangGraph.
        """
        try:
            self.chatbot_node = ChatBotNodes(self.llm)
            self.graph_builder.add_node("chatbot",self.chatbot_node.process)
            self.graph_builder.add_edge(START,"chatbot")
            self.graph_builder.add_edge("chatbot", END)  
        except Exception as e:
            print(f"Error: While setting up nodes and edges. : {e}")

    def chatbot_with_tool_build_graph(self):
        """
        Builds a chatbot to compare the skills requirred and skills given for the candidate. 
        """
        
    def chatbot_for_company_news(self):
        """
        """
        company_news_node = CompanyNewsNode(self.company,self.llm)
        self.graph_builder.add_node("fetch_news",company_news_node.fetch_news)
        self.graph_builder.add_node("call_or_put", company_news_node.company_call_or_put)
        self.graph_builder.add_node("save_result", company_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "call_or_put")
        self.graph_builder.add_edge("call_or_put", "save_result")
        self.graph_builder.add_edge("save_result", END)

    def chatbot_for_arxiv(self):
        """
        This helps to understand any arxiv article in interactive way.
        """
        arxiv_nodes = ArxivNodes(self.company,self.llm)
        self.graph_builder.add_node("fetch_article",arxiv_nodes.fetch_article)
        self.graph_builder.add_node("article_qna",arxiv_nodes.article_qna)

        self.graph_builder.set_entry_point("fetch_article")
        self.graph_builder.add_edge("fetch_article", "article_qna")
        self.graph_builder.add_edge("article_qna", END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected usecase.
        """
        try:
            if usecase == "Basic Chatbot":
                self.chatbot_build_graph()

            if usecase == "Call or Put":
                self.chatbot_for_company_news()

            if usecase == "arXiv Tutor":
                self.chatbot_for_arxiv()
        except Exception as e:
            print(f"Error: While graph setup: {e}")
        return self.graph_builder.compile()