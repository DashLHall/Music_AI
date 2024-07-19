import pandas as pd
import chromadb 
from sentence_transformers import SentenceTransformer

#goals
#chromadb consitent server setup to only have to init once when u start to run server
#condense down info into just list of stuff
#ask chatgpt to only 


def read_excel_to_2d_array(file_path, sheet_name):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Convert each row to a list of values and store in a list
    rows_as_2d_array = df.values.tolist()
    
    return rows_as_2d_array

#init
file_path='/Users/dashiellhall/Desktop/Music_AI/Music DB.xlsx'
sheets = ['itunes_saadiq']
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="music_data")

#reads each sheet in
data = read_excel_to_2d_array(file_path,sheets[0])

#adds to chromadb
k=0
for i in data:
    metadata=str(i)
    collection.add(
        documents=[str(i)],
        metadatas=[{"pk":metadata[0],"export_data":metadata[1],
                    "export_date_raw":metadata[2],"itunes_release":metadata[3],
                    "original_release":metadata[4],"parental_advisory_id":metadata[5],
                    "preview_length":metadata[6],"preview_length_raw":metadata[7],"song_id":metadata[8],
                    "track_length":metadata[9],"track_length_raw":metadata[10],"artist_display_name":metadata[11],
                    "collection_display_name":metadata[12],
                    "copyright":metadata[13],"name":metadata[14],"p_line":metadata[15],"preview_url":metadata[16],
                    "search_terms":metadata[17],"title_version":metadata[18],"view_url":metadata[19],"isrc":metadata[20]}],
        ids=['id'+str(k)]
    )
    k=k+1


results=collection.query(
    query_texts=["list songs by Raphael Saadiq"],
    n_results=200,
    where_document={"$contains": "Raphael Saadiq"},
    include=["documents"]
)
header=["pk","export_data",
                    "export_date_raw","itunes_release",
                    "original_release","parental_advisory_id",
                    "preview_length","preview_length_raw","song_id",
                    "track_length","track_length_raw","artist_display_name",
                    "collection_display_name",
                    "copyright","name","p_line","preview_url",
                    "search_terms","title_version","view_url","isrc"]


import os
from openai import OpenAI
client = OpenAI(
    api_key='sk-None-M8RyvDsNAIV6GYZBnyuzT3BlbkFJ6Ji1d6OcykynEAgZas3g'
)

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
    
response = call_chatgpt_with_prompt("streamline this data into a spreadsheet that has the format of"+str(header)+" while using this data "+str(results))
print(response)


