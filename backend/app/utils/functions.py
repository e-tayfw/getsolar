import dspy 
from dotenv import load_dotenv


load_dotenv()

from app.utils.models import QueryRequest
from app.modules.customerSupport.pipeline import CustomerSupportPipeline

user_histories = {}

async def chat(request: QueryRequest):
    """
    Handles the customer support chat request.
    """

    llm = dspy.LM(
        model="gpt-4o",
        temperature=0.0,
        max_tokens=5000,
        top_p=0.9
    )

    history = user_histories.get(request.user_id, None)
    pipeline = CustomerSupportPipeline()

    with dspy.context(lm=llm):
        response, updated_history = await pipeline.acall(user_query=request.user_query, history=history)
    
    user_histories[request.user_id] = updated_history

    return {"response": response}





