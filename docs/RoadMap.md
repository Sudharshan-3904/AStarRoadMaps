# 🗺️ Backend Developer Roadmap

> **Goal:** Become a backend developer
> **Skill Level:** Beginner
> **Time Commitment:** 10 hours/week
> **Estimated Duration:** 6 months
> **Generated:** 2026-04-11

---

## 📋 Overview

| Phase | Title | Duration | Topics |
|---|---|---|---|
| 1 | Foundations | Week 1–4 | Python, Linux, Git |
| 2 | Core Backend | Week 5–10 | APIs, Databases, Auth |
| 3 | Infrastructure | Week 11–16 | Docker, Cloud, CI/CD |
| 4 | Advanced Topics | Week 17–24 | Caching, Queues, System Design |

---

## Phase 1: Foundations (Week 1–4)

### 🟦 Topic: Python Basics

- **Subtopics:** Variables & types, Functions, OOP, File I/O, Error handling, Virtual environments
- **Resources:**
  - 📖 [Official Python Docs](https://docs.python.org/3/)
  - 🎥 [Python Full Course for Beginners – freeCodeCamp](https://www.youtube.com/watch?v=rfscVS0vtbw)
  - 📝 [Real Python – Beginner Tutorials](https://realpython.com/start-here/)
- **Project:** Build a CLI to-do list app with file persistence
- **Status:** [ ] Not started

---

### 🟦 Topic: Linux & Command Line

- **Subtopics:** File system, Permissions, Shell scripting, SSH, Package managers
- **Resources:**
  - 📖 [The Linux Command Line (free book)](https://linuxcommand.org/tlcl.php)
  - 🎥 [Linux for Beginners – NetworkChuck](https://www.youtube.com/watch?v=l9YxTXDiiFY)
- **Project:** Write a bash script to automate a repetitive file management task
- **Status:** [ ] Not started

---

### 🟦 Topic: Git & Version Control

- **Subtopics:** Init, Add, Commit, Branching, Merging, Pull requests, GitHub workflow
- **Resources:**
  - 📖 [Pro Git Book (free)](https://git-scm.com/book/en/v2)
  - 🎥 [Git and GitHub for Beginners – freeCodeCamp](https://www.youtube.com/watch?v=RGOj5yH7evk)
  - 🛠️ [Learn Git Branching (interactive)](https://learngitbranching.js.org/)
- **Project:** Collaborate on a public GitHub repo using branches and PRs
- **Status:** [ ] Not started

---

## Phase 2: Core Backend (Week 5–10)

### 🟨 Topic: REST API Development

- **Subtopics:** HTTP methods, Status codes, FastAPI/Flask, Request/Response cycle, Serialization, Validation
- **Resources:**
  - 📖 [FastAPI Official Docs](https://fastapi.tiangolo.com/)
  - 🎥 [FastAPI Full Course – Amigoscode](https://www.youtube.com/watch?v=7t2alSnE2-I)
  - 📝 [REST API Design Best Practices](https://www.freecodecamp.org/news/rest-api-best-practices-rest-endpoint-design-examples/)
- **Project:** Build a CRUD REST API for a bookstore (title, author, price)
- **Status:** [ ] Not started

---

### 🟨 Topic: Databases & SQL

- **Subtopics:** Relational models, CRUD, Joins, Indexes, Transactions, PostgreSQL setup, ORMs (SQLAlchemy)
- **Resources:**
  - 📖 [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
  - 🎥 [SQL Full Course – freeCodeCamp](https://www.youtube.com/watch?v=HXV3zeQKqGY)
  - 🛠️ [SQLZoo – Interactive SQL Practice](https://sqlzoo.net/)
- **Project:** Add a PostgreSQL database to your bookstore API
- **Status:** [ ] Not started

---

### 🟨 Topic: Authentication & Security

- **Subtopics:** JWT, OAuth 2.0, Password hashing (bcrypt), HTTPS, CORS, Rate limiting
- **Resources:**
  - 📖 [OWASP Top 10](https://owasp.org/www-project-top-ten/)
  - 🎥 [JWT Authentication – Traversy Media](https://www.youtube.com/watch?v=mbsmsi7l3r4)
- **Project:** Add JWT-based login/signup to your bookstore API
- **Status:** [ ] Not started

---

## Phase 3: Infrastructure (Week 11–16)

### 🟧 Topic: Docker & Containers

- **Subtopics:** Images, Containers, Dockerfile, Docker Compose, Volumes, Networking
- **Resources:**
  - 📖 [Docker Official Docs](https://docs.docker.com/)
  - 🎥 [Docker Tutorial for Beginners – TechWorld with Nana](https://www.youtube.com/watch?v=3c-iBn73dDE)
- **Project:** Dockerize your bookstore API with a Compose file for the app + Postgres
- **Status:** [ ] Not started

---

### 🟧 Topic: Cloud Basics (AWS)

- **Subtopics:** EC2, S3, RDS, IAM, VPC, Elastic Beanstalk, Environment variables
- **Resources:**
  - 📖 [AWS Getting Started Guide](https://aws.amazon.com/getting-started/)
  - 🎥 [AWS Full Course – freeCodeCamp](https://www.youtube.com/watch?v=ubCNZFQZqbI)
- **Project:** Deploy your Dockerized API to an EC2 instance
- **Status:** [ ] Not started

---

### 🟧 Topic: CI/CD Pipelines

- **Subtopics:** GitHub Actions, Build/test/deploy stages, Secrets management, Automated testing
- **Resources:**
  - 📖 [GitHub Actions Docs](https://docs.github.com/en/actions)
  - 🎥 [GitHub Actions Full Course – TechWorld with Nana](https://www.youtube.com/watch?v=R8_veQiYBjI)
- **Project:** Set up a GitHub Actions pipeline to test and deploy your API on push
- **Status:** [ ] Not started

---

## Phase 4: Advanced Topics (Week 17–24)

### 🟥 Topic: Caching

- **Subtopics:** Cache strategies, Redis, Cache invalidation, CDN caching
- **Resources:**
  - 📖 [Redis Docs](https://redis.io/docs/)
  - 🎥 [Redis Crash Course – TechWorld with Nana](https://www.youtube.com/watch?v=jgpVdJB2sKQ)
- **Project:** Add Redis caching to frequently-hit API endpoints
- **Status:** [ ] Not started

---

### 🟥 Topic: Message Queues

- **Subtopics:** Pub/Sub pattern, RabbitMQ, Celery, Async task processing
- **Resources:**
  - 📖 [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
  - 🎥 [Celery with Django/Flask – Pretty Printed](https://www.youtube.com/watch?v=ir4HalTEFm4)
- **Project:** Use Celery + Redis to send welcome emails asynchronously on signup
- **Status:** [ ] Not started

---

### 🟥 Topic: System Design Basics

- **Subtopics:** Scalability, Load balancing, CAP theorem, Horizontal vs vertical scaling, Microservices intro
- **Resources:**
  - 📖 [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)
  - 🎥 [System Design for Beginners – freeCodeCamp](https://www.youtube.com/watch?v=m8Icp_Cid5o)
- **Project:** Design (on paper) a scalable URL shortener — document your decisions
- **Status:** [ ] Not started

---

## ✅ Progress Summary

```
Phase 1: Foundations       -  0%  (0/3 topics)
Phase 2: Core Backend      -  0%  (0/3 topics)
Phase 3: Infrastructure    -  0%  (0/3 topics)
Phase 4: Advanced Topics   -  0%  (0/3 topics)

Overall                    -  0%  (0/12 topics)
```
