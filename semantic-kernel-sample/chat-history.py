"""
https://learn.microsoft.com/en-us/semantic-kernel/concepts/ai-services/chat-completion/chat-history?pivots=programming-language-python
"""

import os

import fire
from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.contents import (
    AuthorRole,
    ChatMessageContent,
    FunctionCallContent,
    FunctionResultContent,
    ImageContent,
    TextContent,
)
from semantic_kernel.contents.chat_history import ChatHistory


def get_chat_service():
    # Get API key from environment variable
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    if not DEEPSEEK_API_KEY:
        raise ValueError("Please set DEEPSEEK_API_KEY environment variable")

    chat_service = OpenAIChatCompletion(
        ai_model_id="deepseek-chat",
        async_client=AsyncOpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        ),
    )
    return chat_service


async def hello():
    chat_service = get_chat_service()
    execution_settings = OpenAIChatPromptExecutionSettings()

    chat_history = ChatHistory()
    chat_history.add_user_message("Hello, how are you?")

    response = await chat_service.get_chat_message_content(
        chat_history, execution_settings
    )
    print(response)


async def chat():
    kernel = Kernel()
    chat_service = get_chat_service()
    execution_settings = OpenAIChatPromptExecutionSettings()
    history = ChatHistory()

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        print("-----" * 8)
        userInput = input("User (exit to end) > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        history.add_user_message(userInput)

        response = await chat_service.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        print("Assistant > " + str(response))
        history.add_message(response)


def print_chat_history(chat_history: ChatHistory):
    """Displays the ChatHistory messages in a formatted way"""
    print("----- Chat History -----")
    for i, message in enumerate(chat_history.messages):
        print(f"{i}. {message.role.upper()}:")
        for item in message.items:
            if item.content_type == "text":
                print("text", item.text)
            elif item.content_type == "function_call":
                print("function_call", item.name)
            elif item.content_type == "function_result":
                print("function_result", item.result)
            elif item.content_type == "image":
                print("image", item.uri)
            else:
                assert False, f"Unknown content type {item.content_type}"
    print("------------------------")


def history_example():
    # Create a chat history object
    chat_history = ChatHistory()

    chat_history.add_system_message("You are a helpful assistant.")
    chat_history.add_user_message("What's available to order?")
    chat_history.add_assistant_message(
        "We have pizza, pasta, and salad available to order. What would you like to order?"
    )
    chat_history.add_user_message("I'd like to have the first option, please.")

    # Add user message with an image
    chat_history.add_message(
        ChatMessageContent(
            role=AuthorRole.USER,
            name="Laimonis Dumins",
            items=[
                TextContent(text="What available on this menu"),
                ImageContent(uri="https://example.com/menu.jpg"),
            ],
        )
    )
    print_chat_history(chat_history)


def history_functions():
    chat_history = ChatHistory()
    chat_history.add_message(
        ChatMessageContent(
            role=AuthorRole.ASSISTANT,
            items=[
                FunctionCallContent(
                    name="get_user_allergies",
                    id="0001",
                    arguments=str({"username": "laimonisdumins"}),
                ),
            ],
        )
    )

    # Add a simulated function results from the tool role
    chat_history.add_message(
        ChatMessageContent(
            role=AuthorRole.TOOL,
            items=[
                FunctionResultContent(
                    name="get_user_allergies",
                    id="0001",
                    result='{ "allergies": ["peanuts", "gluten"] }',
                )
            ],
        )
    )
    print_chat_history(chat_history)


def main():
    fire.Fire(
        {
            "history-example": history_example,
            "history-functions": history_functions,
        }
    )


if __name__ == "__main__":
    main()
