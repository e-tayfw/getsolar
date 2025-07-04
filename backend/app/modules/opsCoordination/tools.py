import dspy
from sqlalchemy.inspection import inspect
from .db import Session
from .models import Lead, LeadEvent
import json


def crm_fetch(lead_id: str) -> str:
    """
    Fetch a lead by ID and return its fields wrapped in a Python docstring.

    Args:
        lead_id (str): The UUID of the lead to fetch.

    Returns:
        str: A triple-quoted docstring containing the lead’s data, or an empty string if not found.
    """
    with Session() as session:
        lead = session.get(Lead, lead_id)
        if not lead:
            return '"""\\nLead not found.\\n"""'

        # Build a plain dict of column→value
        lead_dict = {
            column.key: getattr(lead, column.key)
            for column in inspect(Lead).mapper.column_attrs
        }

        # Serialize to JSON with indentation for readability
        body = json.dumps(lead_dict, indent=4, default=str)

        # Wrap in a docstring
        return f'"""\n{body}\n"""'
    

def crm_update(lead_id: str, status: str, **kwargs) -> None:
    """
    Update a lead's status based on the provided lead_id and status.
    """
    with Session() as session:
        lead = session.get(Lead, lead_id)
        if not lead:
            raise ValueError("Lead not found")
        lead.status = status
        for k, v in kwargs.items():
            setattr(lead, k, v)
        session.add(lead)
        session.commit()
        # Log event
        event = LeadEvent(lead_id=lead_id, event_type=status, payload=kwargs)
        session.add(event)
        session.commit()
