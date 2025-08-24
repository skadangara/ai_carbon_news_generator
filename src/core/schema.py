from typing import TypedDict, List, Dict


# ----------------------------------
# Shared Agent State across Graph
# ----------------------------------
class AgentState(TypedDict):
    topic: str
    articles: List[Dict]
    summaries: List[Dict]
    evaluated: List[Dict]