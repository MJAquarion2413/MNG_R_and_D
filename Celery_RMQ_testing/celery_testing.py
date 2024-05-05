from celery_app import first_task, create_snake

def main():
    # Input to process
    test_input = "Test input"

    # Call the task
    result = first_task.delay(test_input)

    # Retrieve and print the result
    print("Waiting for task to complete...")
    print(f"Result: {result.get(timeout=10)}")  # Adjust the timeout as needed

    print("Task completed!")

    print("Creating snake...")
    result = create_snake.delay()
    print(f"Result: {result.get(timeout=10)}")  # Adjust the timeout as needed


if __name__ == "__main__":
    main()
