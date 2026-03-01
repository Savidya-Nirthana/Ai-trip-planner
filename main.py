from fastapi import FastAPI
from pydantic import BaseModel
from src.agents.agentic_workflow import GraphBuilder
import os
from fastapi.responses import JSONResponse

app = FastAPI()


class QueryRequest(BaseModel):
    """
    Request model for a travel query.

    Attributes:
        query (str): The travel-related query from the user.
    """
    query: str


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    """
    Processes a travel-related query using a ReAct agent workflow.

    This function initializes a ReAct agent with the Groq model provider, 
    generates and saves a graph visualization of the workflow, and invokes 
    the agent to obtain a response for the user's query.

    Args:
        query (QueryRequest): The request object containing the travel query.

    Returns:
        dict: A dictionary containing the agent's final answer or a JSONResponse error.
    """
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()

        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        
        print(f"Graph saved to my_graph.png in {os.getcwd()}")

        messages = react_app.invoke({"messages": [query.question]})

        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})