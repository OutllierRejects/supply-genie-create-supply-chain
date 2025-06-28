from fastapi import FastAPI
from .models import AgentConfig, SupplierExplorationAgentResponse
from mangum import Mangum
import asyncio
from .graph import get_graph, prepare_state, extract_final_response
from .utils import get_logger

logger = get_logger()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    "/api/v1/supply-chain/recommendations",
    response_model=SupplierExplorationAgentResponse,
)
async def get_recommendations(requirements: AgentConfig):
    # Build a plain dict of all inputs (query + chat_history)
    input_payload = requirements.dict(exclude_none=True)
    logger.info(f"Input payload: {input_payload}")

    # Prepare the state to match GraphState schema
    prepared_state = prepare_state(input_payload)
    logger.info(f"Prepared state: {prepared_state}")

    # Invoke the graph with the properly formatted state and increased recursion limit
    raw_output = await asyncio.to_thread(
        get_graph().invoke, prepared_state, {"recursion_limit": 10}
    )
    logger.info(f"Raw output from graph: {raw_output}")

    # Extract the final response properly
    final_response = extract_final_response(raw_output)
    logger.info(f"Final response: {final_response}")

    return final_response


handler = Mangum(app)
