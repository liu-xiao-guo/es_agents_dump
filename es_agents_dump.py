from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

ES_AGENT_URL = os.getenv("ES_AGENT_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
KIBANA_URL = os.getenv("KIBANA_URL")
ES_URL = os.getenv("ES_URL")

# --- Setup Headers ---
HEADERS = {
    "Content-Type": "application/json",
    "kbn-xsrf": "true",
    "Authorization": f"ApiKey {ES_API_KEY}",
}

def make_http_request(url, method="GET", headers=None, data=None, params=None):
    """
    Make an HTTP request to the specified URL.
    
    Args:
        url (str): The URL to make the request to
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
        headers (dict): Optional headers to include in the request
        data (dict): Optional data to send in the request body
        params (dict): Optional query parameters
    
    Returns:
        requests.Response: The response object
    """
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=data,
            params=params
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


# Get all of the tools from the agent builder
def get_agent_builder_tools():  
    url = f"{ES_AGENT_URL}/tools"
    response = make_http_request(url, method="GET", headers=HEADERS)
    if response:
        return response.json()
    return None  


response = get_agent_builder_tools()
if response:
    print(json.dumps(response, indent=2))

    # Dump the response.results to a file
    if response and 'results' in response:
        with open('agent_tools.json', 'w') as f:
            json.dump(response['results'], f, indent=2)
        print("\nAgent tools dumped to agent_tools.json")


# Get all of the agents from the agent builder
def get_agent_builder_agents():  
    url = f"{ES_AGENT_URL}/agents"
    response = make_http_request(url, method="GET", headers=HEADERS)
    if response:
        return response.json()
    return None

response = get_agent_builder_agents()
if response:
    print(json.dumps(response, indent=2))

    # Dump the response.results to a file
    if response and 'results' in response:
        with open('agent_agents.json', 'w') as f:
            json.dump(response['results'], f, indent=2)
        print("\nAgent agents dumped to agent_agents.json")