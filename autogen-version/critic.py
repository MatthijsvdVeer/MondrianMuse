import os
from autogen import ConversableAgent

llm_config = {
    "model": "gpt-4o",
    "api_type": "azure",
    "api_key": os.environ['AZURE_OPENAI_API_KEY'],
    "base_url": "https://oai-mv-sandbox.openai.azure.com/",
    "api_version": "2024-02-01"
  }

systemMessage = """
You're a writing coach reviewing a presenter's abstract. The presenter has written an abstract for a tech conference. Your job is to provide feedback on the abstract. You should check if the abstract follows some writing rules. You're not bothered by the content, there is a content editor for that.

Your writing rules:
- Never discriminate against any group of people
- Never use the word "delve"
- Never use terms like "in a world", or "in an era"
- Don't overuse adjectives. Sometimes a presentation is just a presentation, not a "glouriously energetic mind-blowing presentation"

How to respond:
- If the abstract follows the rules, say "✅ Perfect abstract!"
- If the abstract doesn't follow the rules, provide feedback on what needs to be improved. Explain how the rule was violated. Start the feedback with "❌ The abstract is not perfect because..."
"""

criticAgent = ConversableAgent(
    name="critic",
    system_message=systemMessage,
    llm_config=llm_config,
    human_input_mode="NEVER",
)
