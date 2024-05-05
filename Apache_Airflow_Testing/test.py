import requests


def trigger_dag(dag_id):
    url = f"http://localhost:8080/api/v1/dags/{dag_id}/dagRuns"
    response = requests.post(url, json={"conf": {}})
    if response.status_code == 200:
        print("DAG triggered successfully")
    else:
        print("Failed to trigger DAG")


trigger_dag('my_dag')
