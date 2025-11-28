import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from agent_framework import WorkflowBuilder
from agent_framework import ChatMessage, WorkflowOutputEvent, AgentRunUpdateEvent
from agent_framework import Role
from azure.identity import AzureCliCredential
from executors.abstract_writer import AbstractWriteExecutor
from executors.content_reviewer import ContentReviewer

async def main():
    # 1) Create agents using AzureChatClient
    chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())

    abstractWriter = AbstractWriteExecutor(chat_client=chat_client)

    reviewer = ContentReviewer(chat_client=chat_client)

    # Build the workflow using the fluent builder.
    # Set the start node and connect an edge from writer to reviewer.
    workflow = (WorkflowBuilder()
        .set_start_executor(abstractWriter)
        .add_edge(abstractWriter, reviewer)
        .build())


    # Run the workflow with the user's initial message.
    # For foundational clarity, use run (non streaming) and print the workflow output.
    events = await workflow.run(
        ChatMessage(role="user", text=
                    """
                    ### 1. Who do you think this talk is for?
                    
                    This talk is for developers and IT professionals who want to know how to help their companies create content of high quality

                    ### 2. What do you think you'll learn from this talk?
                    
                    You will learn why people are becoming increasingly worried or annoyed by "AI slop", low-quality genAI content. I'll teach you how you can build automated systems that can generate content that keep in mind that humans have great trouble reviewing automated output because of our automation bias. I'll teach you what signs to look out for when creating this type of content. I'll use the example of session abstract generation.

                    ### 3. What's something you'll be able to accomplish with the information gained from this talk?
                    
                    You'll be able to implement all the guidlines and tricks I propose.

                    ### 4. What is the two-sentence summary of the talk?
                    
                    Title along the lines of: wrtite drunk edit sober: responsible generated content
                    The world is hard at work to include genAI generated content into our jobs, news items and private life. This AI-slop is easy to spot, but can we do better? I'll show ways to automate the generation of high-quality content, by putting in some old-fashioned elbow grease.
                    """)
    )
    # The terminal node yields output; print its contents.
    outputs = events.get_outputs()
    # Print all the outputs from the workflow.
    if outputs:
        for output in outputs:
            print("Workflow output:", output)


if __name__ == "__main__":
    asyncio.run(main())
