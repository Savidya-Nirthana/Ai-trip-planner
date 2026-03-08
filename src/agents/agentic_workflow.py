# from src.agents.tools.weather_information_tool import WeatherInformationTool
# from src.agents.tools.place_search_tool import PlaceSearchTool
# from src.agents.tools.currency_conversion_tool import CurrencyConversionTool
from langgraph.graph import StateGraph,MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from src.agents.prompt_library import SYSTEM_PROMPT
from src.infrastructure.llm_provider.llm_client import get_chat_llm
from src.infrastructure.config import OPENROUTER_BASE_URL

from src.agents.tools.currency_conversion_tool import CurrencyConverterTool
from src.agents.tools.place_search_tool import PlaceSearchTool
from src.agents.tools.weather_information_tool import WeatherInfoTool
from src.agents.tools.expense_calculator_tool import CalculatorTool

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class GraphBuilder():
    def __init__(self, model_provider: str = "groq"):
        self.llm = get_chat_llm(provider=model_provider)
        self.tools = []

        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.currency_conversion_tools = CurrencyConverterTool()
        self.calculator_tools = CalculatorTool()

        self.tools.extend([
            * self.weather_tools.weather_tool_list,
            * self.place_search_tools.place_search_tool_list,
            * self.currency_conversion_tools.currency_converter_tool_list,
            * self.calculator_tools.calculator_tool_list

        ])

        self.llm_with_tools = self.llm.bind_tools(tools = self.tools)

        self.graph = None

        self.system_prompt = SYSTEM_PROMPT


    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state['messages']
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}


    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")

        self.graph = graph_builder.compile()

        return self.graph

    def __call__(self):
        return self.build_graph()

    