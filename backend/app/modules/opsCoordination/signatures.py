import dspy 
from typing import Literal, Dict, Any 

class FormIngestion(dspy.Signature):
    """
    Ingest raw user request data from form
    """

    user_id: str = dspy.InputField(desc="Unique identifier for the user")
    name: str = dspy.InputField(desc="Name of the user making the request")
    email: str = dspy.InputField(desc="Email of the user making the request")
    phone: str = dspy.InputField(desc="Phone number of the user making the request")
    address: str = dspy.InputField(desc="Address of the user, can be property or billing address")
    company: str = dspy.InputField(desc="Company name of the user, if applicable")
    referral_source: str = dspy.InputField(desc="How the user heard about the company, e.g., Website, Email, Social Media, Friend/Referral, Other")
    budget: int = dspy.InputField(desc="Estimated budget for the solar system in SGD")
    timeline_months: int = dspy.InputField(desc="Expected installation timeframe in months")
    interest_level: str = dspy.InputField(desc="Interest level of the user in the company's products or services, e.g., Low, Medium, High")
    requested_capacity: str = dspy.InputField(desc="Desired system capacity in kW")
    enquiry: str = dspy.InputField(desc="User's enquiry or message regarding the company's products or services")
    lead_id: int = dspy.OutputField(desc="7 digit Lead ID of the user, created for the database")
    details: dict = dspy.OutputField(desc="Formatted details extracted from the user request in a clear manner")

class EmailIngestion(dspy.Signature):
    """
    Ingest raw user request data from form
    """

    mail: str = dspy.InputField(desc="Email of the user making the request")
    user_request: str = dspy.InputField(desc="Raw User Request without any formatting or processing")
    user_intent: Literal["qualification", "booking", "cancellation"] = dspy.OutputField(desc="User Intent for the request")
    details: dict = dspy.OutputField(desc="Formatted details extracted from the user request in a clear manner")

class GenerateQualificationQuestions(dspy.Signature):
    """
    Generate qualification questions using the company's products and services, 
    along with the user's information based on the user request
    Context comes from vector retrieval of criteria document and user details
    """

    lead_id: int = dspy.InputField(desc="Lead ID of the user")
    context: dict = dspy.InputField(desc="Contextual information and structured details about the user")
    questions: list[str] = dspy.OutputField(desc="List of qualification questions to ask the user")

class QualificationEvaluator(dspy.Signature):
    """
    Evaluate the user's responses to the qualification questions,
    Use the criteria and other information to determine if the user qualifies for the company's products or services.
    Update the database accordingly and provide feedback on the user's responses.
    """
    
    responses: str = dspy.InputField(desc="User's responses to the qualification questions")
    result: bool = dspy.OutputField(desc="True if the user qualifies, False otherwise")
    feedback: str = dspy.OutputField(desc="Feedback on the user's responses, including areas for improvement or next steps")







