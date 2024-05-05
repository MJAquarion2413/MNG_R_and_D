import redis
import json
import time

r = redis.Redis()


def first_task(arg):
    result = f"Processed {arg}"
    r.set('first_task_result', result)
    return result


def create_snake():
    result = "Snake created"
    r.set('create_snake_result', result)
    return result


def process_task():
    while True:
        _, task_data = r.brpop(['task_queue'])
        task_name, args = json.loads(task_data)
        if task_name == 'first_task':
            first_task(*args)
        elif task_name == 'create_snake':
            create_snake()


if __name__ == "__main__":
    process_task()
