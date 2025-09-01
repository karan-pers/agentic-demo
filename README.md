# Multi-Agent with MCP sample


The core logic defined in `src/agent/**.py`, showcases an array of agents.


## Getting Started

1. Install dependencies, along with the [LangGraph CLI](https://langchain-ai.github.io/langgraph/concepts/langgraph_cli/), which will be used to run the server.

```bash
uv sync --native-tls
```

2. (Optional) Customize the code and project as needed. Create a `.env` file if you need to use secrets.

```bash
cp .env.example .env
```

If you want to enable LangSmith tracing, add your LangSmith API key to the `.env` file.

```text
# .env
LANGSMITH_API_KEY=lsv2...
```

3. Run all MCP servers.

```shell
#Windows
run_all_mcp_servers.cmd

#Mac
./run_all_mcp_servers.sh
```

4. Start the LangGraph Server.

```shell
uv run langgraph dev --allow-blocking
```

5. Test agent with Agent Chat UI

Open deployed version of [Agent Chat UI](https://agentchat.vercel.app/). In Assistant/Graph Id use `conversational` , or any standalone agent you want to test

6. Teardown MCP servers.

```shell
#Windows
Close all windows

#Mac
./stop_all_mcp_servers.sh
```
For more information on getting started with LangGraph Server, [see here](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/).


## Development

While iterating on your graph in LangGraph Studio, you can edit past state and rerun your app from previous states to debug specific nodes. Local changes will be automatically applied via hot reload.

Follow-up requests extend the same thread. You can create an entirely new thread, clearing previous history, using the `+` button in the top right.

For more advanced features and examples, refer to the [LangGraph documentation](https://langchain-ai.github.io/langgraph/). These resources can help you adapt this template for your specific use case and build more sophisticated conversational agents.

LangGraph Studio also integrates with [LangSmith](https://smith.langchain.com/) for more in-depth tracing and collaboration with teammates, allowing you to analyze and optimize your chatbot's performance.