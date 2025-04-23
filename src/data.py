from .schemas import Todo

all_todos = [
    Todo(id=1, description='Go outside', priority=1),
    Todo(id=2, description='Study for fun', priority=1),
    Todo(id=3, description='Watch "The Wheel of Time"', priority=3),
    Todo(id=4, description='Go to the gym', priority=2),
    Todo(id=5, description='Hope for the best', priority=1),
]


def get_all_todos():
    """
    Return all_todos.
    Needed specifically for tests, to be able to override real data with test data, when called via FastAPI.
    """
    return all_todos
