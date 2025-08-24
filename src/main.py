import os
import logging
from datetime import datetime
from src.core.graph import build_graph
from src.core.formatter import format_digest
from src.core.logger import get_logger
import warnings

warnings.filterwarnings("ignore")

# -----------------------------
# Logging Setup
# -----------------------------
logger = get_logger("main")

# -----------------------------
# Topics to Track
# -----------------------------
TOPICS = [
    "carbon accounting standards",
    "GHG Protocol update",
    "CSRD climate disclosure",
    "FASB environmental credit rules"
]

# -----------------------------
# Main Pipeline
# -----------------------------
def main():
    logger.info("Carbon news extraction and summarization started")
    print("Fetching Carbon related news...")
    start_time = datetime.now()

    all_summaries = []
    graph = build_graph()

    for topic in TOPICS:
        logger.info(f"Processing topic: '{topic}'")
        try:
            final_state = graph.invoke({"topic": topic})
            evaluated = final_state.get("evaluated", [])
            logger.info(f"Retrieved {len(evaluated)} evaluated summaries")
            all_summaries.extend(evaluated)
        except Exception as e:
            logger.error(f"Error processing topic '{topic}': {e}")

    # Format the markdown digest
    digest = format_digest(all_summaries)

    # Write output to markdown file
    digest_path = "data/carbon_news_" + datetime.today().strftime('%Y-%m-%d') + ".md"
    with open(digest_path, "w", encoding="utf-8") as f:
        f.write(digest)

    logger.info(f"Digest written to {digest_path}")
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Completed in {duration:.2f} seconds")

    print(f"Carbon news written to {digest_path}")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
