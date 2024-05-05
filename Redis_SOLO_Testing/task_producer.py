import redis
import json
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)


def enqueue_task(task_name, *args):
    # Serialize the task data as JSON
    task_data = json.dumps((task_name, args))
    r.lpush('task_queue', task_data)


def wait_for_result(task_id):
    while True:
        result = r.get(task_id)
        if result:
            return result.decode()
        time.sleep(1)  # Polling interval


def main():
    # Attempt to connect to Redis
    try:
        # Test writing and reading
        r.set('test', 'value')
        value = r.get('test')
        print(f"Redis is working! Retrieved value: {value.decode()}")
    except (redis.exceptions.ConnectionError, Exception) as e:
        print(f"Failed to connect or read/write to Redis: {e}")

    print("Scheduling 'first_task' with input 'Test input'")
    enqueue_task('first_task', 'Test input')
    task_id = 'first_task_result'
    print("Waiting for 'first_task' to complete...")
    result = wait_for_result(task_id)
    print(f"Result: {result}")

    print("Scheduling 'create_snake'")
    enqueue_task('create_snake')
    task_id = 'create_snake_result'
    print("Waiting for 'create_snake' to complete...")
    result = wait_for_result(task_id)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
