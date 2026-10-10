# Overview

As a software engineer, my goal with this project is to deepen my understanding of full-stack web development, hybrid database architectures, relational schema design, and cloud database integration using Django, PostgreSQL, and Google Cloud Firestore. I wanted to learn how to enforce referential integrity across relational entities, design scalable document-oriented schemas in NoSQL, and implement complete CRUD workflows across both traditional and cloud database engines within a modern Model-View-Template (MVT) architecture.

Unitivity is a collaborative project management and discovery web platform designed to connect creators with contributors across multidisciplinary initiatives. Users can explore various project ideas on a dynamic Discovery Feed, review platform-wide analytics, filter initiatives by creation date, join project teams with a single click, participate in threaded discussions, manage personal profiles, and coordinate real-time development tasks through a cloud document store.

I wrote this software to demonstrate how to model multi-table relational databases, execute structured SQL operations (Insert, Select, Update, Delete, Joins, Aggregates) using PostgreSQL, and integrate a cloud-hosted NoSQL document database (Google Cloud Firestore) using the Python Firebase Admin SDK to handle real-time task tracking with foreign-collection relationships.

[Software Demo Video - Module 1](https://youtu.be/58SHd3aTunI)  
[Software Demo Video - Module 2 (Relational Database)](https://youtu.be/ruZhG0zNs_4)  
[Software Demo Video - Module 3 (Cloud Database)](https://youtu.be/wvKRv_9Mu4k)

---

# Cloud Database (Google Cloud Firestore)

Unitivity leverages **Google Cloud Firestore** (Standard Edition, multi-region `nam5`) as its distributed cloud database. Firestore operates as a NoSQL document store to manage agile project tasks and child task comments, connecting securely through the Python Firebase Admin SDK (`firebase-admin`) using service account credentials.

### Data Model & Related Collections
To demonstrate cloud database modeling and relational patterns in NoSQL, the Firestore instance maintains two linked collections:

* **`tasks` (Parent Collection):**
  * `id`: Document ID (Auto-generated unique identifier)
  * `project_id`: Integer referencing the relational `Project.id` (foreign key equivalent)
  * `title`: String (Task title/summary)
  * `assigned_to`: String (Username of the assigned team member)
  * `status`: String (`"todo"`, `"in_progress"`, `"done"`)
  * `priority`: String (`"low"`, `"medium"`, `"high"`)
  * `created_at`: UTC Timestamp
* **`task_comments` (Child Collection - Related Table):**
  * `id`: Document ID (Auto-generated unique identifier)
  * `task_id`: String foreign key referencing the parent `tasks` document ID
  * `author`: String (Commenter username)
  * `comment`: String (Message body)
  * `created_at`: UTC Timestamp

### Demonstrated Cloud Database Operations
* **INSERT (Create):**
  * `create_task()` initializes an auto-generated document reference and executes `.set({...})` to insert a new document into the `tasks` collection.
  * `add_task_comment()` writes a child document into `task_comments` linked by `task_id`.
* **READ / QUERY (Retrieve & Filter):**
  * `get_tasks_for_project()` queries the `tasks` collection using `FieldFilter("project_id", "==", project_id)`.
  * Status filtering dynamically chains a second `FieldFilter("status", "==", status_filter)` to retrieve filtered task subsets.
* **UPDATE (Modify):**
  * `update_task_status()` targets the exact document via `.document(task_id)` and calls `.update({"status": new_status, "updated_at": ...})` to modify task states without mutating unchanged fields.
* **DELETE (Remove & Cascade):**
  * `delete_task()` queries and deletes all dependent child records in `task_comments` where `task_id == doc.id`, then removes the primary document from `tasks` using `.delete()`.

---

# Relational Database (PostgreSQL)

The core application data utilizes **PostgreSQL** (`unitivity_db`) connected via the `psycopg2` database driver. All table structures, constraints, and relationships are managed through Django's relational ORM.

### Database Schema & Tables
The relational schema maintains strict referential integrity across five core tables:

* **`auth_user`**: Django's native authentication table storing user credentials, primary keys (`id`), and identity information.
* **`core_profile`**: Linked via a **One-to-One Foreign Key** (`user_id`) to `auth_user`. Stores professional metadata including `role`, `bio`, and timestamp attributes.
* **`core_project`**: Stores project initiatives (`id`, `title`, `description`, `timeline`, `progress`, and `created_at`). Linked via a **Many-to-One Foreign Key** (`creator_id`) referencing `auth_user.id`.
* **`core_comment`**: Linked via **Foreign Keys** to both `core_project.id` (`project_id`) and `auth_user.id` (`author_id`) to support threaded discussions.
* **Junction Tables (Many-to-Many Relationships):**
  * `core_project_collaborators`: Relational junction table mapping many-to-many memberships between users and projects (`project_id`, `user_id`).
  * `core_project_likes`: Relational junction table tracking unique user likes per project.

### Demonstrated SQL Operations
* **INSERT (Create):**
  * `Project.objects.create(...)` executes `INSERT INTO core_project ...` when publishing a new initiative.
  * `Comment.objects.create(...)` executes `INSERT INTO core_comment ...` when posting feedback.
* **SELECT & Multi-Table JOINs (Read):**
  * Discovery Feed retrieval utilizes `select_related('creator')` (compiling to a SQL `INNER JOIN` against `auth_user`) and `prefetch_related(...)` to eliminate N+1 query bottlenecks when loading collaborator rosters.
* **UPDATE (Modify):**
  * Profile modifications execute `UPDATE auth_user ...` and `UPDATE core_profile ...`.
  * Project likes and team joins dynamically insert or remove rows within the respective relational junction tables.
* **DELETE (Remove):**
  * Deleting a comment issues `DELETE FROM core_comment WHERE id = %s`.
  * Deleting a project issues `DELETE FROM core_project WHERE id = %s`, which cascades to remove dependent comments and junction table entries.
* **Aggregate Functions (`AVG` & `COUNT`):**
  * Evaluated across numerical progress data using `Project.objects.aggregate(Avg('progress'), Count('id'))`, compiling to:
    ```sql
    SELECT AVG("core_project"."progress") AS "avg_progress",
           COUNT("core_project"."id") AS "total_projects"
    FROM "core_project";
    ```
* **Date Range Query Filtering:**
  * Dynamic timestamp filtering using `created_at__gte=cutoff`, compiling into:
    ```sql
    SELECT ... FROM "core_project"
    WHERE "core_project"."created_at" >= 'YYYY-MM-DD HH:MM:SS+00:00';
    ```

---

# Web Pages & Routing

The application is structured around several core pages and dynamic views:

* **Discovery Feed (`/`):** The primary landing page featuring project cards, platform-wide aggregate statistics (Total Projects and Average Progress), and date-based filtering controls (All Time, Past 30 Days, Past 7 Days).
* **Project Creation Form (`/project/new/`):** A form view allowing authenticated users to insert new project records into PostgreSQL with initial timelines and progress values.
* **Project Detail Page (`/project/<int:project_id>/`):** Provides a comprehensive breakdown of a specific project, including description, active collaborators, threaded relational comments, and an integrated **Cloud Firestore Task Board**.
* **Cloud Task Action Endpoints:**
  * `POST /project/<int:project_id>/task/create/`: Inserts a new task document into Cloud Firestore.
  * `POST /project/<int:project_id>/task/<str:task_id>/update/`: Modifies task workflow status in Cloud Firestore.
  * `POST /project/<int:project_id>/task/<str:task_id>/delete/`: Removes the task document and associated comments from Cloud Firestore.
* **User Profile Page (`/profile/`):** Displays user information and provides form controls to modify and persist display names, professional roles, and biographies.

---

# Development Environment

* **Development Tools:** Visual Studio Code, Git, GitHub, macOS Terminal
* **Languages & Frameworks:** Python 3.14 / 3.12, Django 5.x / 6.x, HTML5, CSS3
* **Cloud Database & SDK:** Google Cloud Firestore (Standard Edition), `firebase-admin`
* **Relational Database & Driver:** PostgreSQL 16 (or local SQLite during testing), `psycopg2-binary`

---

# Useful Websites

* [Firebase Admin SDK for Python Documentation](https://firebase.google.com/docs/admin/setup)
* [Google Cloud Firestore Documentation](https://cloud.google.com/firestore/docs)
* [Django Documentation - Making Database Queries](https://docs.djangoproject.com/en/stable/topics/db/queries/)
* [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
* [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

# Future Work

In the spirit of continuous iteration and software improvement, planned future enhancements include:

* **Real-Time Client Snapshots:** Integrate Firebase Web Client SDK listeners (`onSnapshot`) to update the task board instantaneously in the browser without full HTTP page reloads.
* **Real-Time Notifications & Activity Feed:** Implement WebSocket support via Django Channels so collaborators receive instant in-app alerts when teammates join or change task states.
* **Advanced Multi-Tag Querying:** Enhance Firestore and PostgreSQL queries with compound indexes to filter initiatives simultaneously by tech stack, difficulty, and phase.
* **Automated Cloud Backups:** Schedule automated exports of Firestore collections to Google Cloud Storage alongside PostgreSQL `pg_dump` routines.