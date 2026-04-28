# Mini Braze CRM + Personalization Engine

This project simulates a lightweight Braze-style customer engagement workflow for interview demonstration.

## What It Demonstrates

- Event ingestion similar to Braze SDK / REST API
- User attribute and event schema design
- Identity resolution between device IDs and account/user IDs
- SQL-based user segmentation
- Reverse ETL simulation similar to Hightouch
- Liquid-style message personalization
- A/B testing assignment
- CRM journey logic similar to Braze Canvas
- Reporting dashboard using Streamlit

## Tech Stack

- Python
- Pandas
- SQLite SQL
- Streamlit
- Jinja2 template engine to simulate Liquid-style personalization
- Local CSV/JSON data to simulate warehouse and CRM sync

## Project Structure

```text
mini_braze_crm_project/
│
├── data/
│   ├── users.csv
│   ├── events.json
│   └── device_identity_map.csv
│
├── output/
│   ├── unified_events.csv
│   ├── user_segments.csv
│   ├── braze_reverse_etl_payload.json
│   └── personalized_messages.csv
│
├── app.py
├── pipeline.py
├── templates.py
├── requirements.txt
└── demo_script.md
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python pipeline.py
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

## Interview Explanation

“I built a mini customer engagement platform that simulates how Braze works end-to-end. It ingests user events, resolves identities, creates customer segments using SQL, generates reverse ETL payloads, and personalizes messages using Liquid-style templates. I also added A/B testing and a Streamlit dashboard to show campaign performance.”
