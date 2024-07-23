import json
from Chroma_DB.query_chroma_db import get_DB_Query_output
import re

def process_question(question):
    data = get_DB_Query_output(question)
    print(f"Raw Data: {data}")  # Debugging: Print raw data from DB query
    
    documents = data.get('documents', [])
    print(f"Documents: {documents}")  # Debugging: Print documents data

    # Function to handle conversion of complex objects to JSON-friendly types
    def convert_to_json_friendly(item):
        if isinstance(item, float) and (item != item or item == float('inf') or item == float('-inf')):
            return None  # Handle NaN and infinity
        elif isinstance(item, str) and 'Timestamp' in item:
            item = item.replace("Timestamp('", '"').replace("')", '"')
        elif isinstance(item, str):
            item = item.replace('nan', 'null')
        return item

    def clean_and_parse_json_string(json_string):
        try:
            # Remove surrounding square brackets and split the string
            items = json_string[1:-1].split(',')
            cleaned_items = []
            for item in items:
                item = item.strip()
                item = convert_to_json_friendly(item)
                # If the item is still a string after conversion, ensure it is properly quoted
                if isinstance(item, str) and not item.startswith('"') and not item.endswith('"'):
                    item = f'"{item}"'
                cleaned_items.append(item)
            # Reconstruct the JSON string
            cleaned_json_string = f"[{','.join(cleaned_items)}]"
            return json.loads(cleaned_json_string)
        except Exception as e:
            print(f"Error cleaning and parsing JSON string: {json_string}, Error: {e}")
            return None

    # Convert the list of lists into a JSON-compatible format
    flattened_data = []
    for sublist in documents:
        for item in sublist:
            try:
                if isinstance(item, str) and item.startswith('[') and item.endswith(']'):
                    parsed_item = clean_and_parse_json_string(item)
                else:
                    parsed_item = convert_to_json_friendly(item)
                if parsed_item is not None:
                    flattened_data.append(parsed_item)
            except Exception as e:
                print(f"Error processing item: {item}, Error: {e}")
                continue

    # Print the flattened data
    print("Flattened Data:", json.dumps(flattened_data, indent=2))  # Debugging: Print flattened data
    return flattened_data
##question = "list all songs by raphael saadiq"
#processed_data = process_question(question)
#print("Processed Data:", processed_data)





