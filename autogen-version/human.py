import os
from autogen import ConversableAgent

llm_config = {
    "model": "gpt-4o",
    "api_type": "azure",
    "api_key": os.environ['AZURE_OPENAI_API_KEY'],
    "base_url": "https://oai-mv-sandbox.openai.azure.com/",
    "api_version": "2024-02-01"
  }

humanAgent = ConversableAgent(
        "presenter",
        system_message="You provide the input for the session abstract. You know what you're going to present.",
        llm_config=False,
        human_input_mode="ALWAYS",  # Always ask for human input.
)
