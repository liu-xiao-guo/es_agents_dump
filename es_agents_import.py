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
        # print(f"Error making request: {e}")
        return None

# Define a list of tool ids to avoid to import
AGENT_TOOLS_TO_AVOID_IMPORT = ["platform.core.search", 
                               "platform.core.execute_esql", 
                               "platform.core.generate_esql",
                               "platform.core.list_indices", 
                               "platform.core.get_index_mapping",
                               "platform.core.index_explorer",
                               "platform.core.get_document_by_id"]
    
# import tools into the agent builder
def import_agent_builder_tool(tool_data): 
    url = f"{ES_AGENT_URL}/tools"
    response = make_http_request(url, method="POST", headers=HEADERS, data=tool_data)
    if response:
        return response.json()
    return None

# Add a function to check whether a tool already exists in the agent builder
def tool_exists_in_agent_builder(tool_id):
    url = f"{ES_AGENT_URL}/tools/{tool_id}"
    response = make_http_request(url, method="GET", headers=HEADERS)
    if response and response.status_code == 200:
        return True
    return False

# Read in agent_tools.json file, and import each tool into the agent builder
with open("agent_tools.json", "r") as f:    
    agent_tools = json.load(f)
    for tool in agent_tools:
        if tool["id"] in AGENT_TOOLS_TO_AVOID_IMPORT:   
            print(f"Skipping import of tool {tool['id']}")
            continue
        
        if tool_exists_in_agent_builder(tool["id"]):
            print(f"Tool {tool['id']} already exists, skipping import")
            continue
            
        print(f"Importing tool {tool['id']}")
        # print(json.dumps(tool, indent=2, ensure_ascii=False))
        tool.pop('readonly', None)
        response = import_agent_builder_tool(tool)
        if response:
            print(f"Successfully imported tool {tool['id']}")
        else:
            print(f"Failed to import tool {tool['id']}")
    

AGENTS_TO_AVOID_IMPORT = ["elastic-ai-agent"]

# import agents into the agent builder
def import_agent_builder_agent(agent_data): 
    url = f"{ES_AGENT_URL}/agents"
    response = make_http_request(url, method="POST", headers=HEADERS, data=agent_data)
    if response:
        return response.json()
    return None

# Add a function to check whether an agent already exists in the agent builder
def agent_exists_in_agent_builder(agent_id):
    url = f"{ES_AGENT_URL}/agents/{agent_id}"
    response = make_http_request(url, method="GET", headers=HEADERS)
    if response and response.status_code == 200:
        return True
    return False

# Read in agent_agents.json file, and import each agent into the agent builder
with open("agent_agents.json", "r") as f:    
    agent_agents = json.load(f)
    for agent in agent_agents:
        if agent["id"] in AGENTS_TO_AVOID_IMPORT:   
            print(f"Skipping import of agent {agent['id']}")
            continue
        
        if agent_exists_in_agent_builder(agent["id"]):
            print(f"Agent {agent['id']} already exists, skipping import")
            continue
            
        print(f"Importing agent {agent['id']}")
        agent.pop('readonly', None)
        agent.pop('type', None)
        # print(json.dumps(agent, indent=2, ensure_ascii=False))        
        response = import_agent_builder_agent(agent)
        if response:
            print(f"Successfully imported agent {agent['id']}")
        else:
            print(f"Failed to import agent {agent['id']}")  