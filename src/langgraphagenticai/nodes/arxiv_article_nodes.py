from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import ArxivRetriever
import streamlit as st

class ArxivNodes:
    def __init__(self, arxiv_id, llm):
        """
        Initiate CompanyNews class.  
        """
        self.retriever = ArxivRetriever(
        load_max_docs=1,
        get_ful_documents=True,
        )
        self.llm  = llm
        self.state = {}
        self.id = arxiv_id

    def fetch_article(self, state:dict) -> dict:
        """
        Fetch the news for the company.
        
        Args:
            state (dict): Information about the State of graph. Here it contains news frequency.

        Returns:
            dict: State along with news.
        """
        docs = self.retriever.invoke(self.id)

        state["article_content"] = docs
        self.state["article_content"] = state["article_content"]
        return state
    
    def fetch_intent(self, state: dict) -> dict:
        """ Fetch the intent of the article.
        Args:
            state (dict): Information about the State of graph. Here it contains article content.   
        Returns:
            dict: updated state with intent.
        """
        message = self.state["messages"] 
        state["messages"] = self.state["messages"]
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a friendly agent. Your task is to analyse the given user query.\n
            So your task is to find the intent of the article.\n    
            TIf the intent is to 'generate a blog' then return generate_blog else None.\n
            ************** USER QUERY *****************\n
            {message}   
            """)
        ])
        response = self.llm.invoke(prompt_template.format(message=message))     
        self.state["messages"] = [response.content]
        state["messages"] = self.state["messages"]
        return self.state 
    

    
    def generate_blog(self, state: dict) -> dict:
        """
        This function generate a blog out of the article given.
        """
        article = self.state["article_content"] 
        state["article_content"] = self.state["article_content"]

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a friendly agent. Your task is to analyse the given article.\n
                        So your task is to generate a blog out of the article given. \n
                        The blog should in Markdown format and the standard rules must be followed for generating the blog.\n
                        Properly use heading ans subheading in the article.\n
                        ************** ARTICLE CONTENT *****************\n
                        {article_content}  
            """)
        ])
        response = self.llm.invoke(prompt_template.format(article_content = article))
        self.state["messages"] = [response.content]
        state["messages"] = self.state["messages"]
        return {"messages": self.llm.invoke(prompt_template.format(article_content = article, query=state["messages"]))}
    
    def article_qna(self, state: dict) -> dict:
        """
        Discuss the article with bot.
        
        Args:
            state (dict): Information about the State of graph. Here it contains article content.

        Returns:
            dict: updated state with Q&A.
        """
        print(6)
        article = self.state["article_content"] 
        state["article_content"] = self.state["article_content"]
        print(7)

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a scientific technical chatbot. Your task is to analyse the given article and aswer the user query accordingly.\n 
            Answer the user query in detailed manner.\n 
            If the user query is not related to the article then politely tell the user that you are not able to answer the query.\n 
            If the user is being friendly then answer in friendly manner.\n
            If the user asks for genrating the blog then the answer should be in Markdown format and the standard rules must be followed for generating the blog. Properly use heading ans subheading in the answer.\n
            
            ************** ARTICLE CONTENT *****************\n
                        {article_content}  
            """),
            ("user", "{query}")
        ])
        print(8)
        response = self.llm.invoke(prompt_template.format(article_content = article, query=state["messages"]))
        print(9)
        self.state["messages"] = [response.content]
        state["messages"] = self.state["messages"]
        return {"messages": self.llm.invoke(prompt_template.format(article_content = article, query=state["messages"]))}