
# Project Title

AI-powered automated Carbon accounting news generator.


## Project Summary

This project automates the process of discovering and summarizing carbon accounting related news. It delivers a concise daily overview of key developments to climate experts.

The system is built using a multi-agent architecture powered by GPT-4o and the LangGraph framework.

Agents

search_agent → Fetches carbon-related news from the web via Google RSS feeds and scrapes raw article content.

summarize_agent → Generates concise summaries from the raw content.

evaluate_agent → Compares each summary with the original content and assigns a quality score (1–10). A higher score indicates better accuracy, completeness, and clarity.

This ensures experts receive reliable, high-quality, and actionable news updates every day.
## Prerequisites

1. Install necessary libraries from the requirements.txt file.
2. Set your OpenAI key in env file.
3. Python (version=3.9+)
4. pip package manager
## Setup

1. Extract the source code and navigate to the root folder.
cd ai_carbon_news_generator

2. Install requirement using below command.
pip install -r requirements.txt

3. Run the app using below command.
python src/main.py

4. Output
The generated news will be saved to the "data" folder 



## Tools & Technologies

Programming Language: Python

LLM: GPT-4o (OpenAI)

Framework: LangGraph

Web Scraping: BeautifulSoup, Playwright
## Demo Output

Sample outputs are available in the data/ folder.

Currently, the output is generated in Markdown (.md) format, but it can also be exported to PDF, JSON, or XML.

Each generated news summary includes the following sections:

Title

Source

Summary

Evaluation Score (1–10)

Read More → link to the full article


## Authors

- [@skadangara](https://github.com/skadangara)


## License

Sajana Kadangara

