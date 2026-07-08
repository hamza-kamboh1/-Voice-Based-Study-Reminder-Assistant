from typing import List, Dict, Optional
from models.task import Task
from utils.logger import logger

# In-memory task storage
_tasks: List[Task] = []

def add_study_task(title: str, due_date: Optional[str] = None) -> str:
    """Add a new study task"""
    task = Task(title=title, due_date=due_date)
    _tasks.append(task)
    logger.info(f"Added task: {title}")
    return f"I added '{title}' to your study tasks{f' for {due_date}' if due_date else ''}."

def list_study_tasks() -> str:
    """List all study tasks"""
    if not _tasks:
        return "You have no study tasks."
    
    pending = [t for t in _tasks if not t.completed]
    completed = [t for t in _tasks if t.completed]
    
    response = "Here are your study tasks:"
    if pending:
        response += f"\nPending ({len(pending)}):"
        for task in pending:
            due = f" (due: {task.due_date})" if task.due_date else ""
            response += f"\n  - {task.title}{due}"
    if completed:
        response += f"\nCompleted ({len(completed)}):"
        for task in completed:
            response += f"\n  - {task.title}"
    return response

def complete_study_task(task_name: str) -> str:
    """Mark a task as completed"""
    for task in _tasks:
        if task.title.lower() == task_name.lower() and not task.completed:
            task.mark_completed()
            logger.info(f"Completed task: {task.title}")
            return f"Done. I marked '{task.title}' as completed."
    return "I could not find that task to mark as completed."

def delete_study_task(task_name: str) -> str:
    """Delete a study task"""
    for i, task in enumerate(_tasks):
        if task.title.lower() == task_name.lower():
            deleted = _tasks.pop(i)
            logger.info(f"Deleted task: {deleted.title}")
            return f"I deleted '{deleted.title}' from your study tasks."
    return "I could not find that task to delete."

# Export tools for the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_study_task",
            "description": "Add a new study task. Use this when the user mentions adding, creating, or scheduling a study task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title or description of the study task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "The due date of the task (e.g., 'tomorrow', 'next week')"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_study_tasks",
            "description": "List all study tasks. Use this when the user asks what tasks they have or wants to see their study tasks.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_study_task",
            "description": "Mark a task as completed. Use this when the user says they finished, completed, or done with a study task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "The name or title of the task to mark as completed"
                    }
                },
                "required": ["task_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_study_task",
            "description": "Delete a study task. Use this when the user wants to remove or delete a study task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "The name or title of the task to delete"
                    }
                },
                "required": ["task_name"]
            }
        }
    }
]