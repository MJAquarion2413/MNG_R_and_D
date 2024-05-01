class Task:
    """Encapsulates a callable and its arguments, to be executed by TaskScheduler."""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        """Executes the task using the stored function and arguments."""
        self.func(*self.args, **self.kwargs)
