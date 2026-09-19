# Overview

As a software engineer, my goal with this project is to deepen my understanding of full-stack web development using the Django framework. I wanted to learn how to design dynamic database models, set up clean URL routing, structure reusable templates, and seamlessly integrate static CSS assets into a Python web application.

Unitivity is a web platform designed to connect project creators with collaborators. Users can explore various project ideas on a Discovery Feed, support ideas by liking them, join project teams with a single click, view dedicated project detail pages with progress tracking, and manage their personal profiles.

I created this software to practice building clean, scalable Model-View-Template (MVT) web architecture and to refine my frontend CSS layout skills within a modern web framework.

[Software Demo Video](https://youtu.be/58SHd3aTunI)

# Web Pages

The application is structured around several core pages and dynamic views:

* **Discovery Feed (`/` or `/projects/`):** The primary landing page featuring project cards. Displays project titles, brief descriptions, creator details, like counts, and dynamic action buttons to join or like projects directly from the feed.
* **Project Detail Page (`/projects/<int:pk>/`):** Provides a comprehensive breakdown of a specific project, including full project descriptions, visual progress indicators/status bars, roster of active team members, and open collaborator roles.
* **Project Creation / Edit Form (`/projects/create/`):** A form-based view allowing authenticated users to define project parameters, goals, required skills, and deadlines.
* **User Profile Page (`/profile/<username>/`):** Displays user information, bio, projects created, and teams the user has joined across the platform.

# Development Environment

* **Development Tools:** Visual Studio Code, Git, GitHub, macOS Terminal
* **Languages & Frameworks:** Python 3, Django 6, HTML5, CSS3

# Useful Websites

* [Django Documentation - Static Files](https://docs.djangoproject.com/en/6.1/howto/static-files/)
* [Django Documentation - Templates & MVT Layout](https://docs.djangoproject.com/en/6.1/topics/templates/)
* [MDN Web Docs - CSS Flexbox & Layouts](https://developer.mozilla.org/en-US/docs/Learn/CSS)

# Future Work

In the spirit of Kaizen and continuous iteration, planned improvements and feature expansions include:

* **Real-Time Notifications & Activity Feed:** Implement WebSocket support via Django Channels so collaborators receive live notifications when team members join or post updates.
* **Direct Messaging / Team Discussion Boards:** Add in-app communication channels for project teams to coordinate tasks directly on the platform.
* **Advanced Search and Tag Filtering:** Enhance the Discovery Feed with multi-tag filtering (e.g., tech stack, project stage, needed roles) and full-text keyword search.
* **Role-Based Permissions:** Refine access controls so project creators can review join requests, assign administrative privileges, or designate custom team roles.
* **Automated Testing Suite:** Expand coverage with Django unit and integration tests for model validations, view responses, and form submissions.
