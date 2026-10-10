from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from mysite.firebase_client import get_firestore_client

db = get_firestore_client()

# --- CREATE (Insert) ---
def create_task(project_id: int, title: str, assigned_to: str, priority="medium") -> str:
    """Inserts a new task document into the Firestore 'tasks' collection."""
    doc_ref = db.collection("tasks").document()
    doc_ref.set({
        "project_id": int(project_id),
        "title": title,
        "assigned_to": assigned_to,
        "status": "todo",
        "priority": priority,
        "created_at": datetime.utcnow(),
    })
    return doc_ref.id

def add_task_comment(task_id: str, author: str, comment: str) -> str:
    """Inserts a related record into the 'task_comments' collection."""
    doc_ref = db.collection("task_comments").document()
    doc_ref.set({
        "task_id": task_id,
        "author": author,
        "comment": comment,
        "created_at": datetime.utcnow(),
    })
    return doc_ref.id

# --- READ (Query & Filter) ---
def get_tasks_for_project(project_id: int, status_filter=None):
    """Queries tasks for a project, with optional status filtering."""
    query = db.collection("tasks").where(filter=FieldFilter("project_id", "==", int(project_id)))
    
    if status_filter and status_filter != "all":
        query = query.where(filter=FieldFilter("status", "==", status_filter))

    tasks = []
    for doc in query.stream():
        data = doc.to_dict()
        data["id"] = doc.id
        tasks.append(data)
    return tasks

# --- UPDATE (Modify) ---
def update_task_status(task_id: str, new_status: str):
    """Modifies the status of an existing task document."""
    task_ref = db.collection("tasks").document(task_id)
    task_ref.update({
        "status": new_status,
        "updated_at": datetime.utcnow(),
    })

# --- DELETE ---
def delete_task(task_id: str):
    """Deletes a task and cascades delete to child comments."""
    comments = db.collection("task_comments").where(
        filter=FieldFilter("task_id", "==", task_id)
    ).stream()
    for comment in comments:
        db.collection("task_comments").document(comment.id).delete()

    db.collection("tasks").document(task_id).delete()