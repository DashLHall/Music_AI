import pandas as pd
import chromadb 
from sentence_transformers import SentenceTransformer
#parses excel file into a .txt

def read_excel_to_2d_array(file_path, sheet_name):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Convert each row to a list of values and store in a list
    rows_as_2d_array = df.values.tolist()
    
    return rows_as_2d_array

def write_string_to_file(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)

#init
file_path='/Users/dashiellhall/Desktop/Music_AI/Music DB.xlsx'
sheets = ['itunes_saadiq']

write_string_to_file('/Users/dashiellhall/Desktop/Music_AI/Chroma_DB/parsed.txt',str(read_excel_to_2d_array(file_path,sheets[0])))