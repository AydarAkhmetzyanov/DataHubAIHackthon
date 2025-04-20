# DataHubAI

datahub docker quickstart -f docker-compose.quickstart.yml
Custom dockerfile with api keys

An intelligent data catalog built on [DataHub](https://datahubproject.io/) with AI-powered capabilities, developed for the Google AI Build Hackathon.

## Project Description

DataHubAI enhances traditional data catalogs with AI capabilities to make data discovery, governance, and usage more intuitive and powerful. Our solution addresses common data management challenges by integrating AI directly into the data catalog workflow.

### Core Features

- **Business Context Training**: Automatically train models on company wikis using key-value pairs to understand organizational data context
- **Data Quality Analysis**: AI-powered identification of data quality issues across datasets
- **SQL Generation**: Natural language to SQL conversion based on catalog metadata
- **Automated Metadata Generation**: Intelligent extraction and creation of metadata for datasets
- **GitHub Lineage Analysis**: Automatically detect and visualize data lineage from GitHub repositories
- **Enhanced DataHub Interface**: Custom UI extensions to the DataHub platform for AI features

## Architecture

DataHubAI builds on top of the open-source DataHub platform, integrating Google AI technologies to provide intelligent data catalog capabilities. The system connects to various data sources, analyzes metadata and content, and presents insights through an enhanced DataHub interface.

### Google ADK Integration

This project leverages [Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/get-started/quickstart/) to build intelligent agents that power our data catalog features. ADK provides the framework for:

- Creating LLM-powered agents with specialized data catalog knowledge
- Developing tools for data quality analysis and SQL generation
- Building multi-agent systems for complex data governance workflows
- Integrating with Google Cloud services and Gemini models

## Getting Started

### Prerequisites
- Python 3.12+
- DataHub instance
- Google Cloud account for AI/ML services
- Google ADK (`pip install google-adk`)

### Installation

```bash
# Clone the repository
git clone https://github.com/[username]/DataHubAI.git
cd DataHubAI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration for Google ADK
# GOOGLE_GENAI_USE_VERTEXAI=TRUE/FALSE
# GOOGLE_API_KEY or GOOGLE_CLOUD_PROJECT settings
```

### Running DataHubAI Agents

```bash
# Start the development UI
adk web

```

Visit http://localhost:8000 to interact with your agents through the ADK development UI.

## Usage

[Brief instructions on how to use the main features will be added as they are developed]

## Hackathon Team

[Team member information]

## License

[License information] 