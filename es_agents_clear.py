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
AGENT_TOOLS_TO_AVOID_DELETE = ["platform.core.search", 
                               "platform.core.execute_esql", 
                               "platform.core.generate_esql",
                               "platform.core.list_indices", 
                               "platform.core.get_index_mapping",
                               "platform.core.index_explorer",
                               "platform.core.get_document_by_id"]

AGENTS_TO_AVOID_DELETE = ["elastic-ai-agent"]


# Delete tools from the agent builder
def delete_agent_builder_tool(tool_id): 
    url = f"{ES_AGENT_URL}/tools/{tool_id}"
    response = make_http_request(url, method="DELETE", headers=HEADERS)
    if response:
        return response.json()
    return None

# Delete all of the tools from the agent builder except those in the avoid list
def clear_agent_builder_tools():  
    url = f"{ES_AGENT_URL}/tools"
    response = make_http_request(url, method="GET", headers=HEADERS)
    if response:
        tools = response.json()
        for tool in tools.get('results', []):
            # print(json.dumps(tool, indent=2, ensure_ascii=False))
            tool_id = tool.get("id")
            if tool_id not in AGENT_TOOLS_TO_AVOID_DELETE:
                delete_response = delete_agent_builder_tool(tool_id)
                if delete_response:
                    print(f"Deleted tool: {tool_id}")
                else:
                    print(f"Failed to delete tool: {tool_id}")
    else:
        print("Failed to retrieve tools.")

clear_agent_builder_tools()


# Delete agents from the agent builder
def delete_agent_builder_agent(agent_id): 
    url = f"{ES_AGENT_URL}/agents/{agent_id}"
    response = make_http_request(url, method="DELETE", headers=HEADERS)
    if response:
        return response.json()
    return None

# Delete all of the agents from the agent builder except those in the avoid list
def clear_agent_builder_agents():   
    url = f"{ES_AGENT_URL}/agents"
    response = make_http_request(url, method="GET", headers=HEADERS)
    if response:
        agents = response.json()
        for agent in agents.get('results', []):
            # print(json.dumps(agent, indent=2, ensure_ascii=False))
            agent_id = agent.get("id")
            if agent_id not in AGENTS_TO_AVOID_DELETE:
                delete_response = delete_agent_builder_agent(agent_id)
                if delete_response:
                    print(f"Deleted agent: {agent_id}")
                else:
                    print(f"Failed to delete agent: {agent_id}")
    else:
        print("Failed to retrieve agents.")      


clear_agent_builder_agents()