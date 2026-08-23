# Complete CI/CD with Jenkins, Docker, Github, and Google Cloud 

## Objective

The goal of this setup is to prepare a **Jenkins-based CI/CD environment** for an MLOps project.

The overall flow is:

```text
Developer
    ↓
GitHub
    ↓
Jenkins
    ↓
Docker Build
    ↓
Container Image
    ↓
Google Cloud Registry
    ↓
Google Cloud Run
    ↓
Production Application
```

Jenkins will act as the automation server, while Docker will be used to containerize the application.

<br/>

## Steps
1. Setup Jenkins Container
2. Github Integration
3. Dockarization of Project (Dockerfile)
4. Create venv in Jenkins
5. Build Docker Image of the Project
6. Push to GCR (Google Cloud Registry) - Act similar as dockerhub
7. Live the application with GCR (Google Cloud Run) from GCR

<br/>

## Architecture to Remember

```text
┌──────────────────────────────────────────────┐
│              DEVELOPMENT                     │
│                                              │
│  VS Code → Git → GitHub                      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 JENKINS                      │
│                                              │
│  Source Code                                 │
│      ↓                                       │
│  Python Environment                          │
│      ↓                                       │
│  Build / Test                                │
│      ↓                                       │
│  Docker Build                                │
│      ↓                                       │
│  gcloud                                      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Docker Image    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Artifact        │
              │ Registry        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Google Cloud    │
              │ Run             │
              └────────┬────────┘
                       │
                       ▼
                Production App
```

<br/>

## The key idea

**GitHub is the source of truth → Jenkins is the automation engine → Docker is the packaging mechanism → Registry stores the image → Cloud Run runs the application.**