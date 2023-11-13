from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()


# Define a Pydantic model for the request body
class DnsQueryRequest(BaseModel):
    name: str
    type: str = "A"


@app.post("/dns-query")
def dns_query(request: DnsQueryRequest):
    # Construct the URL for the Cloudflare API
    url = f"https://cloudflare-dns.com/dns-query?name={request.name}&type={request.type}"

    # Define the required headers
    headers = {"accept": "application/dns-json"}

    # Make the GET request to Cloudflare's DNS over HTTPS service
    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        # If there's an error with the request, raise an HTTPException
        raise HTTPException(status_code=response.status_code, detail=response.text)

# To run the server, use the command: uvicorn filename:app --reload
# Replace 'filename' with the name of your Python script
