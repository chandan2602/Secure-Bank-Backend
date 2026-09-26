import os

from dotenv import load_dotenv

from groq import Groq

from retriever import retrive_data

from schemas import QuestionRequest

from database import execute_query

from fastapi import APIRouter, HTTPException


# =====================================================
# Configuration
# =====================================================

load_dotenv()


router = APIRouter(
    prefix="/Rag",
    tags=["Rag chatbot"]
)


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


client = Groq(
    api_key=GROQ_API_KEY
)


# =====================================================
# 1. Generate SQL
# =====================================================

def generate_sql(
    question: str,
    context: str
):

    prompt = f"""
You are a PostgreSQL SQL expert for a Secure Bank system.

Use ONLY the database schema provided below.

DATABASE SCHEMA:

{context}

User Question:

{question}

RULES:

1. Generate ONLY a SELECT query.
2. Do not generate INSERT.
3. Do not generate UPDATE.
4. Do not generate DELETE.
5. Do not generate DROP.
6. Do not generate ALTER.
7. Never select user_password.
8. Never select passwords, tokens, API keys or secrets.
9. Use the exact table and column names from the schema.
10. The interest rate column is "intrest_rate".
11. Return ONLY the SQL query.
12. Do not use markdown code blocks.
13. Do not explain the SQL.
14. Do not return any text other than the SQL query.

SQL:
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    sql = response.choices[0].message.content.strip()


    return sql


# =====================================================
# 2. Generate final answer
# =====================================================

def generate_answer(
    question: str,
    database_result
):

    prompt = f"""
You are a helpful assistant for a Secure Bank system.

User Question:

{question}

Database Result:

{database_result}

Rules:

1. Answer using ONLY the database result.
2. Do not invent information.
3. Do not expose passwords or authentication credentials.
4. Give a clear and simple answer.
5. If the database result is empty, say:

"I don't have that information."

Answer the user's question directly and concisely.
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    return response.choices[0].message.content.strip()


# =====================================================
# 3. FastAPI endpoint
# =====================================================

@router.post("/ask")
def ask_question(
    request: QuestionRequest
):

    question = request.question


    try:

        # ------------------------------------------------
        # STEP 1: Retrieve database schema
        # ------------------------------------------------

        context = retrive_data(
            question,
            top_k=3
        )


        print(
            "\n========== RETRIEVED CONTEXT =========="
        )

        print(context)


        # ------------------------------------------------
        # STEP 2: Make sure context exists
        # ------------------------------------------------

        if not context:

            raise HTTPException(
                status_code=404,
                detail="No relevant database schema found."
            )


        # ------------------------------------------------
        # STEP 3: Generate SQL
        # ------------------------------------------------

        sql = generate_sql(
            question,
            context
        )


        print(
            "\n========== GENERATED SQL =========="
        )

        print(sql)


        # ------------------------------------------------
        # STEP 4: Validate SQL
        # ------------------------------------------------

        sql_clean = sql.strip()


        # Remove markdown code blocks if model somehow
        # returns them

        if sql_clean.startswith("```"):

            sql_clean = sql_clean.replace(
                "```sql",
                ""
            )

            sql_clean = sql_clean.replace(
                "```",
                ""
            )

            sql_clean = sql_clean.strip()


        # Only SELECT queries allowed

        if not sql_clean.lower().startswith(
            "select"
        ):

            raise HTTPException(
                status_code=400,
                detail={
                    "message":
                        "LLM did not generate a valid SELECT query",

                    "generated_output":
                        sql
                }
            )


        # ------------------------------------------------
        # STEP 5: Execute SQL
        # ------------------------------------------------

        database_result = execute_query(
            sql_clean
        )


        print(
            "\n========== DATABASE RESULT =========="
        )

        print(database_result)


        # ------------------------------------------------
        # STEP 6: Generate final answer
        # ------------------------------------------------

        answer = generate_answer(
            question,
            database_result
        )


        print(
            "\n========== FINAL ANSWER =========="
        )

        print(answer)


        # ------------------------------------------------
        # STEP 7: Return response
        # ------------------------------------------------

        return {

            "question": question,

            "sql": sql_clean,

            "database_result":
                database_result,

            "answer":
                answer
        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )