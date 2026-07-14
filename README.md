# BizTwin — AI Business Digital Twin

![Status](https://img.shields.io/badge/Status-Hackathon-blue)![Python](https://img.shields.io/badge/Python-3.11-green)![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)![React](https://img.shields.io/badge/React-Frontend-blue)![AMD](https://img.shields.io/badge/Powered%20By-AMD-red)

> Ask your business what happens next — before it happens.

BizTwin is an AI-powered Business Digital Twin that lets small and medium-sized business owners upload their operational spreadsheets and simulate decisions — supplier changes, hiring, product discontinuation — in plain English, before committing real money to them.

Built for the AMD AI Hackathon.

**Live Demo:** [https://biz-twin-ai.vercel.app](https://biz-twin-ai.vercel.app)

> **Note:** During the AMD Developer Hackathon, BizTwin initially used Fireworks AI for LLM inference on AMD Developer Cloud. After the temporary hackathon API credits expired, the AI layer was migrated to Google's Gemini API for continued development and deployment. The underlying business simulation engine remains unchanged, and all financial calculations continue to be performed deterministically using the uploaded business data.

---

## Table of Contents

- [Overview](#overview)
- [Problem](#problem)
- [Solution](#solution)
- [How It Works](#how-it-works)
- [Core Features](#core-features)
- [Why AI](#why-ai)
- [Why AMD](#why-amd)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Team](#team)
- [License](#license)

---

## Overview

Most small businesses generate real operational data — sales, inventory, supplier costs, employee expenses — but that data sits scattered across spreadsheets and is rarely used for actual decision-making. Business owners typically decide whether to switch suppliers, hire staff, or drop a product based on intuition, because advanced business intelligence tooling is too expensive, too technical, or built for enterprises with dedicated data teams.

BizTwin closes that gap. It turns a business's spreadsheets into a structured digital twin, then lets the owner interact with it conversationally — asking questions like *"What happens if Supplier A increases prices by 15%?"* or *"Should I hire two more sales reps?"* — and get back a data-grounded simulation of the outcome, explained in plain language, with a clear before-and-after comparison.

---

## Problem

Small and medium-sized businesses face:

- Reduced profitability due to poor supplier decisions
- Overstocking or understocking inventory
- Unnecessary hiring costs
- Difficulty identifying low-performing products
- Hours spent manually analyzing spreadsheets
- Limited access to affordable, usable business intelligence tools

Current analytics platforms are expensive, require technical expertise, or are designed for large enterprises — leaving most SMBs without a practical way to test decisions before making them.

---

## Solution

BizTwin creates an AI-powered digital twin of a business from uploaded spreadsheets. Instead of manually analyzing data, the owner uploads sales, inventory, supplier, and employee information, and BizTwin processes it into a unified business model. The owner can then ask questions in plain English; a simulation engine performs the actual financial calculations on the real uploaded data, while an AI assistant explains the results in accessible language and presents visual comparisons — letting the owner evaluate a decision before spending real money on it.

---

## How It Works

1. **Upload Business Data** — sales, products, inventory, suppliers, and employee spreadsheets (CSV/Excel).
2. **Create Digital Twin** — BizTwin combines all uploaded data into one structured model of the business.
3. **Ask Questions** — the owner interacts naturally: *"Which supplier affects my profits the most?"*, *"Should I hire two sales employees?"*
4. **Simulation** — the simulation engine runs the scenario against the real business data.
5. **AI Explanation** — the AI assistant explains the financial impact, business implications, recommended actions, and supporting visualizations.

The AI never generates financial values itself — all numerical calculations are performed by the simulation engine using the business's actual data. The AI's role is limited to understanding the question, triggering the right simulation, and explaining the result.

---

## Core Features

- **Business Data Upload** — CSV/Excel ingestion for sales, inventory, suppliers, and employees
- **Business Digital Twin** — a structured digital representation of the company's operations
- **AI Business Assistant** — natural language interface to the twin
- **Interactive Dashboard** — revenue, profit, inventory, employees, supplier info, and KPIs at a glance
- **Scenario Simulation** — supplier price increases, hiring costs, and product discontinuation
- **Before vs. After Comparison** — visual comparison of business metrics for every simulated decision

---

## Why AI

Traditional business intelligence platforms require users to understand dashboards, filters, reports, and SQL. BizTwin removes that barrier by letting users interact in natural language. AI is used to:

- Understand business questions
- Identify the requested scenario
- Interpret simulation results
- Explain complex financial outcomes in simple language
- Improve accessibility for non-technical users

All numbers come from the simulation engine, not the AI — this keeps BizTwin trustworthy for real financial decisions rather than being a purely generative tool.

The production deployment currently uses Google's Gemini API for natural language understanding and business explanations, while the original hackathon prototype used Fireworks AI during development on AMD Developer Cloud.


---


## Why AMD

BizTwin was originally developed during the AMD Developer Hackathon using AMD Developer Cloud and Fireworks AI for rapid LLM prototyping and testing.

Following the hackathon, the conversational AI layer was migrated to Google's Gemini API for the live deployment after the temporary Fireworks API credits expired. This demonstrates BizTwin's model-agnostic architecture, allowing different large language models to power the conversational interface while the deterministic business simulation engine continues to perform all financial calculations using real uploaded business data.

The project demonstrates how AI-powered business decision support can be built on AMD technologies while remaining flexible enough to switch LLM providers without changing the underlying business logic.

---

## Architecture

```
┌─────────────────────┐     ┌──────────────────────┐     ┌────────────────────────┐
│   Data Upload        │────▶│   Digital Twin        │────▶│   Simulation Engine     │
│  (CSV / Excel)       │     │  (structured model)   │     │ (deterministic math)    │
└─────────────────────┘     └──────────────────────┘     └────────────┬───────────┘
                                                                       │
                                                                       ▼
┌─────────────────────┐     ┌──────────────────────┐     ┌────────────────────────┐
│ │   Interactive         │◀───│   AI Explanation      │◀───│   Simulation Result     │
│   Dashboard           │     │ (Google Gemini API)  │     │   (before vs. after)    │
└─────────────────────┘     └──────────────────────┘     └────────────────────────┘
```

The AI layer and the simulation engine are deliberately separated: the AI interprets natural language and explains outcomes, while all financial math is computed deterministically from the business's real uploaded data.

---

## Tech Stack

- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** FastAPI
- **AI Layer:** Google Gemini API (Gemini 3.5 Flash)
- **Data Processing:** Pandas, NumPy
- **Hosting:** Vercel (Frontend), Render (Backend API)
- **AI Infrastructure:** AMD Developer Cloud (Hackathon Development), Fireworks AI (Initial LLM Prototyping), Google Gemini API (Production Deployment)

---

## Usage

> Installation and Docker setup instructions are provided separately below this section.

Once running, the typical usage flow is:

1. Open the BizTwin web app.
2. Upload your business spreadsheets (sales, inventory, suppliers, employees).
3. Wait for BizTwin to build your digital twin and populate the dashboard.
4. Ask a business question in the chat interface, e.g.:
   - "What happens if Supplier A increases prices by 15%?"
   - "Should I hire two additional sales representatives?"
   - "Which products are reducing my profits?"
5. Review the simulation result: financial impact, explanation, and before/after comparison on the dashboard.

---

## Roadmap

Future versions of BizTwin could include:

- ERP integration
- Shopify integration
- QuickBooks integration
- Real-time inventory synchronization
- Sales forecasting
- Demand prediction using machine learning
- Supplier recommendation engine
- Multi-branch business support
- Financial forecasting
- Mobile application
- Multi-user collaboration
- Automated reporting

---

## Team

- **Huzaifa Khalid**
- **Hamza Shehryar**
- **Muhammad Bilal**
- **Maaz Ahmed**

---

## License

This project is licensed under the [MIT License](LICENSE).
