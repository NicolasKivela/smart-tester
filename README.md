# smart-tester
Smart testing tool for software engineering project course.


##  Getting Started

### 1. Clone the Repository

   

### 2. Run with Docker
Download docker desktop
Build the containers:
    docker compose build

Start the containers:
    docker compose up

The service should now be running locally.

---

##  Usage

- API documentation: http://localhost:8000/docs

---
#  Branching Rules

## Main Branches
- main → production-ready
- dev → integration branch for new work

## Feature Branches
- feature/<frontend|backend>-<short-name>
  Example: feature/frontend-auth-ui

## Fix Branches
- fix/<frontend|backend>-<short-name>
  Example: fix/backend-db-connection

## Hotfix Branches
- hotfix/<short-name>
  Example: hotfix/backend-critical-bug
