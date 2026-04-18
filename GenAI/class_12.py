from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools import ShellTool


# search_results = DuckDuckGoSearchRun()

# results = search_results.invoke("What is LangSmith?")

# print(results)

# tool = PythonREPLTool()
# result = tool.run("print(2+3)")
# print(result)

# search_results = ShellTool()
# result = search_results.invoke("cd\\Module2data")
# print(result)

@tool
def multiply(a:int, b:int) -> int:
    """Multiplies two numbers together."""
    return a * b