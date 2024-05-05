import redis
import json
import networkx as nx
import logging
from threading import Thread
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to Redis
r = redis.Redis()

# Graph to manage tasks
dag = nx.DiGraph()


def add_task_to_dag(task_id, dependencies=None):
    """
    Adds a task to the DAG with optional dependencies.
    """
    dag.add_node(task_id)
    if dependencies:
        for dependency in dependencies:
            dag.add_edge(dependency, task_id)
            logging.info(f"Added edge from {dependency} to {task_id}")


def execute_task(task_id):
    """
    Simulate task execution.
    """
    logging.info(f"Executing task {task_id}")
    time.sleep(1)  # Simulate some work
    logging.info(f"Task {task_id} completed")
    return f"{task_id} completed"


def process_tasks():
    """
    Process tasks according to the DAG order.
    """
    for task in nx.topological_sort(dag):
        r.lpush('task_queue', task)
        logging.info(f"Task {task} pushed to queue")


def worker():
    """
    Worker to process tasks from Redis.
    """
    while True:
        task_id = r.brpop(['task_queue'])[1]
        if dag.has_node(task_id):
            execute_task(task_id)
            for successor in dag.successors(task_id):
                in_deg = dag.in_degree(successor)
                if in_deg == 0 or all(dag.nodes[pred]['status'] == 'completed' for pred in dag.predecessors(successor)):
                    r.lpush('task_queue', successor)
        dag.nodes[task_id]['status'] = 'completed'


# Example of setting up a simple DAG and running the system
add_task_to_dag('task1')
add_task_to_dag('task2', ['task1'])
add_task_to_dag('task3', ['task1'])

if __name__ == "__main__":
    Thread(target=process_tasks).start()
    Thread(target=worker).start()
