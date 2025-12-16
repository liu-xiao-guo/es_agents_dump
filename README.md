This project shows how to maintain your agents and tools created by the AI Agent builder. There are 3 files:

- **es_agents_clear.py**: use to clear all of the tools and agents
- **es_agents_dump.py**: used to save all of the tools and agents into **agent_tools.json** and **agent_agents.json** files
- **es_agents_import.py**: used to import all of the tools and agents from **agent_tools.json** and **agent_agents.json** files

**Note:** Before you clear all of your agents and tools, make sure you use es_agents_dump.py to save them. Otherwise, your settings will not be saved.

You can run them like:

```
python es_agents_dump.py
python es_agents_import.py
python es_agents_clear.py
```

You can even maintain the two JSON files to create new tools and agents easily. You directly edit the files and then re-import the tools and agents.

**.env**

- ES_AGENT_URL=http://localhost:5601/api/agent_builder
- KIBANA_URL=http://localhost:5601
- ES_URL=https://localhost:9200
- ES_API_KEY=WnJwR3RKb0JGQVVCVjdnb29yUkI6RHotbGZBTmJzMDJWUWszbTAtbDVjQQ==

You have to make changes according to your setup.

The whole API spec can be found at https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder

**License** ⚖️
This software is licensed under the [https://github.com/elastic/elasticsearch-labs/blob/main/LICENSE](Apache License, version 2 ("ALv2")).