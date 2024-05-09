import asyncio
from message_handler import start_consumer


async def trigger_action(action):
    print(f"Triggering action: {action['function']}")
    if action['function'] == "activate_widget1":
        await activate_widget1()
    elif action['function'] == "activate_widget2":
        await activate_widget2()


async def activate_widget1():
    await asyncio.sleep(1)  # Simulate some processing time
    print("Widget 1 Activated - Async")


async def activate_widget2():
    await asyncio.sleep(1)  # Simulate some processing time
    print("Widget 2 Activated - Async")


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_consumer(trigger_action))
    loop.close()


if __name__ == "__main__":
    main()
