from utils.models_loader import ModelLoader
from tools.weather_information_tool import WeatherInformationTool
from tools.place_search_tool import PlaceSearchTool
from tools.currency_conversion_tool import CurrencyConversionTool
from langgraph.graph import StateGraph,MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from agents.prompt_library import SYSTEM_PROMPT






class GraphBuilder():
    def __init__(self):
        self.tools = [
            # WeatherInformationTool(),
            # PlaceSearchTool(),
            # CurrencyConversionTool()
        ]
        self.system_prompt = SYSTEM_PROMPT


    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state['message']
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"message": [response]}


    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_edge("agent", self.agent_function)
        graph_builder.add_edge("router", ToolNode(tools = self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge('tools', "agent")           
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()

        return self.graph

    def __call__(self):
        return self.build_graph()

    