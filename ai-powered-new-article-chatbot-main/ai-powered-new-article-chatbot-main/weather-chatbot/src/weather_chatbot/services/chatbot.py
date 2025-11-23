from openai import OpenAI
from src.weather_chatbot.core.config import settings
from src.weather_chatbot.utils.tools.tool import model_tool
from src.weather_chatbot.schemas.chatbot import UserInput
from src.weather_chatbot.utils.prompt.prompt_template import PromptTemplate
from src.weather_chatbot.schemas.chatbot import ChatRole, ChatHistory
from src.weather_chatbot.utils.llm_utils.llm_model import LLM_MODEL_CONFIG
from src.weather_chatbot.models.base import WeatherAppChatHistory
import uuid
import time
import json
import random
import os
from src.weather_chatbot.database.database import get_db

client = OpenAI(api_key=settings.API_KEY, base_url=settings.API_BASE_URL)

in_memory_chat_log = {}


def chat_with_llm(user_input: UserInput, session_id: str, user_id: int):
    initial_dict = {"session_id": session_id, "user_id": user_id}
    system_prompt = PromptTemplate.AGENTIC_BEHAVIOUR_PROMPT.value.format(
        TOOL_INVOKED_CONTEXT="N/A", AVAILABLE_TOOLS=model_tool.tool_list
    )
    if session_id not in in_memory_chat_log:
        system_message = {"role": ChatRole.SYSTEM.value, "content": system_prompt}
        previous_session_history = retrieve_chat_history(
            session_id=session_id, user_id=user_id
        )
        in_memory_chat_log[session_id] = [system_message]
        if previous_session_history:
            chat_history = []
            for chat in previous_session_history:
                chat_row = {"role": chat.role, "content": chat.chat_message}
                chat_history.append(chat_row)
            in_memory_chat_log[session_id] += chat_history

    user_message = {"role": ChatRole.USER.value, "content": user_input.content}
    in_memory_chat_log[session_id].append(user_message)
    store_chat_log(user_message | initial_dict)

    def invoke_llm():
        response = client.chat.completions.create(
            model=LLM_MODEL_CONFIG.get_model_name(),
            messages=in_memory_chat_log[session_id],
            temperature=1,
            top_p=1,
            max_tokens=int(LLM_MODEL_CONFIG.get_model_context_length()),
            # tools=model_tool.tool_list,
            # tool_choice="auto",
        )
        return response

    # while True:
    completion = invoke_llm()
    message = completion.choices[0].message
    parsed_response = json.loads(message.content)
    if parsed_response.get("tool_required"):
        print(f"STEP 01.\nPARSED ASSISTANT RESPONSE {parsed_response}\n")
        function_name = parsed_response.get("tool_name")
        function_args = parsed_response.get("tool_arg")
        fn = model_tool.tool_function_mapping.get(function_name)
        if not fn:
            result = {"error": f"Unknown tool: {function_name}"}
        else:
            result = fn(function_args)
        print(f"STEP 02.\nRECORD_PULLED_FROM_DB {result}")
        system_prompt = PromptTemplate.AGENTIC_BEHAVIOUR_PROMPT.value.format(
            TOOL_INVOKED_CONTEXT=result,
            AVAILABLE_TOOLS=model_tool.tool_list,
        )
        in_memory_chat_log[session_id][0]["content"] = system_prompt
        completion = invoke_llm()
        message = completion.choices[0].message
        parsed_response = json.loads(message.content)

        # continue

    assistant_response = parsed_response.get("response")
    assistant_message = {
        "role": ChatRole.ASSISTANT.value,
        "content": assistant_response,
    }
    in_memory_chat_log[session_id].append(assistant_message)
    store_chat_log(assistant_message | initial_dict)
    # break

    response = {
        "user_prompt": user_input.content,
        "assistant_response": assistant_response,
        "chat_history": in_memory_chat_log[session_id][1:],
        "session_id": session_id,
        "model_name": LLM_MODEL_CONFIG.get_model_name(),
    }
    print(f"\nLAST STEP\nFinal Output {parsed_response}\n")
    return response


def store_chat_log(chat_info: ChatHistory):
    db = next(get_db())
    new_chat_log = WeatherAppChatHistory(
        session_id=chat_info["session_id"],
        user_id=chat_info["user_id"],
        role=chat_info["role"],
        chat_message=chat_info["content"],
    )
    db.add(new_chat_log)
    db.commit()
    db.refresh(new_chat_log)


def retrieve_chat_history(session_id: str, user_id: str):
    db = next(get_db())
    chat_history = (
        db.query(WeatherAppChatHistory)
        .filter(
            WeatherAppChatHistory.session_id == uuid.UUID(session_id),
            WeatherAppChatHistory.user_id == user_id,
        )
        .order_by(WeatherAppChatHistory.created_at.asc())
    )
    in_memory_chat_log[session_id] = chat_history
    response = chat_history
    return response


def get_model_cards():
    return LLM_MODEL_CONFIG.models_info


def update_model_preset(model_name):
    response = LLM_MODEL_CONFIG.update_model_preset(model_name=model_name)
    return response


def get_mock_llm_responses(user_prompt: UserInput, session_id):
    file_path = os.getcwd() + r"\src\weather_chatbot\utils\prompt\mock_response.json"
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        random_choice = random.randint(0, len(data))
        response = {
            "user_prompt": user_prompt.content,
            "assistant_response": data[random_choice],
            "chat_history": [],
            "session_id": session_id,
            "model_name": "mock-llm",
        }
        time.sleep(2)
        return response
    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
