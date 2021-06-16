from datetime import datetime
from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import Todo


@convert_kwargs_to_snake_case
def resolve_create_todo(self, info, description, due_date):
    try:
        due_date = datetime.strptime(due_date, '%d-%m-%Y').date()
        todo = Todo(description=description, due_date=due_date)
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }

    except ValueError:
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    return payload



@convert_kwargs_to_snake_case
def set_mark_done_todo(self, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        todo.completed = True
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} was not found"]
        }
    return payload
