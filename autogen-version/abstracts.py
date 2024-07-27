import os
from autogen import GroupChat, GroupChatManager
from writer import writerAgent
from human import humanAgent
from critic import criticAgent
from editor import contentEditorAgent

llm_config = {
    "model": "gpt-4o",
    "api_type": "azure",
    "api_key": os.environ['AZURE_OPENAI_API_KEY'],
    "base_url": "https://oai-mv-sandbox.openai.azure.com/",
    "api_version": "2024-02-01"
  }

group_chat = GroupChat(
    agents=[writerAgent, humanAgent, criticAgent, contentEditorAgent],
    messages=[],
    max_round=60,
    send_introductions=True
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)

chat_result = humanAgent.initiate_chat(
    group_chat_manager,
    message="Let's start writing then, shall we?",
    summary_method="reflection_with_llm",
)
