import os
import logging
from langgraph.graph import StateGraph
from src.core.schema import AgentState
from src.agents.search_agent import search_google_news
from src.agents.summarize_agent import extract_text, summarize
from src.agents.evaluate_agent import evaluate_summary
from src.core.logger import get_logger

# -----------------------------
# Logger Setup
# -----------------------------
logger = get_logger("graph")

# -----------------------------
# Agent: Search
# -----------------------------
def search_agent(state):
    topic = state["topic"]
    logger.info(f"[Search Agent] Searching news for topic: {topic}")
    articles = []

    try:
        for result in search_google_news(topic):
            title, text = extract_text(result["url"])
            articles.append({
                "title": title,
                "content": text,
                "source": result["source"],
                "url": result["url"]
            })
        logger.info(f"[Search Agent] Found {len(articles)} articles for topic: {topic}")
    except Exception as e:
        logger.error(f"[Search Agent] Error during search: {e}")

    state["articles"] = articles
    return state

# -----------------------------
# Agent: Summarize
# -----------------------------
def summarize_agent(state):
    logger.info(f"[Summarize Agent] Summarizing {len(state['articles'])} articles")
    summaries = []

    try:
        for a in state["articles"]:
            summary = summarize(a["content"])
            summaries.append({**a, "summary": summary})
        logger.info(f"[Summarize Agent] Completed summaries")
    except Exception as e:
        logger.error(f"[Summarize Agent] Error during summarization: {e}")

    state["summaries"] = summaries
    return state

# -----------------------------
# Agent: Evaluate
# -----------------------------
def evaluate_agent(state):
    logger.info(f"[Evaluate Agent] Evaluating {len(state['summaries'])} summaries")
    evaluated = []

    try:
        for a in state["summaries"]:
            score = evaluate_summary(a["content"], a["summary"])
            evaluated.append({**a, "evaluation": score})
        logger.info(f"[Evaluate Agent] Completed evaluations")
    except Exception as e:
        logger.error(f"[Evaluate Agent] Error during evaluation: {e}")

    state["evaluated"] = evaluated
    return state

# -----------------------------
# Build LangGraph
# -----------------------------
def build_graph():
    logger.info(" Building LangGraph pipeline")
    graph = StateGraph(AgentState)

    graph.add_node("search", search_agent)
    graph.add_node("summarize", summarize_agent)
    graph.add_node("evaluate", evaluate_agent)

    graph.set_entry_point("search")
    graph.add_edge("search", "summarize")
    graph.add_edge("summarize", "evaluate")
    graph.set_finish_point("evaluate")

    logger.info("LangGraph pipeline compiled")
    return graph.compile()
