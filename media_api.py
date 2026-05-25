import random
import time
import sqlite3
from datetime import datetime
from fastapi import FastAPI

app = FastAPI(
    title="Automated Media Intelligence & Telemetry Pipeline",
    description="Enterprise Multi-Source Content Analytics & Infrastructure Monitoring Engine",
    version="1.2.0"
)

DB_FILE = "pipeline_analytics.db"

def init_db():
    """Initializes the SQLite database and creates the historical logs table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trend_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            extracted_at TEXT,
            total_keywords INTEGER,
            top_keyword TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database immediately on startup
init_db()

MEDIA_SOURCES = {
    "Reuters": [
        "Global markets brace for shifting interest rates as inflation cools down",
        "Central banks coordinate monetary policy to stabilize international trade markets",
        "Investors pivot portfolios toward low-risk bonds amid global market fluctuations"
    ],
    "Bloomberg Technology": [
        "Tech giants invest billions in cloud infrastructure and hyperscale data centers",
        "Next-generation microchips drive massive expansion in enterprise computing power",
        "Cloud infrastructure spending hits record highs as global enterprise demands scale"
    ],
    "TechCrunch": [
        "Silicon Valley startups secure massive venture capital funding for breakthrough AI models",
        "Venture capital firms shift focus toward profitable tech startups in latest funding round",
        "Emerging tech startups disrupt traditional software markets with agile product releases"
    ],
    "Wired": [
        "Cyber security experts warn of sophisticated phishing threats targeting critical infrastructure",
        "New cyber security frameworks implemented globally to protect sensitive consumer data",
        "Emerging quantum encryption technologies revolutionize enterprise cyber security protocols"
    ],
    "Techpoint Africa": [
        "African fintech startups drive massive digital inclusion across regional ecosystems",
        "Digital transformation accelerates across sub-Saharan tech hubs as connectivity expands",
        "Fintech growth and local tech talent positioning Nigeria as a premier digital innovation hub"
    ],
    "Business Day": [
        "Regional economic policy undergoes strategic restructuring to attract foreign direct investment",
        "Macro-economic stability becomes primary target for regional financial regulators",
        "New fiscal policy frameworks aiming to drive industrial growth and long-term economic expansion"
    ]
}

def process_text_analytics(source_name: str):
    articles = MEDIA_SOURCES.get(source_name, [])
    combined_text = " ".join(articles).lower()
    all_words = combined_text.split()
    
    noise_words = {
        "the", "and", "for", "to", "as", "with", "in", "of", "a", "an", 
        "is", "are", "on", "by", "at", "across", "toward", "amid", "its", "their"
    }
    
    cleaned_keywords = [word for word in all_words if word not in noise_words]
    
    frequency_map = {}
    for word in cleaned_keywords:
        word = word.strip(",.()")
        if word:
            frequency_map[word] = frequency_map.get(word, 0) + 1
            
    sorted_trends = dict(sorted(frequency_map.items(), key=lambda item: item[1], reverse=True))
    return sorted_trends

@app.get("/")
def root():
    return {"status": "online", "pipeline": "Media Intelligence Engine with SQL Persistence"}

@app.get("/api/trends")
def get_media_trends(source: str = "Reuters"):
    if source not in MEDIA_SOURCES:
        source = "Reuters"
        
    trends = process_text_analytics(source)
    extracted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_keywords = sum(trends.values())
    
    top_keyword = list(trends.keys())[0] if trends else "None"
    
    # SQL INSERTION LAYER
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trend_logs (source, extracted_at, total_keywords, top_keyword)
        VALUES (?, ?, ?, ?)
    """, (source, extracted_at, total_keywords, top_keyword))
    conn.commit()
    conn.close()
    
    return {
        "source": source,
        "extracted_at": extracted_at,
        "total_keywords_processed": total_keywords,
        "trending_topics": trends
    }

@app.get("/api/history")
def get_pipeline_history():
    """Executes a SQL query to fetch the latest 10 data extraction logs."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT source, extracted_at, total_keywords, top_keyword FROM trend_logs ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "Source": row[0],
            "Execution Timestamp": row[1],
            "Total Keywords Logged": row[2],
            "Top Trending Word": row[3]
        })
    return history

@app.get("/api/analytics")
def get_db_metrics():
    """New Endpoint: Runs advanced SQL aggregations for metrics reporting."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Calculate cumulative keywords processed
    cursor.execute("SELECT SUM(total_keywords) FROM trend_logs")
    total_volume = cursor.fetchone()[0] or 0
    
    # 2. Find the most audited media source
    cursor.execute("SELECT source, COUNT(source) as cnt FROM trend_logs GROUP BY source ORDER BY cnt DESC LIMIT 1")
    top_source_row = cursor.fetchone()
    top_source = top_source_row[0] if top_source_row else "None"
    
    # 3. Find the most reoccurring top keyword
    cursor.execute("SELECT top_keyword, COUNT(top_keyword) as cnt FROM trend_logs GROUP BY top_keyword ORDER BY cnt DESC LIMIT 1")
    top_word_row = cursor.fetchone()
    dominant_keyword = top_word_row[0] if top_word_row else "None"
    
    conn.close()
    
    return {
        "cumulative_keywords": total_volume,
        "most_active_source": top_source,
        "dominant_trend_keyword": dominant_keyword
    }

@app.get("/api/telemetry")
def get_system_telemetry():
    return {
        "infrastructure_status": "Healthy",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "network_throughput_mbps": round(random.uniform(15.4, 88.9), 2),
        "server_latency_ms": round(random.uniform(35.0, 115.5), 1),
        "system_memory_utilization": round(random.uniform(42.1, 68.5), 1),
        "active_concurrent_sessions": random.randint(3, 15)
    }