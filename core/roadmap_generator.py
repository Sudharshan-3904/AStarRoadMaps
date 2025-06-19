import os
import json
from typing import TypedDict, Optional

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
import roadmap_elements as map_elements

import datetime

load_dotenv()

LM_STUDIO_MODEL_NAME = os.getenv("LM_STUDIO_MODEL_NAME")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
MODEL_MODE = os.getenv("MODEL_MODE", "LM_STUDIO")

def save_roadmap(roadmap: map_elements.Roadmap, filename: str):
    """
    Save the roadmap to a JSON file.
    """

    save = str(roadmap)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(roadmap, f, default=str, indent=4)

@tool
def create_resource(title: str, url: str, description: str = "") -> map_elements.Resource:
    """
    Create a new resource with the given title, URL, and optional description.
    """
    return map_elements.Resource(title=title, url=url, description=description)

@tool
def create_keyframe(title: str, description: str, due_date: str, completed: bool = False, resources: list[map_elements.Resource] = []) -> map_elements.Keyframe:
    """
    Create a new keyframe with the given title, description, due date, completion status, and a list of resources.
    """
    return map_elements.Keyframe(title=title, description=description, due_date=datetime.datetime.fromisoformat(due_date), completed=completed, resources=resources)

@tool
def create_stage(name: str, level: map_elements.LearningLevel, keyframes: list[map_elements.Keyframe]) -> map_elements.Stage:
    """
    Create a new stage with the given name, learning level and a list of keyframes.
    """
    return map_elements.Stage(name=name, level=level, keyframes=keyframes)

@tool
def create_roadmap(topic: str, level: map_elements.LearningLevel = 'full', stages: list[map_elements.Stage] = []) -> map_elements.Roadmap:
    """
    Create a new roadmap with the given topic, user ID, optional learning level, and a list of stages to be passed.
    """
    generated_roadmap = map_elements.Roadmap(topic=topic, created_at=datetime.datetime.now(), level=level, stages=stages)

    save_roadmap(generated_roadmap, f"{topic}.txt")

    return generated_roadmap 

class ChatState(TypedDict):
    messages: list
    topic: Optional[str]
    level: Optional[str]

llm = init_chat_model(LM_STUDIO_MODEL_NAME if MODEL_MODE=='lm-studio' else OLLAMA_MODEL_NAME, model_provider=MODEL_MODE)

# TODO - Define all the tools and their functionality here
tool_node = ToolNode([create_resource, create_keyframe, create_stage, create_roadmap])
raw_llm = init_chat_model(LM_STUDIO_MODEL_NAME if MODEL_MODE=='lm-studio' else OLLAMA_MODEL_NAME, model_provider=MODEL_MODE)


def llm_node(state):
    """
    A node that uses the LLM to generate a response based on the current state.
    """
    system_message = SystemMessage(content="""You are a professional roadmap creator. Use the topic give and the user level to build an optimal roadmap. 
                                   If the user level is not given build a full roadmap from beginner to advanced level. The generated data should be in json format 
                                   and should be very detailed with optinal additional concepts related to the topic. The generated output should be a roadmap object 
                                   as defined in roadmap generator. Ensure that proper JSON format is followed as it will be passed to json.loads().
                                   The following is the layout for each leve of the roadmap:
                                   
                                   # Resource:
                                   - Title
                                   - Description
                                   - URL
                                   
                                   # Keyframe
                                   - title
                                   - description
                                   - resourcess

                                   # Stage
                                   - name
                                   - level
                                   - keyframes

                                   # Roadmap
                                   - Topic
                                   - stages
                                   - level""")

    messages_for_llm = [system_message] + state['messages']
    response = llm.invoke(messages_for_llm)
    return {'messages': state['messages'] + [response]}

def router(state):
    """
    A router node that decides which node to invoke based on the current state.
    """    
    last_message = state['messages'][-1]

    if isinstance(last_message, AIMessage) and getattr(last_message, 'tool_calls', None):
        return 'tools'
    elif isinstance(last_message, ToolMessage):
        return 'llm'
    else:
        return 'end'

def tools_node(state):
    """
    A node that uses the tools to generate a response based on the current state.
    """
    result = tool_node.invoke(state)
    tool_output_messages = result.get('messages', [])

    return {'messages': state['messages'] + tool_output_messages}

builder = StateGraph(ChatState)
builder.add_node('llm', llm_node)
builder.add_node('tools', tools_node)
builder.add_edge(START, 'llm')
builder.add_edge('llm', 'tools')
builder.add_conditional_edges('llm', router, {'tools': 'tools', 'end': END})

graph = builder.compile()

def generate_roadmap(topic: str, level: Optional[map_elements.LearningLevel] = None):
    """
    Generate a roadmap based on the given topic, user ID, and optional learning level.
    """
    initial_state = {
        'messages': [
            HumanMessage(content=f"Create a roadmap for the topic: {topic} with level: {level if level else 'from begginer to advanced'}.")
        ]
    }
    
    final_state_output = None

    for s in graph.stream(initial_state):
        if 'llm' in s:
            final_state_output = s['llm']
        elif 'tools' in s:
            final_state_output = s['tools']
        
        if final_state_output and 'messages' in final_state_output and final_state_output['messages']:
            last_message = final_state_output['messages'][-1]

            if isinstance(last_message, AIMessage):
                return last_message.content
            elif isinstance(last_message, ToolMessage):
                return last_message.content
            else:
                return f"Agent response: {last_message}"
        else:
            return "No valid response from the agent."

def convert_to_json_str(input_string: str = ""):
    thing = json.loads(input_string)
    print("Converter called")
    save_roadmap(thing, f"data\\RoadMaps\\{topic}.json")
    print("File saved")
    return thing

def create_new_roadmap(topic, level):
    roadmap = str(generate_roadmap(topic, level))
    roadmap = str(generate_roadmap(topic, level))
    roadmap = roadmap[(roadmap.find("</think>") + len("</think>") + 2):]
    roadmap = convert_to_json_str(roadmap)
    roadmap = json.loads(roadmap)
    roadmap = map_elements.Roadmap.from_json(roadmap)
    return roadmap

if __name__ == "__main__":
    topic = "Roman Empire History"
    level = 'full'

    roadmap = str(generate_roadmap(topic, level))
    roadmap = roadmap[(roadmap.find("</think>") + len("</think>") + 2):]

    with open("things.txt", 'w') as f:
        f.writelines(roadmap)
    
    roadmap = convert_to_json_str(roadmap)
    
    print("Exiting")
    
    roadmap_obj = map_elements.Roadmap(topic=topic, level=level)
