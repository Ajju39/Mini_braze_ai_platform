# 2-Minute Interview Demo Script

## Opening

“I built a small project to simulate how a Braze-style customer engagement workflow works end-to-end. The goal was to show how events, user attributes, segmentation, reverse ETL, personalization, and reporting connect together.”

## Architecture Explanation

“The pipeline starts with event data, similar to what would be captured from a Braze SDK or REST API. These events include app opens, sessions, purchases, trial starts, and feature usage across Windows, desktop, and web platforms.”

“Next, I perform identity resolution by mapping device-level IDs to known user IDs. This is important because CRM platforms often receive anonymous device activity first and later need to stitch it back to account-level profiles.”

“After that, I use SQL-based segmentation logic to classify users into groups such as high-value users, trial users, inactive users, default users, and users who should not be messaged because of consent preferences.”

## Data Engineering Explanation

“The ETL pipeline is written in Python. It loads user data, raw event data, and identity mapping data, then transforms them into unified events and segment tables. In a real enterprise environment, this same logic could run in Databricks using SQL, PySpark, Delta Lake tables, and scheduled jobs.”

## Reverse ETL Explanation

“I also created a reverse ETL payload that simulates syncing user attributes from a warehouse back into Braze. In a production environment, this would typically be done using Hightouch or a similar tool to sync audience segments and profile attributes into Braze.”

## Personalization Explanation

“For personalization, I used a Liquid-style templating approach. Based on each user’s segment, the system generates a customized message. For example, premium purchasers get a high-value message, trial users get a trial reminder, and inactive users get a re-engagement message.”

## A/B Testing Explanation

“I added deterministic A/B testing logic so each user is assigned to variant A or B. Variant A sends an email-style message, while variant B sends an in-app style message. This mimics how Braze Canvas could test different channels or message strategies.”

## Dashboard Explanation

“The Streamlit dashboard shows total users, total events, purchasers, messageable users, segment distribution, personalized messages, and unified events after identity resolution. This gives both technical and business stakeholders visibility into campaign readiness and data quality.”

## Closing

“This project helped me connect the business side of CRM marketing with the technical implementation: event schemas, data contracts, identity stitching, SQL segmentation, reverse ETL, personalization, and reporting. That is exactly the kind of bridge I would bring to this role.”
