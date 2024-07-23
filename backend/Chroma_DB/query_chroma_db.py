# ask the Client and then call chatgpt to get answer
import chromadb
from sentence_transformers import SentenceTransformer
import os
from openai import OpenAI
import os

os.environ["TOKENIZERS_PARALLELISM"] = "true"
chroma_client = chromadb.PersistentClient(path="/Users/dashiellhall/Desktop/Music_AI/backend/Chroma_DB")
collection = chroma_client. get_or_create_collection(name="music_data")
client = OpenAI(
    api_key='sk-None-M8RyvDsNAIV6GYZBnyuzT3BlbkFJ6Ji1d6OcykynEAgZas3g'
)
query = "list songs by Raphael Saadiq"

header=["pk","export_data",
                    "export_date_raw","itunes_release",
                    "original_release","parental_advisory_id",
                    "preview_length","preview_length_raw","song_id",
                    "track_length","track_length_raw","artist_display_name",
                    "collection_display_name",
                    "copyright","name","p_line","preview_url",
                    "search_terms","title_version","view_url","isrc"]

#need to figure work-around for contains 
#gets results from chroma_db query
def get_DB_Query_output(query):
    name=query.split(":")
    print(name)
    results=collection.query(
        query_texts=[query],
        n_results=100,
        where_document={"$contains": name[1]},
        include=["documents"]
    )
    return results

def call_chatgpt_with_prompt(prompt):
    # Call the OpenAI API with the prompt
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Specify the model you want to use
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    # Get the response content
    return response.choices[0].message.content

#results=get_DB_Query_output(query)
#print(results)
#response = call_chatgpt_with_prompt("return only the data under \"'documents'\": and nothing else"+str(results))
#print(response)
#for chatgpt use, takes rlly long tho
def data_process(query):
    results=get_DB_Query_output(query)
    #print(results)
    response = call_chatgpt_with_prompt("return only the data under \"'documents'\": and nothing else"+str(results))
    print(response)

