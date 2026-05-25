# 🛡️ Automated Media Intelligence & Telemetry Pipeline

An enterprise-grade, decoupled full-stack data pipeline designed to automate unstructured content ingestion, clean text streams, and monitor distributed infrastructure telemetry with persistent relational logging.

---

## 🏗️ Architecture Overview

The platform uses a decoupled microservices-inspired architecture consisting of three core layers:

1. **Frontend Layer (`media_ui.py`)**: Built with **Streamlit**, featuring a highly customized enterprise dark-mode UI, responsive data frames, and interactive plotting mechanics.
2. **Transport & API Layer (`media_api.py`)**: Powered by **FastAPI** running on a high-velocity, asynchronous **Uvicorn** ASGI server to manage secure RESTful endpoints.
3. **Data Persistence Layer (`pipeline_analytics.db`)**: Powered by an embedded **SQLite** relational engine to track real-time processing audit trails and historical execution logs.

---

## 🚀 Key Functional Features

### 1. Multi-Source Content Intelligence
* Automated analysis across 6 industry-standard target media streams (including *Reuters*, *Bloomberg Technology*, and *Techpoint Africa*).
* A specialized text-processing algorithm that strips structural noise and conversational filler words on the fly to isolate and chart maximum-frequency keywords.

### 2. Infrastructure Telemetry Streaming
* Live network and system metrics simulation modeling real-world performance under constraint.
* Captures and tracks key production health signals: Network Throughput (Mbps), Server Latency (ms), and System Memory Utilization.

### 3. Relational SQL Accountability Audit
* Production-ready database schema tracking every content-ingestion lifecycle event.
* A live administrative control center executing complex backend `SELECT` statements to query real-time audit logs directly on the user interface.

---

## 🛠️ Technology Stack & Frameworks

* **Language**: Python 3
* **Backend Framework**: FastAPI
* **Web Server Engine**: Uvicorn (ASGI)
* **Frontend UI**: Streamlit / Custom CSS Injection
* **Database Engine**: SQLite3
* **Network Protocol**: RESTful API / JSON Exchange (`requests`)

---

## 💻 Local Installation & Deployment Guide

To deploy this pipeline locally or inside your containerized environment, execute the following commands in your terminal:

### 1. Clone the repository and navigate to the project directory
```bash
cd 02_media_intelligence_pipeline