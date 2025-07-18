from app.utils.models import QueryForm, QueryRequest
from app.modules.customerSupport.pipeline import CustomerSupportPipeline
from app.modules.opsCoordination.pipeline import FormQualificationPipeline
import dspy 
from dotenv import load_dotenv


load_dotenv()


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

async def form(request: QueryForm):
    """
    Routes the form submission to the appropriate pipeline.
    """

    llm = dspy.LM(
        model="gpt-4o",
        temperature=0.0,
        max_tokens=5000,
        top_p=0.9
    )

    pipeline = FormQualificationPipeline()

    with dspy.context(lm=llm):
        lead_id, questions, context = await pipeline.acall(
            user_id=request.user_id,
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address,
            company=request.company,
            referral_source=request.referral_source,
            budget=request.budget,
            timeline_months=request.timeline_months,
            interest_level=request.interest_level,
            requested_capacity=request.requested_capacity,
            enquiry=request.enquiry,
        )
    
    return {
        "lead_id": lead_id,
        "questions": questions,
        "context": context
    }






