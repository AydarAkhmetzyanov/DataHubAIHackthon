# DataHubAI Pitch Plan

## 1. Problem Statement
- Data discovery and governance are challenging in modern organizations.
- Traditional data catalogs lack AI-powered search, context, and automation.
- Teams waste time finding, understanding, and using data.

## 2. Solution: DataHubAI
- An intelligent data catalog built on DataHub, enhanced with AI/LLM capabilities.
- Semantic search, automated metadata, and natural language SQL generation.
- Google ADK and Gemini integration for advanced reasoning and automation.

## 3. Key Features
- **Semantic Table Search:** Find relevant datasets using natural language.
- **AI-Generated Metadata:** Automatic table and column descriptions.
- **Natural Language to SQL:** Generate Postgres SQL from user questions.
- **Data Quality Analysis:** Detect issues using LLMs.
- **Lineage & Context:** Extract lineage from GitHub and wikis.

## 4. System Architecture

```
+-------------------+         +-------------------+         +-------------------+
|   User / Analyst  | <-----> |   DataHubAI Agent | <-----> |    DataHub Core   |
+-------------------+         +-------------------+         +-------------------+
         |                            |                              |
         |                            |                              |
         v                            v                              v
+-------------------+         +-------------------+         +-------------------+
|  Google Gemini    |         |   Qdrant Vector   |         |  Data Sources     |
|  (LLM/ADK)        |         |   Database        |         |  (DBs, GitHub,    |
+-------------------+         +-------------------+         |   Wikis, etc.)    |
                                                            +-------------------+
```

- **User/Analyst:** Interacts via UI or chat, asks questions in natural language.
- **DataHubAI Agent:** Orchestrates search, description, and SQL generation using tools.
- **Qdrant:** Stores dense embeddings for semantic search.
- **Google Gemini/ADK:** Provides LLM-powered reasoning and metadata generation.
- **DataHub Core:** Manages metadata, schemas, and connects to data sources.

## 5. Demo Flow
1. User asks: "Show me the most active users last month."
2. Agent semantically searches Qdrant for relevant tables.
3. Agent describes table(s) using DataHub schema.
4. Agent generates and returns a Postgres SQL query.
5. (Optional) User runs query in their data warehouse.

## 6. Value Proposition
- **Faster Data Discovery:** Find the right data instantly.
- **Self-Service Analytics:** Anyone can generate SQL, not just data engineers.
- **Automated Documentation:** Always up-to-date, AI-generated context.
- **Improved Data Quality:** Proactive issue detection.

## 7. Next Steps
- Expand to more data sources and cloud platforms.
- Add more AI-powered tools (data quality, lineage, etc.).
- Open source and community engagement.

--- 