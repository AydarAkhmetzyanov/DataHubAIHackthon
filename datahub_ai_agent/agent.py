import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

# Import tools from other scripts
from get_all_tables_from_datahub import DescribeTable
from search_table import search_tables as SearchTable # Rename for clarity in agent


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


# Define the agent
root_agent = Agent(
    name="datahub_sql_agent",
    model="gemini-2.0-flash", # Using a more powerful model for SQL generation
    description=(
        "An agent that helps explore datahub tables using semantic search "
        "and generates PostgreSQL SQL queries."
    ),
    instruction=(
        "You are a helpful AI assistant specialized in data exploration and SQL generation.\n\n"
        "When a user asks a question about data or requests an SQL query:\n"
        "1. First, use the `SearchTable` tool to find the most relevant tables in the Qdrant vector database based on the user's query.\n"
        "2. Analyze the search results. Identify the most promising table(s) (usually the top 1-2 results).\n"
        "3. Use the `DescribeTable` tool to get the schema (columns and types) for the selected table(s).\n"
        "4. Based on the user's request and the table schema, generate an accurate and efficient PostgreSQL (PGSQL) query.\n"
        "5. Present the final SQL query to the user, explaining which table(s) it uses and why.\n"
        "6. If the search results are not relevant or the necessary tables cannot be found, inform the user clearly.\n"
        "7. If the user provides a specific table name, you can use `DescribeTable` directly without searching first."
    ),
    tools=[SearchTable, DescribeTable],
)