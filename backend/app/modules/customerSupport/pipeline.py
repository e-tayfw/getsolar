from app.modules.customerSupport.tools import faqRetrieval, vectorRetrieval, webSearch
from app.modules.customerSupport.signatures import ResponseGenerator, ReactSignature
import dspy 
import mlflow
import mlflow.dspy


mlflow.set_tracking_uri("http://localhost:5001")
mlflow.set_experiment("DSPy Get Solar AI Customer Support")
mlflow.dspy.autolog()

react_agent = dspy.ReAct(signature=ReactSignature, tools=[faqRetrieval, vectorRetrieval, webSearch])

class CustomerSupportPipeline(dspy.Module):
    """
    A pipeline for customer support that retrieves relevant information from FAQs and vector databases,
    and generates a clean response based on the user's query.
    """
    
    def __init__(self):
        self.response_generator = dspy.ChainOfThought(ResponseGenerator)
        self.react_agent = react_agent

    async def aforward(self, user_query: str, history = None):
        """
        Processes the user query to generate a clean response.
        """

        if history is None:
            history = dspy.History(messages=[])

        # Uses the react agent to output proper conetext
        # Pass history to ReAct agent

        faq_result = faqRetrieval(user_query)
        print("FAQ Retrieval Output:", faq_result)
        vector_result = vectorRetrieval(user_query)
        print("Vector Retrieval Output:", vector_result)
        web_result = webSearch(user_query)
        print("Web Search Output:", web_result)

        react_result = await self.react_agent.acall(user_query=user_query, history=history)
        context = react_result.response

        response = self.response_generator(user_query=user_query, context=context, history=history)

        history.messages.append({"user_query": user_query, "response": response.response})
        
        return response.response, history
    


            
