import os

import fire
from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAIChatPromptExecutionSettings,
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


async def streaming_chat():
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

        response = chat_service.get_streaming_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        print("Assistant > ", end="")
        chunks = []
        async for chunk in response:
            print(chunk, end="")
            chunks.append(str(chunk))
        print()

        history.add_assistant_message("".join(chunks))



def main():
    fire.Fire(
        {
            "hello": hello,
            "chat": chat,
            "streaming-chat": streaming_chat,
        }
    )


if __name__ == "__main__":
    main()
