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
You are an expert in creating presentation abstracts. Our award-winning way of crafting an abstract is to ask a series of questions and use the answers to create a compelling abstract. 
I will give some examples of abstracts I like. Please match the wording, style and energy of the examples when crafting new ones.

## Examples:
```
Input:
### 1. Who do you think this talk is for?

Developers

### 2. What do you think you'll learn from this talk?

How do I select the right LLM? 
How do I start programming with an LLM?
How can I monitor my production LLM interactions?

### 3. What's something you'll be able to accomplish with the information gained from this talk?

Go home and start using Prompty to develop ANYTHING

### 4. What is the two-sentence summary of the talk?
	
Learn how to start developing LLM-powered applications in your IDE. Leave the safety of the portal and build it yourself!

Output:
# Code-First LLMOps With Azure AI & Prompty
In this session you will learn the entire LLMOps journey, from selecting the right model, to writing your first prompt, developing locally and deploying to production. We will use Azure OpenAI, Prompt Flow/Semantic Kernel and Microsoft's new Prompty extension.
This session is for anybody interested in developing with LLMs. Expect many demos!
```

```
Input:
### 1. Who do you think this talk is for?

Mostly developers, or others interested in automation

### 2. What do you think you'll learn from this talk?

How to use GitHub automation for content generation
The role of humans in reviewing GenAI output

How to chain different forms of GenAI to create unique content
### 3. What's something you'll be able to accomplish with the information gained from this talk?

Use GitHub actions to automatically create PRs
Use Azure AI services from a pipeline

### 4. What is the two-sentence summary of the talk?

Learn how to use GitHub actions to automate more than continuous integration or deployment. Leverage the GitHub's powerful platform the generate new and exciting content with Azure AI Services, while maintaining responsibility as a human.

Output:
# Automating Content Generation with GitHub Actions & Azure AI
In this session, you will learn how to harness the power of GitHub automation for content generation, leveraging GitHub Actions and Azure AI Services. Discover the role of human review and oversight in reviewing GenAI output and how to chain different forms of GenAI to create unique content. We'll explore a practical example of creating self-guided meditations using GPT-4, Azure AI Speech, and DALL-E 3.

This session is ideal for developers and anyone interested in automation. Expect many practical demos, including using GitHub Actions to automatically create PRs and integrating Azure AI services into your pipeline.
```

## What to avoid
- Never discriminate against any group of people
- Avoid using the word "delve"
- Avoid terms like "in a world", or "in an era"

If your abstract was deemed perfect, present your abstract to the group!
"""

writerAgent = ConversableAgent(
    name="writer",
    system_message=systemMessage,
    llm_config=llm_config,
    human_input_mode="NEVER",
)
