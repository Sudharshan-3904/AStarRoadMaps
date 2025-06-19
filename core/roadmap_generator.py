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
    print("\n\n\n\n\n\n\n")

    with open(filename, "w", encoding="utf-8") as f:
        # json.dump(roadmap.to_dict(), f, default=str, indent=4)
        f.writelines(roadmap.to_dict())

@tool
def create_resource(title: str, url: str, description: str = "") -> map_elements.Resource:
    """
    Create a new resource with the given title, URL, and optional description.
    """
    return map_elements.Resource(title=title, url=url, description=description)

@tool
def create_keyframe(title: str, description: str, due_date: str, completed: bool = False) -> map_elements.Keyframe:
    """
    Create a new keyframe with the given title, description, due date, and completion status.
    """
    return map_elements.Keyframe(title=title, description=description, due_date=datetime.datetime.fromisoformat(due_date), completed=completed)

@tool
def create_stage(name: str, level: map_elements.LearningLevel) -> map_elements.Stage:
    """
    Create a new stage with the given name and learning level.
    """
    return map_elements.Stage(name=name, level=level)

@tool
def create_roadmap(topic: str, user_id: str = "default_user", level: map_elements.LearningLevel = 'full') -> map_elements.Roadmap:
    """
    Create a new roadmap with the given topic, user ID, and optional learning level.
    """
    generated_roadmap = map_elements.Roadmap(topic=topic, created_at=datetime.datetime.now(), user_id=user_id, level=level)

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
                                   If the user level is not given build a full roadmap from beginner to advanced level. 
                                   The generated data should be in json format. The generated output should be a roadmap object as defined in roadmap generator.
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

def generate_roadmap(topic: str, user_id: str = "default_user", level: Optional[map_elements.LearningLevel] = None):
    """
    Generate a roadmap based on the given topic, user ID, and optional learning level.
    """
    initial_state = {
        'messages': [
            HumanMessage(content=f"Create a roadmap for the topic: {topic} with user ID: {user_id} and level: {level if level else 'not specified'}.")
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

def convert_to_roadmap(input_string: str = ""):
    thing = json.loads(input_string)
    print("\n"*10)
    print(thing)
    save_roadmap(thing, f"data\\RoadMaps\\{topic}.json")

    return thing


if __name__ == "__main__":
    topic = "Artificial Intelligence"
    level = 'full'

    roadmap = generate_roadmap(topic, level)
    roadmap = convert_to_roadmap(roadmap)
    
    print("Exiting")
    
    roadmap_obj = map_elements.Roadmap(topic=topic, level=level)
