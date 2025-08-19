from src.langgraphagenticai.state.state import State


class ChatBotNodes:
    """
    All chatbot nodes logic is implemented here.
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state:State) -> dict:
        """
        Process the input and returns the generated output.
        """
        try:
            result = self.llm.invoke(state["messages"])
        except Exception as e:
            print(f"Error: During Gemini invoking: {e}")
            print(state["messages"])
        return {"messages": self.llm.invoke(state["messages"])}

    