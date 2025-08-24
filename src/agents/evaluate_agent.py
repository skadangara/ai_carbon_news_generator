import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from src.core.logger import get_logger

# Load .env and init OpenAI client
load_dotenv()
client = OpenAI()
logger = get_logger("evaluate_agent")

# -----------------------------
# Score Format
# -----------------------------
class Score(BaseModel):
    score: int

# -----------------------------
# Evaluation Agent
# -----------------------------
def evaluate_summary(original_text, summary, model="gpt-4o", temperature=0.2):
    """
    Evaluate a summary against the original article based on clarity, completeness, and climate relevance.
    Returns a dict like: { "score": 9 }
    """
    try:
        prompt = f"""Evaluate this AI-generated summary for:
                1. Accuracy
                2. Completeness
                3. Relevance to climate regulations
                4. Clarity for climate experts

        ORIGINAL:
        {original_text[:3000]}

        SUMMARY:
        {summary}

        Give a score (1–10) and one-sentence feedback.
        Instructions:
        Give a score from 1 to 10 (only a number)
        """

        response = client.beta.chat.completions.parse(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            response_format=Score,  # Use Pydantic validation
        )

        parsed_result = response.choices[0].message.parsed.model_dump()
        logger.info(f"Evaluation returned: {parsed_result}")
        return parsed_result

    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        return {"score": "N/A"}
