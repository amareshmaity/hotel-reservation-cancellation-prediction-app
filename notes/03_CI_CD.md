# CI/CD Deployment in MLOps

## 1. Introduction to CI/CD

CI/CD is one of the final stages of an MLOps pipeline. It automates the process of taking changes made to a project, building the application, and deploying the updated version to the cloud.

**CI/CD stands for:**

* **CI — Continuous Integration**
* **CD — Continuous Deployment**

The main goal is to reduce manual deployment work and make software delivery faster, repeatable, and reliable.

### Example

Suppose an ML application is already running on Google Cloud.

Later, we modify:

* `index.html`
* CSS files
* Flask/FastAPI code
* ML model code
* Configuration
* Application features

Instead of manually copying the updated files to the cloud, we can push the changes to GitHub and let the CI/CD pipeline handle the deployment automatically.

```text
Developer
    ↓
GitHub
    ↓
Jenkins
    ↓
Build & Test
    ↓
Docker Image
    ↓
Container Registry
    ↓
Google Cloud Run
    ↓
Updated Application
```

<br/>

## 2. Continuous Integration (CI)

**Continuous Integration** is the practice of frequently integrating code changes into a shared repository and automatically running build, validation, and testing processes.

In our project:

```text
Local Development
       ↓
     git push
       ↓
     GitHub
       ↓
    Jenkins
       ↓
Build / Test / Validate
```

### Benefits of CI

* Detects problems early
* Keeps the main codebase up to date
* Automates builds and tests
* Reduces manual work
* Improves development speed
* Makes integration more reliable

<br/>

# 3. Continuous Deployment (CD)

**Continuous Deployment** extends CI by automatically deploying successfully built and validated software to the production environment.

For our ML application:

```text
Successful Build
      ↓
Docker Image
      ↓
Container Registry
      ↓
Google Cloud Run
      ↓
Production Application
```

Therefore, a developer does not need to manually deploy every change.

<br/>

## 4. Jenkins

**Jenkins** is an automation server commonly used to implement CI/CD pipelines.

It can automate tasks such as:

* Pulling source code from GitHub
* Creating environments
* Installing dependencies
* Running tests
* Building Docker images
* Pushing images to a registry
* Deploying applications

For this project, Jenkins acts as the **orchestrator of the deployment process**.

```text
                 Jenkins
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
     Build        Test       Deploy
```

<br/>

## 5. Docker-in-Docker (DinD)

**DinD** stands for **Docker-in-Docker**.

The idea is that Jenkins runs inside a Docker environment while also needing Docker capabilities to build and manage application containers.

Conceptually:

```text
Host
 │
 └── Jenkins Container
       │
       └── Docker Operations
             │
             └── Application Image
```

### Why is this useful?

The Jenkins environment needs Docker functionality because the CI/CD pipeline will build the application's Docker image.

> **Important:** Docker-in-Docker is an architectural approach, not simply "a container inside another container." In production Jenkins setups, alternatives such as mounting the Docker socket or using dedicated container-build tools may be preferred depending on security requirements.

<br/>

## 6. Overall CI/CD Pipeline

The deployment pipeline can be divided into the following stages:

```text
1. Jenkins Setup
       ↓
2. GitHub Integration
       ↓
3. Dockerize Application
       ↓
4. Prepare Environment & Dependencies
       ↓
5. Build and Push Docker Image
       ↓
6. Deploy to Cloud Run
```

<br/>

## 7. Stage 1 — Jenkins Setup

The first step is to set up Jenkins as the CI/CD server.

Jenkins needs to be capable of:

* Accessing the GitHub repository
* Executing shell commands
* Running build processes
* Working with Docker
* Authenticating with Google Cloud
* Deploying the application

A Dockerized Jenkins setup can be used to keep the Jenkins environment isolated and reproducible.

```text
Docker
  │
  └── Jenkins
       │
       └── CI/CD Pipeline
```

<br/>

## 8. Stage 2 — GitHub Integration

The source code should be maintained in a Git repository, such as GitHub.

The Jenkins pipeline retrieves the project from the repository instead of using the developer's local project directory.

```text
Developer
    ↓
git push
    ↓
GitHub Repository
    ↓
Jenkins
```

### Why GitHub?

GitHub provides:

* Version control
* Centralized source code
* Collaboration
* Commit history
* Branch management
* Integration with CI/CD systems

A common workflow is:

```text
Code Change
    ↓
Commit
    ↓
Push
    ↓
GitHub
    ↓
Jenkins Pipeline Trigger
```

<br/>

## 9. Stage 3 — Dockerize the Application

The application needs to be packaged into a Docker container.

A **Dockerfile** describes how the application image should be built.

A typical Dockerfile defines:

* Base image
* Working directory
* Required dependencies
* Application files
* Environment variables
* Application startup command

The general process is:

```text
Application Source Code
          +
      Dockerfile
          ↓
    docker build
          ↓
     Docker Image
```

