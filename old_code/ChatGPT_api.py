import pandas as pd
from openai import OpenAI
import os

client = OpenAI(api_key='sk-None-M8RyvDsNAIV6GYZBnyuzT3BlbkFJ6Ji1d6OcykynEAgZas3g')

def call_chatgpt_with_prompt_and_file(prompt,sheet_name, file_path):
    # Read the Excel file content
    df = pd.read_excel(file_path,sheet_name=sheet_name)
    file_content = df.to_csv(index=False)  # Convert DataFrame to CSV string

    # Combine the custom prompt with the file content
    combined_prompt = f"{prompt}\n\n{file_content}"

    # Call the OpenAI API with the combined prompt
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Specify the model you want to use
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": combined_prompt}
        ]
    )

    # Get the response content
    reply = response.choices[0].message.content
    return reply
    
def ChatGPT_run(question):
    # Params
    print(question)
    file_path = f'/Users/dashiellhall/Desktop/Music_AI/Music DB.xlsx'  # Input Excel file
    sheets = ['itunes_saadiq']  # Sheet names to process
    response=''
    
    #for i in sheets:
        #response += call_chatgpt_with_prompt_and_file(question,i,file_path)+'\n'
    
    #return response 
    return question