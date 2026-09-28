# Overview

As a software engineer, my goal with this project is to deepen my understanding of full-stack web development and relational database management using Django and PostgreSQL. I wanted to learn how to design normalized relational database schemas, enforce referential integrity across related entities, build dynamic SQL queries, and implement complete CRUD functionality within a modern Model-View-Template (MVT) architecture.

Unitivity is a collaborative project management and discovery web platform designed to connect creators with contributors across multidisciplinary initiatives. Users can explore various project ideas on a dynamic Discovery Feed, review platform-wide analytics, filter initiatives by creation date, join project teams with a single click, participate in threaded discussions, and manage their personal profiles.

I wrote this software to demonstrate how to model multi-table relational databases, execute structured database operations (Insert, Select, Update, Delete), perform multi-table joins, and calculate statistical aggregates on numerical data using a PostgreSQL backend.

[Software Demo Video](https://youtu.be/58SHd3aTunI)
[Software Demo Video Module 2](https://youtu.be/ruZhG0zNs_4)

# Relational Database

The application utilizes **PostgreSQL** (`unitivity_db`) hosted locally and connected via the `psycopg2` database driver. All table structures, constraints, and relationships are managed through Django's relational ORM.

### Database Schema & Tables
The database maintains strict referential integrity across five core relational tables:

* **`auth_user`**: Django's native authentication table storing user credentials, primary keys (`id`), and identity information.
* **`core_profile`**: Linked via a **One-to-One Foreign Key** (`user_id`) to `auth_user`. Stores professional metadata including `role`, `bio`, and timestamp attributes.
* **`core_project`**: Stores project initiatives (`id`, `title`, `description`, `timeline`, `progress`, and `created_at`). Linked via a **Many-to-One Foreign Key** (`creator_id`) referencing `auth_user.id`.
* **`core_comment`**: Linked via **Foreign Keys** to both `core_project.id` (`project_id`) and `auth_user.id` (`author_id`) to support threaded discussions.
* **Junction Tables (Many-to-Many Relationships)**:
  * `core_project_collaborators`: Relational junction table mapping many-to-many memberships between users and projects (`project_id`, `user_id`).
  * `core_project_likes`: Relational junction table tracking unique user likes per project.

### Demonstrated SQL Operations
* **INSERT (Create):**
  * `Project.objects.create(...)` executes an `INSERT INTO core_project ...` statement when publishing a new initiative.
  * `Comment.objects.create(...)` executes an `INSERT INTO core_comment ...` statement when posting feedback.
* **SELECT & Multi-Table JOINs (Read):**
  * Feed retrieval utilizes `select_related('creator')` (compiling to a SQL `INNER JOIN` against `auth_user`) and `prefetch_related(...)` to eliminate N+1 query bottlenecks when loading collaborator rosters.
* **UPDATE (Modify):**
  * Saving profile changes executes `UPDATE auth_user ...` and `UPDATE core_profile ...`.
  * Liking or joining projects dynamically updates rows within the respective relational junction tables (`core_project_likes` and `core_project_collaborators`).
* **DELETE (Remove):**
  * Deleting a comment issues `DELETE FROM core_comment WHERE id = %s`.
  * Deleting a project issues `DELETE FROM core_project WHERE id = %s`, which cascades to remove dependent comments and relationship rows.
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

# Web Pages & Routing

The application is structured around several core pages and dynamic views:

* **Discovery Feed (`/`):** The primary landing page featuring project cards, platform-wide aggregate statistics (Total Projects and Average Progress), and date-based filtering controls (All Time, Past 30 Days, Past 7 Days). Users can like projects, join teams, and read or delete comments.
* **Project Creation Form (`/project/new/`):** A form view allowing authenticated users to insert new project records into the database with initial timelines and progress values.
* **Project Detail Page (`/project/<int:project_id>/`):** Provides a comprehensive breakdown of a specific project, including description, current progress percentage, active collaborator rosters, threaded comments, and a project deletion action for the owner.
* **User Profile Page (`/profile/`):** Displays user information and provides form controls to modify and persist display names, professional roles, and biographies to PostgreSQL.

# Development Environment

* **Development Tools:** Visual Studio Code, Git, GitHub, macOS Terminal
* **Languages & Frameworks:** Python 3.12, Django 5.x / 6.x, HTML5, CSS3
* **Database Management System:** PostgreSQL 16 (Hosted locally via Homebrew)
* **Database Connector:** `psycopg2-binary`

# Useful Websites

* [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
* [Django Documentation - Making Database Queries](https://docs.djangoproject.com/en/stable/topics/db/queries/)
* [Django Documentation - QuerySet Aggregation](https://docs.djangoproject.com/en/stable/topics/db/aggregation/)
* [psycopg2 Documentation](https://www.psycopg.org/docs/)
* [MDN Web Docs - CSS Flexbox & Layouts](https://developer.mozilla.org/en-US/docs/Learn/CSS)

# Future Work

In the spirit of Kaizen and continuous iteration, planned improvements and feature expansions include:

* **Real-Time Notifications & Activity Feed:** Implement WebSocket support via Django Channels so collaborators receive live notifications when team members join or post updates.
* **Direct Messaging / Team Discussion Boards:** Add in-app communication channels for project teams to coordinate tasks directly on the platform.
* **Advanced Search and Tag Filtering:** Enhance the Discovery Feed with multi-tag filtering (e.g., tech stack, project stage, needed roles) and full-text keyword search.
* **Role-Based Permissions:** Refine access controls so project creators can review join requests, assign administrative privileges, or designate custom team roles.
* **Automated Database Backup Routine:** Create a scheduled cron task or Django management command to generate automated PostgreSQL `pg_dump` backups.