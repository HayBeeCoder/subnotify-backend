#main.py
import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()



url = os.getenv('SUPABASE_SUPAFAST_URL')
key = os.getenv('SUPABASE_SUPAFAST_KEY')
supabase: Client = create_client(url, key)
results = supabase.table('demo-table').select('*').execute() 

print(results)

@app.get("/themes")
def themes():
    themes = supabase.table('Themes').select('*').execute()
    return themes

@app.get("/monsters/")
def monsters(theme : str = "demo-theme-1"):
    monsters = supabase.table('monsters').select('*').eq('MonsterTheme',theme).execute()
    return monsters

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
    