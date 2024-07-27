# Autogen Abstract Creator

This is overkill for an abstract creation tool, but a very fun application of the [Autogen][1] framework. 

## Overview

The Autogen Abstract Creator leverages multiple agents to collaboratively generate, critique, and refine presentation abstracts. The agents involved include:

- **Writer Agent**: Expert in crafting presentation abstracts by asking a series of questions and using the answers to create compelling abstracts.
- **Human Agent**: Acts as the presenter, providing input for the session abstract.
- **Critic Agent**: Reviews the abstract for adherence to specific writing rules and provides feedback.
- **Content Editor Agent**: Ensures that all questions are answered in the abstract and provides a detailed review.
- **Group Chat Manager**: Manages the interaction between all agents to facilitate the abstract creation process.

## Configuration

The agents are configured to use the GPT-4o model via Azure OpenAI services. The configuration details are specified in each agent's respective file.

## Usage

To initiate the abstract creation process, the `humanAgent` starts a chat session with the message "Let's start writing then, shall we?" The `GroupChatManager` coordinates the interaction between the agents to produce a refined abstract.

## Installation

1. Clone the repository.
1. Install the required dependencies.
1. Set the `AZURE_OPENAI_API_KEY` environment variable with your Azure OpenAI API key.
1. Set the `AZURE_OPENAI_ENDPOINT` environment variable with your Azure OpenAI endpoint.
1. Run the `abstracts.py` script to start the abstract creation process.

[1]: https://microsoft.github.io/autogen/
