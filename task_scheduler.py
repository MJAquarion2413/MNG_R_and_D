from PySide6.QtCore import QObject, Signal, Slot

from task import Task


class TaskScheduler(QObject):
    taskReady = Signal(Task)

    def __init__(self):
        super().__init__()
        self.taskReady.connect(self.execute_task)

    @Slot(Task)
    def execute_task(self, task):
        """Slot to execute a Task when emitted by taskReady signal."""
        task.execute()
        print("Task executed")

    def schedule_task(self, task):
        """Schedules a Task for execution by emitting the taskReady signal with the Task."""
        self.taskReady.emit(task)
