from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import (
    ChatAgent,
    ChatMessage,
    Executor,
    WorkflowContext,
    handler
)
from pydantic import BaseModel, ConfigDict
from domain.abstract import Abstract

class AbstractWriteExecutor(Executor):
    """
    This executor takes input from the workflow context and uses an agent to generate a response.
    """
    
    agent: ChatAgent
    
    def __init__(self, chat_client: AzureOpenAIChatClient, id: str = "writer"):
        # Create a domain specific agent using your configured AzureChatClient.
        self.agent = chat_client.create_agent(
            instructions=(
                """
                You are an expert in creating presentation abstracts. Our award-winning way of crafting an abstract is to ask a series of questions and use the answers to create a compelling abstract. 
                I will give some examples of abstracts I like. Please match the wording, style and energy of the examples when crafting new ones. These sessions will be presented at tech conferences.
                Always return the output in JSON format, with the keys "title" and "abstract".

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
                {
                "title": "Code-First LLMOps With Azure AI & Prompty",
                "abstract": "In this session, you will learn how to select the right LLM for your needs, start programming with an LLM, and monitor your production LLM interactions. We'll explore the entire LLMOps journey, from selecting the right model to writing your first prompt, developing locally, and deploying to production using Azure OpenAI, Prompt Flow/Semantic Kernel, and Microsoft's new Prompty extension.\n\nThis session is ideal for developers interested in LLMs. Expect many practical demos and leave with the knowledge to start using Prompty to develop anything!"
                }
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
                {
                "title": "Automating Content Generation with GitHub Actions & Azure AI",
                "abstract": "In this session, you will learn how to harness the power of GitHub automation for content generation, leveraging GitHub Actions and Azure AI Services. Discover the role of human review and oversight in reviewing GenAI output and how to chain different forms of GenAI to create unique content. We'll explore a practical example of creating self-guided meditations using GPT-4, Azure AI Speech, and DALL-E 3.\n\nThis session is ideal for developers and anyone interested in automation. Expect many practical demos, including using GitHub Actions to automatically create PRs and integrating Azure AI services into your pipeline."
                }

                ```
                Input:
                ### 1. Who do you think this talk is for?

                This talk is for anyone interested in generative AI and how we work with it.

                ### 2. What do you think you'll learn from this talk?

                In this talk you will learn what automation bias is. You'll learn that it's important to be aware of this flaw that most humans share, as it can cause mistakes at work, impacting many people. You'll learn how to increase your awareness, and some tricks to reduce your bias. I'll also teach how you can reduce the bias by including more automation. You'll learn that this bias occurs when generating text, images, as well as code. You'll see examples in a live demo too.

                ### 3. What's something you'll be able to accomplish with the information gained from this talk?

                You'll become more aware of your bias and change your relationship with genai as a result.

                ### 4. What is the two-sentence summary of the talk?
                    
                The real danger with generative AI is automation bias, a form of cognitive bias that most modern humans suffer from. In this talk we'll explore why and how we're so ready to accept machine-generated content, and how we can arm ourselves against it.

                Output:
                {
                "title": "Toxic Trust: The Psychology of Automation Bias in Generative AI",
                "abstract": "In this session, explore the hidden dangers of automation bias in the realm of generative AI—a cognitive trap where we too readily trust machine-generated content. We'll examine the psychological aspects of this bias, its impact on text, images, and code, and provide actionable strategies for increasing your awareness and reducing your bias. Expect a live demo showcasing practical examples and innovative approaches to transform your interaction with generative AI.\n\nThis talk is ideal for anyone interested in generative AI and how we work with it. Come prepared to challenge your assumptions and change your relationship with AI."
                }
                ```
                ## What to avoid
                - Never discriminate against any group of people
                - Never use the words "delve", "equip", "empower", "navigate", "landscape", "enhance", "delve", "insight".
                - Avoid terms like "in a world", or "in an era"
                """
            ),
        )
        # Associate the agent with this executor node. The base Executor stores it on self.agent.
        super().__init__(agent=self.agent, id=id)
        
    @handler
    async def handle(self, message: ChatMessage, ctx: WorkflowContext[list[ChatMessage], str]) -> None:
        """Generate content using the agent and forward the updated conversation.

        Contract for this handler:
        - message is the inbound user ChatMessage.
        - ctx is a WorkflowContext that expects a list[ChatMessage] to be sent downstream.

        Pattern shown here:
        1) Seed the conversation with the inbound message.
        2) Run the attached agent to produce assistant messages.
        3) Forward the cumulative messages to the next executor with ctx.send_message.
        """
        # Start the conversation with the incoming user message.
        messages: list[ChatMessage] = [message]
        # Run the agent and extend the conversation with the agent's messages.
        response = await self.agent.run(messages, temperature=0.5, max_tokens=3000, response_format=Abstract)
        if isinstance(response.value, Abstract):
            abstract = response.value
        
        await ctx.yield_output(response.text)
        
        messages.extend(response.messages)
        # Forward the accumulated messages to the next executor in the workflow.
        await ctx.send_message(messages)
