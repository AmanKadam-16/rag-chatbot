from src.weather_chatbot.utils.tools.tool_function import ModelFunctions


class model_tool:

    tool_list = [
        {
            "type": "function",
            "function": {
                "name": "get_continent_weather_context",
                "description": "This function takes PostgreSQL query to pull context from database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sql_query": {
                            "type": "string",
                            "description": "Here we strictly expect the parameters to be a query based on schema context provided.",
                        },
                    },
                    "required": ["sql_query"],
                },
            },
        },
    ]

    tool_function_mapping = {
        "get_continent_weather_context": ModelFunctions.get_continent_weather_context
    }