### Why Dockerize the application?

Docker provides a consistent runtime environment.

Instead of relying on the configuration of a particular machine, the application and its required runtime environment are packaged together.

This helps reduce:

> "It works on my machine" problems.

<br/>

## 10. Stage 4 — Environment and Dependencies

The application needs its required Python packages and dependencies during the build process.

For example:

```text
Python
   ↓
Virtual Environment
   ↓
Install Dependencies
   ↓
Application
```

Dependencies may be defined in files such as:

```text
requirements.txt
```

or through Python packaging configuration such as:

```text
pyproject.toml
setup.py
```

### Important point

The local virtual environment should generally **not** be pushed to GitHub.

For example:

```text
❌ venv/
❌ .venv/
```

Instead, dependency definitions are committed:

```text
✅ requirements.txt
✅ pyproject.toml
```

The CI/CD environment can then recreate the required environment.

<br/>

## 11. Stage 5 — Build the Docker Image

Once the application and dependencies are ready, Jenkins builds the Docker image using the Dockerfile.

```text
Dockerfile
    +
Application Code
    +
Dependencies
    ↓
Docker Build
    ↓
Docker Image
```

The image becomes the deployable artifact of the application.

For example:

```text
hotel-reservation-app:v1
```

The image can then be pushed to a container registry.

<br/>

## 12. Container Registry

A **container registry** is a repository for storing and retrieving Docker/container images.

Historically, Google Cloud's service was called:

**Google Container Registry (GCR)**

The conceptual workflow is:

```text
Jenkins
   ↓
Docker Image
   ↓
Container Registry
```

The registry acts as a central location from which deployment platforms can retrieve container images.

### Modern Google Cloud practice

For new Google Cloud projects, **Artifact Registry** is generally preferred over GCR.

So a modern architecture would normally look like:

```text
Jenkins
   ↓
Docker Build
   ↓
Artifact Registry
   ↓
Cloud Run
```

<br/>

## 13. Stage 6 — Deploy to Google Cloud Run

After the Docker image has been stored in the registry, it can be deployed to **Google Cloud Run**.

```text
Artifact Registry
       ↓
   Docker Image
       ↓
   Cloud Run
       ↓
Running Application
```

Cloud Run provides a managed environment for running containerized applications without requiring you to manage the underlying server infrastructure directly.

<br/>

## 14. Complete Deployment Flow

Putting everything together:

```text
                    Developer
                        │
                        │ git push
                        ▼
                 ┌─────────────┐
                 │   GitHub    │
                 └──────┬──────┘
                        │
                        │ Source Code
                        ▼
                 ┌─────────────┐
                 │   Jenkins   │
                 └──────┬──────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
           Build                Test
              │                   │
              └─────────┬─────────┘
                        ▼
                   Docker Build
                        │
                        ▼
                 ┌─────────────┐
                 │Docker Image │
                 └──────┬──────┘
                        │
                        ▼
                Artifact Registry
                        │
                        ▼
                 Google Cloud Run
                        │
                        ▼
                Production App
```

<br/>

## 15. Why CI/CD Is Important in MLOps

Machine learning applications are not just notebooks or models. They eventually need to be delivered as reliable software.

CI/CD helps automate this transition.

### Without CI/CD

```text
Developer
   ↓
Manual Copy
   ↓
Manual Build
   ↓
Manual Deployment
   ↓
Production
```

This is:

* Slow
* Error-prone
* Difficult to reproduce
* Difficult to maintain

### With CI/CD

```text
Developer
   ↓
Git Push
   ↓
Automated Pipeline
   ↓
Automated Build
   ↓
Automated Deployment
   ↓
Production
```

This makes deployment:

* Faster
* Repeatable
* Consistent
* Easier to maintain
* Less dependent on manual intervention

<br/>

## 16. Key Components to Remember

| Component                   | Purpose                                       |
| --------------------------- | --------------------------------------------- |
| **GitHub**                  | Source-code repository                        |
| **Jenkins**                 | CI/CD automation                              |
| **Dockerfile**              | Instructions for building the container image |
| **Docker**                  | Containerization                              |
| **Container Image**         | Deployable application artifact               |
| **Artifact Registry / GCR** | Stores container images                       |
| **Cloud Run**               | Runs the containerized application            |
| **Virtual Environment**     | Isolates Python dependencies                  |

<br/>

## Conclusion 

CI/CD turns deployment from a **manual process** into an **automated software delivery pipeline**.

For an MLOps project, this is particularly important because the same pipeline can eventually be extended beyond application deployment to include:

```text
Code
 ↓
Tests
 ↓
Data Validation
 ↓
Model Training
 ↓
Model Evaluation
 ↓
Model Packaging
 ↓
Docker Image
 ↓
Registry
 ↓
Cloud Deployment
 ↓
Monitoring
```

That is the broader role of CI/CD within a production-grade **MLOps lifecycle**.
