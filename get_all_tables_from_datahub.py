import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATAHUB_GMS_URL = os.getenv('DATAHUB_GMS_URL', 'http://localhost:8080')
DATAHUB_TOKEN = os.getenv('DATAHUB_TOKEN', None)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Gemini API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash') # Or your preferred model
else:
    print("Warning: GOOGLE_API_KEY not found in .env. Cannot generate descriptions.")
    gemini_model = None

HEADERS = {
    'Authorization': f'Bearer {DATAHUB_TOKEN}' if DATAHUB_TOKEN else '',
    'Content-Type': 'application/json',
}

GRAPHQL_URL = DATAHUB_GMS_URL.rstrip('/') + '/api/graphql'

def get_all_tables(page_size: int = 500):
    query = '''
    query search($input: SearchInput!) {
      search(input: $input) {
        start
        count
        total
        searchResults {
          entity {
            urn
            ... on Dataset {
              name
            }
          }
        }
      }
    }
    '''
    all_tables = []
    start = 0
    total = float('inf')

    print("Fetching all datasets from DataHub...")
    while start < total:
        variables = {
            "input": {
                "type": "DATASET",
                "query": "*",
                "filters": [],  # Removed filters
                "start": start,
                "count": page_size
            }
        }
        try:
            resp = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS)
            resp.raise_for_status()
            resp_json = resp.json()

            if 'data' not in resp_json or resp_json['data'] is None:
                print('GraphQL response:', resp_json)
                raise Exception('No data returned from DataHub GraphQL API')

            search_result = resp_json['data']['search']
            results = search_result['searchResults']
            total = search_result['total']

            if not results:
                break  # No more results

            for r in results:
                entity = r['entity']
                # Create a simple object to hold urn and name
                all_tables.append(type('Table', (), {'urn': entity['urn'], 'name': entity.get('name', '')}))

            start += len(results)
            print(f"Fetched {start}/{total} datasets...")

        except requests.exceptions.RequestException as e:
            print(f"Error during GraphQL request: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    print(f"Finished fetching. Total datasets found: {len(all_tables)}")
    return all_tables

def DescribeTable(table_urn: str):
    query = '''
    query getDataset($urn: String!) {
      dataset(urn: $urn) {
        urn
        # editableSchemaMetadata may not have description directly, skip for now
        # If documentation exists, it might be in 'properties' or 'documentation' aspects
        schemaMetadata {
          fields {
            fieldPath
            type # Changed from type { type }
            description
          }
        }
        # Example: fetch documentation if available
        # documentation {
        #   description
        # }
      }
    }
    '''
    variables = {"urn": table_urn}
    resp = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    resp.raise_for_status()
    resp_json = resp.json()

    if 'data' not in resp_json or resp_json['data'] is None or resp_json['data'].get('dataset') is None:
        print(f'GraphQL response for DescribeTable({table_urn}):', resp_json)
        raise Exception(f'No dataset data returned from DataHub GraphQL API for URN: {table_urn}')

    entity = resp_json['data']['dataset']

    doc = None # We are not fetching documentation in this version
    columns = []
    # Documentation - If needed, query `documentation` aspect separately or adjust query
    # if entity and entity.get('documentation'):
    #     doc = entity['documentation'].get('description')

    if entity and entity.get('schemaMetadata'):
        for field in entity['schemaMetadata'].get('fields', []):
            field_type = field.get('type') # Directly get the type
            columns.append({
                'name': field.get('fieldPath'),
                'type': str(field_type) if field_type else None, # Convert type to string
                'description': field.get('description'),
            })
    return {
        'description': doc,
        'columns': columns
    }

def generate_table_description(table_name: str, columns: list) -> str:
    """Generates a table description using Gemini based on column names and types."""
    if not gemini_model:
        return "(Gemini API not configured)"
    if not columns:
        return "(Table has no columns to describe)"

    prompt = f"Generate a concise, one-sentence description for a database table named '{table_name}' based on its columns.\n\nColumns:\n"
    for col in columns:
        col_desc = f" - {col.get('name')} (Type: {col.get('type')})"
        if col.get('description'):
            col_desc += f": {col.get('description')}"
        prompt += col_desc + "\n"
    prompt += "\nDescription:"

    try:
        print(f"\nGenerating description for {table_name} using Gemini...")
        response = gemini_model.generate_content(prompt)
        # Handle potential safety blocks or empty responses
        if response.parts:
            generated_desc = response.parts[0].text.strip()
            return generated_desc
        else:
            print(f"Warning: Gemini response for {table_name} was empty or blocked. {response.prompt_feedback}")
            return "(Failed to generate description)"
    except Exception as e:
        print(f"Error calling Gemini API for {table_name}: {e}")
        return "(Error generating description)"

if __name__ == "__main__":
    tables = get_all_tables()  # Call without filters
    print(f"Found {len(tables)} total datasets:")
    # Print first 10 for brevity
    for t in tables[:10]:
        print(t.urn, t.name)

    found_table_with_columns = False
    if tables:
        print("\nSearching for first dataset with columns...")
        for t in tables:
            print(f"Checking {t.urn}...")
            try:
                desc_data = DescribeTable(t.urn)
                if desc_data.get('columns'):  # Check if the columns list is not empty
                    print(f"\nFound table with columns: {t.urn} ({t.name})")
                    print("Existing Metadata:", desc_data)

                    # Generate new description using Gemini
                    generated_desc = generate_table_description(t.name, desc_data['columns'])
                    print("\nGenerated Description:")
                    print(generated_desc)

                    found_table_with_columns = True
                    break  # Stop after finding the first one
            except Exception as e:
                print(f"  -> Error describing table {t.urn}: {e}")

        if not found_table_with_columns:
            print("\nNo datasets found with schema information (columns) in DataHub.")
    else:
        print("No datasets found in DataHub.") 