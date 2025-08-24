import json
import os
import logging
from datetime import date
from src.core.logger import get_logger

# -----------------------------
# 🔧 Logger Setup
# -----------------------------
logger = get_logger("formatter")

# -----------------------------
# Markdown Formatter
# -----------------------------
def format_digest(items):
    """
    Format a list of evaluated news items into a Markdown-formatted digest.

    Each item should contain:
    - title
    - source
    - summary
    - evaluation (optional dict with 'score' and optionally 'feedback')
    - url
    """
    logger.info(f"📝 [Formatter] Formatting {len(items)} articles into digest")

    lines = [f"# 📰 Carbon Accounting News Digest — {date.today().isoformat()}\n"]

    for i, item in enumerate(items, start=1):
        try:
            title = item.get("title", "Untitled")
            source = item.get("source", "Unknown Source")
            summary = item.get("summary", "No summary available.")
            url = item.get("url", "#")

            evaluation = item.get("evaluation", {})
            score = evaluation.get("score", "N/A")
            feedback = evaluation.get("feedback", None)

            lines.append(f"## {title}\n")
            lines.append(f"*Source*: {source}\n")
            lines.append(f"{summary}\n")
            lines.append(f"**Evaluation Score**: {score}/10")
            if feedback:
                lines.append(f"**Evaluator Feedback**: {feedback}")
            lines.append(f"[🔗 Read more]({url})\n")
            lines.append("---\n")

        except Exception as e:
            logger.error(f"❌ [Formatter] Error formatting item #{i}: {e}")
            continue

    logger.info("✅ [Formatter] Digest formatting complete")
    return "\n".join(lines)
