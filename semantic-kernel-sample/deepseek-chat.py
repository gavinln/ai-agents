import asyncio
import logging

from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.utils.logging import setup_logging


def list_all_loggers():
    # Get the dictionary of all loggers
    loggers = logging.Logger.manager.loggerDict

    print("Existing loggers:")
    for name, logger in loggers.items():
        if not isinstance(logger, logging.PlaceHolder):
            print(f"- {name} (level: {logging.getLevelName(logger.level)})")
        else:
            print(f"- {name} (placeholder)")


async def main2():
    # Initialize the kernel
    kernel = Kernel()

    # Set the logging level for  semantic_kernel.kernel to DEBUG.

    list_all_loggers()
    setup_logging()
    # list_all_loggers()

    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Create a history of the conversation
    history = ChatHistory()

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        print(history)


async def main():
    chat_service = OpenAIChatCompletion(
        ai_model_id="deepseek-chat",  # or "deepseek-reasoner"
        async_client=AsyncOpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        ),
    )

    chat_history = ChatHistory()
    chat_history.add_user_message("Hello, how are you?")

    response = await chat_service.get_chat_message_content(
        chat_history, OpenAIChatPromptExecutionSettings()
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
