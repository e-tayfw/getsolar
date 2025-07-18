import json
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any, List, Optional, Dict
from mailersend import MailerSend
from mailersend.models import Template, Personalization
import os
import weaviate
from dotenv import load_dotenv

load_dotenv()


CRITERIA_COLLECTION_NAME = "getSolarLeadCriteria"
mailer = MailerSend(api_key=os.getenv("MAILERSEND_API_KEY"))
weaviate_port = int(os.getenv("WEAVIATE_PORT"))
weaviate_host = os.getenv("WEAVIATE_HOST")

client = weaviate.connect_to_local(
    host=weaviate_host,
    port=weaviate_port,
)

## ----------- Database Connection and Database Management Tools ------------- ##

def get_db_connection():
    return psycopg2.connect(
        dbname="getSolar_crm",
        user="postgres",
        password="1029",
        host="host.docker.internal",
        port=5432
    )

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user/lead record by email and return it as a dict of all columns.
    """
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cur.fetchone()  # None or full dict
        return user
    finally:
        conn.close()

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user/lead record by its UUID and return it as a dict of all columns.
    """
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()
        return user
    finally:
        conn.close()

def create_user(
    id: str,
    name: str,
    email: str,
    phone: str = None,
    address: str = None,
    company: str = None,
    referral_source: str = None,
    budget: float = None,
    timeline_months: int = None,
    interest_level: str = None,
    requested_capacity: float = None,
    status: str = "new"
) -> Dict[str, Any]:
    """
    Create a new user/lead with all optional CRM fields.
    Returns the full user record as a dict.
    """
    # 1) Collect only the fields that are not None
    fields = {
        "id": id,
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "company": company,
        "referral_source": referral_source,
        "budget": budget,
        "timeline_months": timeline_months,
        "interest_level": interest_level,
        "requested_capacity": requested_capacity,
        "status": status
    }
    # Filter out None values
    insert_fields = {k: v for k, v in fields.items() if v is not None}

    # 2) Build the INSERT clause dynamically
    columns = ", ".join(insert_fields.keys())
    placeholders = ", ".join(f"%({k})s" for k in insert_fields.keys())

    sql = f"""
        INSERT INTO users ({columns})
        VALUES ({placeholders})
        RETURNING *
    """

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, insert_fields)
                user = cur.fetchone()  # returns a dict
        return user
    finally:
        conn.close()

def create_lead(user_id: str, status: str) -> Dict:
    """Create a new lead for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO leads (user_id, status) VALUES (%s, %s) RETURNING id, user_id, status, created_at",
        (user_id, status)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {
        "id": row[0],
        "user_id": row[1],
        "status": row[2],
        "created_at": row[3].isoformat() if row[3] else None
    }

def update_lead_status(lead_id: int, status: str) -> Optional[Dict]:
    """Update the status of a lead."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE leads SET status = %s WHERE id = %s RETURNING id, user_id, status, created_at",
        (status, lead_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row:
        return {
            "id": row[0],
            "user_id": row[1],
            "status": row[2],
            "created_at": row[3].isoformat() if row[3] else None
        }
    return None

## ----------- Qualifications Handling ------------- ##

def create_qualification(user_id: str, questions: List[str], responses: List[str], result: bool, evaluated_at: Optional[str] = None) -> Dict:
    """
    Create a new qualification record for a user.
    """

    conn = get_db_connection()
    cur = conn.cursor()
    q_json = json.dumps(questions)
    r_json = json.dumps(responses)
    sql = """
      INSERT INTO qualifications
        (user_id, questions, responses, result, evaluated_at)
      VALUES (%s, %s::jsonb, %s::jsonb, %s, %s)
      RETURNING id, user_id, questions, responses, result, evaluated_at
    """
    cur.execute(sql, (user_id, q_json, r_json, result, evaluated_at))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {
        "id": row[0],
        "user_id": row[1],
        "questions": row[2],
        "responses": row[3],
        "result": row[4],
        "evaluated_at": row[5].isoformat() if row[5] else None
    }

def update_qualification_based_on_user(user_id:str, qualification_status: str):
    """
    Update the qualification status of a user based on their ID.
    """

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET qualification_status = %s WHERE user_id = %s RETURNING id, user_id, questions, responses, result, evaluated_at",
        (qualification_status, user_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    if row:
        return {
            "id": row[0],
            "user_id": row[1],
            "questions": row[2],
            "responses": row[3],
            "result": row[4],
            "evaluated_at": row[5].isoformat() if row[5] else None
        }
    return None

def get_qualification_status(user_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT qualification_status FROM leads WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return row[0]
    return None


## ----------- Vector Search Retrieval ------------- ##

def vectorRetrieval(user_query: str, limit: int = 3) -> str:
    """
    Retrieves the most relevant context from a vector database containing a criteria document based on the user's query.
    """
    collection = client.collections.get(CRITERIA_COLLECTION_NAME)
    response = collection.query.hybrid(
        query = user_query,
        limit = limit
    )

    # 3) Pull out the “content” property
    chunks = []
    for obj in response.objects:
        # adjust this depending on your client:
        content = obj.properties.get("content")  
        if content:
            chunks.append(content)

    return "\n\n".join(chunks)


def assemble_context_from_form(form_data: dict) -> dict:
    """
    Assemble context for qualification question generation by combining form details
    with dynamically retrieved criteria.
    """
    # Construct a query from relevant form fields
    user_query = (
    f"Enquiry: (form_data.get('enquiry', '')). "
    f"Interest level: {form_data.get('interest_level', '')}. "
    f"Requested capacity: {form_data.get('requested_capacity', '')} kW. "
    f"Budget: SGD {form_data.get('budget', '')}. "
    f"Timeline: {form_data.get('timeline_months', '')} months."
)
    # Retrieve criteria as a string
    criteria_text = vectorRetrieval(user_query)
    # Assemble context as a dict
    context = {
        "user_details": form_data,
        "criteria": criteria_text
    }
    return context


## Mail Sending Tools
def send_questionnaire_email(
    recipient_email: str,
    recipient_name: str,
    questions: List[str],
    template_id: str = "x2p0347y3p74zdrn"
) -> Dict[str, Any]:
    """
    Sends a templated questionnaire email to a specific client.
    - recipient_email: destination email address
    - recipient_name: for personalization
    - questions: list of questions to inject into template
    - template_id: MailerSend template identifier
    """
    # 2) Build Personalization
    personalization = Personalization(
        to=recipient_email,
        variables={
            "name": recipient_name,        
            "questions": questions        
        }
    )

    # 3) Construct Template message
    template = Template(template_id=template_id)
    template.personalization = [personalization]  

    # 4) Send and return response
    response = mailer.send(template)             
    return response.json()