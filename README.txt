How to run locally
-install all packages
pandas
chromadb
sentence-transformers
json
os
openai
sqlite3
flask_cors
flask
React
axios
react-table
npm/npx
python

for help installing or if i missed one consult chatgpt with terminal errors

start with intializing the database
in chroma_DB terminal
in populate_chroma_db.py
-change where your Music DB.xlsx file to the file path
-change chroma_client to where chroma_DB module is

-python populate_chroma_db.py 
in query_chroma_db.py
-change chroma_client to where chroma_DB module is


in backend terminal
-python app.py
in frontend terminal
-npm start

in ui type in
list all songs by:(insert artist name cap specific only space between first and last)
the : is needed for chroma_DB search atm
only lists 100 songs, output number can be changed
working on more complex prompts and output displays
curretn bug in parsing with song names with ,'s in them messing up data table





