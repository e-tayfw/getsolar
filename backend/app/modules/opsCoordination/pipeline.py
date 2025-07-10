import dspy
from app.modules.opsCoordination.signatures import FormIngestion, EmailIngestion, QualificationIntent, GenerateQualificationQuestions, QualificationEvaluator
from app.modules.opsCoordination.tools import create_lead, create_user, get_user_by_id, update_qualification_based_on_user, create_qualification, vectorRetrieval, assemble_context_from_form, create_lead, update_lead_status

class FormQualificationPipeline(dspy.Module):

    """
    A pipeline for processing form submissions to generate qualification questions.
    """

    def __init__(self):
        self.form_ingestion = dspy.ReAct(signature=FormIngestion, tools=[create_user, create_lead, get_user_by_id])
        self.generate_questions = dspy.ReAct(signature=GenerateQualificationQuestions, tools=[create_qualification, update_lead_status])
        
    async def aforward(self, **form_inputs):
        # Step 1: Ingest form data
        ingestion_result = await self.form_ingestion(**form_inputs)
        # Step 2: Assemble context with criteria retrieval
        context = assemble_context_from_form(form_inputs)
        # Step 3: Generate qualification questions
        questions_result = await self.generate_questions(
            lead_id=ingestion_result.lead_id,
            context=context
        )
        return {
            "lead_id": ingestion_result.lead_id,
            "questions": questions_result.questions,
            "context": context
        }


class EmailOpsPipeline(dspy.Module):
    """
    A pipeline for operations coordination that handle user replies from emails on either submission of qualification questions or booking requests.
    """

    def __init__(self):
        self.ingestion = dspy.ChainOfThought(EmailIngestion)


                


            

