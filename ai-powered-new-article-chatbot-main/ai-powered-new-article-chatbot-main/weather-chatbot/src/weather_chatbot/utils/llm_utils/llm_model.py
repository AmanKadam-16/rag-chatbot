from src.weather_chatbot.core.config import settings


class LanguageModel:
    models_info = {
        "meta/llama-3.3-70b-instruct": {
            "context_window": 15000,
            "unit": "tokens",
            "category": "chat ,language generation ,large language models ,text-to-text ,code generation",
            "description": "Powers complex conversations with superior contextual understanding, reasoning and text generation",
        },
        "deepseek-ai/deepseek-v3.1-terminus": {
            "context_window": 20000,
            "unit": "tokens",
            "category": "advanced reasoning ,agentic ,chat ,tool calling",
            "description": "DeepSeek-V3.1: hybrid inference LLM with Think/Non-Think modes, stronger agents, 128K context, strict function calling.",
        },
        "openai/gpt-oss-20b": {
            "context_window": 12000,
            "unit": "tokens",
            "category": "math ,chat ,reasoning ,text-to-text",
            "description": "Smaller Mixture of Experts (MoE) text-only LLM for efficient AI reasoning and math.",
        },
        "openai/gpt-oss-120b": {
            "context_window": 12000,
            "unit": "tokens",
            "category": "math ,chat ,reasoning ,text-to-text",
            "description": "Mixture of Experts (MoE) reasoning LLM (text-only) designed to fit within 80GB GPU.",
        },
    }

    def __init__(self, model_name, context_window):
        self.model_name = model_name
        self.context_window = context_window

    def update_model_preset(self, model_name):
        if model_name not in self.models_info:
            raise Exception("Model name invalid.")
        model_preset = self.models_info[model_name]
        self.model_name = model_name
        self.context_window = model_preset["context_window"]
        return {"updated_model": self.model_name, "context_length": self.context_window}

    def get_model_name(self):
        return self.model_name

    def get_model_context_length(self):
        return self.context_window


LLM_MODEL_CONFIG = LanguageModel(settings.MODEL_NAME, settings.MODEL_CONTEXT_WINDOW)
