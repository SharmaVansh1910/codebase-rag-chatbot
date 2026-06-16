from dotenv import load_dotenv
import os

from google import genai


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))


while True:
    user_query = input("Enter your query: ")
    if user_query.lower() == "exit":
        break
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_query,
    )
    print(response.text)
    
 
