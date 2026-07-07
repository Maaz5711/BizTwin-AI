# BizTwin
## The AI Business Digital Twin

> **An Enterprise AI Command Center that creates an intelligent digital twin of your business, enabling executives to simulate decisions, analyze operations, and receive AI-powered recommendations before making real-world changes.**

![Status](https://img.shields.io/badge/Status-Hackathon-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![AMD](https://img.shields.io/badge/Powered%20By-AMD-red)

---

# Overview

Modern businesses generate enormous amounts of operational data, yet many important decisions are still made using spreadsheets, intuition, and manual analysis.

Questions like:

- Should we hire another salesperson?
- What happens if supplier costs increase?
- Which products should be discontinued?
- Why is profit declining?
- Which department needs immediate attention?

often require analysts, accountants, and hours of manual work.

**BizTwin** solves this by creating a **Digital Twin** of a business and combining it with a collaborative **Multi-Agent AI Executive Team**.

Business owners simply upload their operational data and ask questions in natural language.

BizTwin analyzes the data, simulates future scenarios, calculates financial impact, and provides executive-level recommendations backed by real business numbers.

Built for the **AMD Developer Hackathon 2026 – Unicorn Track**.

---

# Problem

Small and medium-sized businesses often lack access to expensive Business Intelligence platforms and dedicated analysts.

Decision makers struggle to:

- Understand operational performance
- Forecast business outcomes
- Detect hidden risks
- Evaluate strategic decisions
- Convert raw data into actionable insights

---

# Our Solution

BizTwin creates a digital representation of a company using operational data including:

- Sales
- Products
- Inventory
- Suppliers
- Employees
- Expenses

The platform then allows users to interact with their business using conversational AI.

Instead of reading spreadsheets...

Ask:

> "What happens if Supplier A increases prices by 15%?"

or

> "Is hiring two additional salespeople profitable?"

BizTwin performs the calculations, runs simulations, and explains the outcome.

---

# Core Features

## Business Twin Creation

Upload CSV or Excel files to automatically create a digital representation of your business.

Supports:

- Sales
- Inventory
- Products
- Suppliers
- Employees

---

## AI Business Chat

Interact with your business using natural language.

Example questions:

- Why did profits decrease?
- Which products perform best?
- Which supplier is increasing costs?
- What should I prioritize next?

---

## What-If Scenario Simulation

Current MVP includes:

### Supplier Price Increase

Predict:

- Profit impact
- Margin changes
- Affected products

---

### Hiring Analysis

Estimate:

- Salary costs
- Revenue growth
- ROI

---

### Product Discontinuation

Evaluate:

- Lost revenue
- Saved expenses
- Net profitability

---

## Executive Dashboard

Interactive analytics including:

- Revenue
- Profit
- Expenses
- Inventory
- Supplier insights
- Before vs After comparisons
- KPI cards
- Charts

---

## Explainable AI

Business calculations always come from uploaded data.

The AI never invents numbers.

Every recommendation includes an explanation.

---

# AI Multi-Agent Architecture

Instead of relying on a single AI model, BizTwin uses a team of specialized AI agents that collaborate like an executive board.

Each agent focuses on a specific business domain and reports its findings to the Executive Agent.

---

## Executive Agent

The brain of BizTwin.

Responsibilities:

- Understand user intent
- Coordinate all agents
- Combine insights
- Generate executive summaries
- Recommend strategic actions

---

## Sales Intelligence Agent

Analyzes business growth.

Responsibilities:

- Revenue analysis
- Sales trends
- Product performance
- Customer purchasing insights

---

## Finance Agent

Monitors financial health.

Responsibilities:

- Profit calculation
- Expense analysis
- Margin optimization
- Cost anomalies

---

## Inventory Agent

Optimizes inventory operations.

Responsibilities:

- Overstock detection
- Low-stock alerts
- Dead inventory
- Restocking suggestions

---

## Supplier Intelligence Agent

Analyzes procurement performance.

Responsibilities:

- Supplier comparison
- Price monitoring
- Vendor risks
- Procurement optimization

---

## Scenario Simulation Agent

The predictive engine of BizTwin.

Runs business simulations including:

- Supplier price increase
- Hiring employees
- Product discontinuation

Calculates:

- Revenue impact
- Cost impact
- Profit impact
- Business risk

---

## Risk Analysis Agent

Continuously evaluates business health.

Responsibilities:

- Detect anomalies
- Identify profit leaks
- Operational risks
- Financial impact estimation

---

## Analytics Agent

Transforms raw business data into executive insights.

Responsibilities:

- KPI generation
- Dashboard metrics
- Trend analysis
- Business summaries

---

# Agent Collaboration

```
                          User
                            │
                            ▼
                  Executive Agent
                            │
     ┌─────────┬─────────┬─────────┬──────────┬──────────┐
     ▼         ▼         ▼         ▼          ▼
 Sales     Finance   Inventory  Supplier   Risk
 Agent       Agent      Agent      Agent     Agent
                            │
                            ▼
                 Scenario Simulation Agent
                            │
                            ▼
                Executive Recommendation
```

---

# Architecture

```
                React Frontend
                       │
                       ▼
                 FastAPI Backend
                       │
               Business Twin Engine
                       │
               AI Orchestrator
                       │
     ┌─────────┬──────────┬─────────┐
     ▼         ▼          ▼
 Business   Simulation  Analytics
   Data       Engine
                       │
                       ▼
        Fireworks AI + AMD Open Models
                       │
                       ▼
            AMD Developer Cloud GPUs
```

---

# Technology Stack

## Frontend

- React
- TypeScript
- Tailwind CSS
- Recharts

## Backend

- FastAPI
- Python

## AI

- Fireworks AI
- LangGraph
- Open-source LLMs
- Prompt Engineering

## Data

- Pandas
- PostgreSQL
- ChromaDB (Future)

## Infrastructure

- AMD Developer Cloud
- Docker
- Docker Compose

---

# AMD Technologies Used

BizTwin is built using AMD's AI ecosystem.

- AMD Developer Cloud for GPU-powered model execution
- Fireworks AI for LLM inference
- Open-source models running on AMD GPUs
- Docker for containerized deployment

---

# Example Workflow

```
Upload Business Data
        │
        ▼
Create Business Digital Twin
        │
        ▼
Ask Business Question
        │
        ▼
AI Agents Analyze Business
        │
        ▼
Run Financial Simulation
        │
        ▼
Generate Executive Recommendation
        │
        ▼
Interactive Dashboard
```

---

# Example Questions

- What happens if supplier prices increase by 15%?
- Should we hire two more salespeople?
- Which products are reducing profitability?
- Predict next month's revenue.
- Which supplier has the greatest financial impact?
- Summarize this month's business performance.

---

# Project Structure

```
BizTwin/

├── frontend/
├── backend/
├── docker/
├── docs/
├── sample-data/
├── assets/
├── README.md
├── docker-compose.yml
└── LICENSE
```

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/<your-username>/biztwin-ai.git
```

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

## Docker

```bash
docker compose up --build
```

---

# Future Roadmap

- Predictive demand forecasting
- AI-generated executive reports
- Voice-enabled business assistant
- ERP & accounting software integrations
- Autonomous AI workflows
- Multi-company management
- Mobile application
- Real-time business monitoring

---

# Team

Developed by students from **FAST National University** for the **AMD Developer Hackathon 2026**.

---

# Why BizTwin?

BizTwin combines the concept of a **Business Digital Twin** with an **AI Executive Team**, allowing organizations to test decisions virtually before committing resources in the real world.

Our vision is to make enterprise-grade business intelligence accessible to every business through collaborative AI.

---

# License

MIT License
