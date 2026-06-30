# News Hunter

An AI-powered news intelligence platform that collects, analyzes, summarizes, and distributes technology and AI news using FastAPI, Docker, PostgreSQL, n8n, and Large Language Models.

## Overview

News Hunter automatically:

- Collects news from multiple RSS feeds
- Stores articles in PostgreSQL
- Uses AI to summarize and categorize articles
- Detects duplicate stories
- Generates newsletters
- Automates workflows with n8n

---

## Tech Stack

### Backend
- FastAPI
- Python 3.11

### Database
- PostgreSQL
- SQLAlchemy
- Alembic

### AI
- OpenAI API
- NVIDIA NIM
- Ollama (optional)

### Automation
- n8n

### Infrastructure
- Docker
- Docker Compose
- Oracle Cloud

---

## Architecture

Internet
        │
        ▼
FastAPI
        │
        ▼
PostgreSQL
        │
        ▼
AI Processing
        │
        ▼
n8n Workflows
        │
        ▼
Newsletter / Discord / Email

---

## Project Structure

```
news-hunter/
│
├── app/
├── data/
├── docs/
├── docker/
├── scripts/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Current Features

- FastAPI Backend
- Docker Deployment
- Health API
- Oracle Cloud Deployment

---

## Planned Features

- PostgreSQL Integration
- RSS Feed Collection
- AI Summarization
- Semantic Search
- Newsletter Generator
- n8n Automation
- Authentication
- Admin Dashboard

---

## Author

Dhruv Bhavsar