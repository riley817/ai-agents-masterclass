from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("openai/gpt-4o")

def get_weather(city):
    return f"The weather in {city} is 30 degress."

def conver_units(degress: int):
    return f"That is 40 farenheit"

geo_agent = Agent(
    name="GeoAgent",
    instruction="You help the user with geo questions",
    model=MODEL,
    description="Transfer to this agent when you have a geo related question."
)


# sub agent -> 상위 체인 agent로  
weather_agent = Agent(
    name="WeatherAgent",
    instruction="You help the user with weather related questions",
    model=MODEL,
    tools=[
        get_weather, 
        conver_units,
        AgentTool(
            name="GeoAgent",
            agent=geo_agent,
        )
    ],
    sub_agents=[geo_agent], # open ai handoff 비슷
    
)
# 반드시 root_agent
root_agent = weather_agent