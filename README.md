This project shows how to maintain your agents and tools created by the AI Agent builder. There are 3 files:

**es_agents_clear.py** - use to clear all of the tools and agents
**es_agents_dump.py** - used to save all of the tools and agents into agent_tools.json and agent_agents.json files
**es_agents_import.py** - used to import all of the tools and agents from agent_tools.json and agent_agents.json files

**Note:** Before you clear all of your agents and tools, make sure you use es_agents_dump.py to save them. Otherwise, your settings will not be saved.

**.env**

ES_AGENT_URL=http://localhost:5601/api/agent_builder
KIBANA_URL=http://localhost:5601
ES_URL=https://localhost:9200
ES_API_KEY=WnJwR3RKb0JGQVVCVjdnb29yUkI6RHotbGZBTmJzMDJWUWszbTAtbDVjQQ==

You have to make changes according to your setup.
