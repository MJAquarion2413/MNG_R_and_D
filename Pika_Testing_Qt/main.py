from gui import run
import threading
import orchestrator


def start_orchestrator():
    orchestrator.main()


if __name__ == "__main__":
    # Run orchestrator in a separate thread
    threading.Thread(target=start_orchestrator, daemon=True).start()
    run()
