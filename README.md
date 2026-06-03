# 5 Whys Analyzer

Open-source root cause analysis toolkit for teams using the 5 Whys method.

5 Whys Analyzer helps teams investigate incidents, recurring problems, customer escalations, and operational failures through a structured root-cause-analysis workflow. It is designed to run locally, support privacy-conscious teams, and produce reports that can be shared in GitHub, Jira, Slack, Notion, Confluence, or internal postmortem documents.

## Why this exists

Many teams handle incidents informally. Important context gets lost, corrective actions are unclear, and the same problems return. 5 Whys Analyzer helps teams turn a problem into a structured investigation, root cause, and action plan.

## Use cases

- Software incident postmortems
- DevOps and infrastructure failures
- Customer support escalations
- Internal operations issues
- Process improvement
- Manufacturing or quality investigations
- Security retrospectives

## Features

Current:

- Flask-based web interface
- Guided 5 Whys analysis
- Local LLM support through Ollama
- Simple browser-based workflow

Planned:

- Structured RCA reports
- Markdown and JSON exports
- SQLite persistence
- Docker setup
- GitHub/Jira/Slack-ready report formats
- Tests and CI
- Example reports and templates

## Quickstart

### Prerequisites

- Python 3.10+
- Ollama installed locally
- A local model such as llama3

### Install

```bash
git clone https://github.com/Mohit-Gajula/5_Whys_Analyzer.git
cd 5_Whys_Analyzer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt