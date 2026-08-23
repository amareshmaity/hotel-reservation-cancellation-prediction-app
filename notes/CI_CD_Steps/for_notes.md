---
# 2. Github Integration



# Step 8 — Create the Project Dockerfile

Now Dockerize the actual ML application.

Create a `Dockerfile` in the **project root directory**.

Example:

```dockerfile
FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python", "application.py"]
```

---

# Step 9 — Understand the Project Dockerfile

## 9.1 Base Image

```dockerfile
FROM python:slim
```

Uses a lightweight Python image as the base.

---

## 9.2 Python Environment Variables

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

### `PYTHONDONTWRITEBYTECODE=1`

Prevents Python from creating `.pyc` bytecode files.

### `PYTHONUNBUFFERED=1`

Makes Python output appear immediately in container logs.

This is useful for monitoring applications running in containers.

---

# Step 10 — Set the Working Directory

```dockerfile
WORKDIR /app
```

All subsequent application operations occur inside:

```text
/app
```

Inside the container, the project will therefore look conceptually like:

```text
/app
├── application.py
├── pipeline/
├── requirements/
├── ...
└── Dockerfile
```

---

# Step 11 — Install System Dependencies

The Dockerfile installs:

```dockerfile
libgomp1
```

This is required by certain libraries, including **LightGBM**, because of its OpenMP runtime dependency.

The command also removes unnecessary APT cache files:

```dockerfile
rm -rf /var/lib/apt/lists/*
```

This helps keep the image smaller.

---

# Step 12 — Copy the Project

```dockerfile
COPY . .
```

This copies the project files from the Docker build context into:

```text
/app
```

inside the image.

Conceptually:

```text
Local Project
     ↓
Docker Build
     ↓
/app
```

---

# Step 13 — Install the Python Project

```dockerfile
RUN pip install --no-cache-dir -e .
```

This installs the project in **editable mode**.

The project should have appropriate Python packaging metadata, such as `pyproject.toml` or compatible `setup.py` configuration.

---

# Step 14 — Train the Model During Image Build

The Dockerfile contains:

```dockerfile
RUN python pipeline/training_pipeline.py
```

This executes the training pipeline while the Docker image is being built.

Conceptually:

```text
Docker Build
     ↓
Install Dependencies
     ↓
Run Training Pipeline
     ↓
Generate Model Artifact
     ↓
Complete Docker Image
```

### Important architectural consideration

For a production MLOps system, **training during the Docker image build is usually not the preferred architecture**.

A more scalable design separates:

```text
Model Training
      ↓
Model Artifact / Model Registry
      ↓
Application Container
```

The application container should generally serve an already-trained model rather than retraining every time the application image is built.

For learning purposes, however, the approach in the provided setup demonstrates how a training script can be executed during the image build.

---

# Step 15 — Expose Application Port

```dockerfile
EXPOSE 5000
```

This documents that the Flask application listens on port `5000`.

The application should therefore be configured to listen on the appropriate interface and port.

---

# Step 16 — Start the Application

```dockerfile
CMD ["python", "application.py"]
```

This becomes the default command when the container starts.

Therefore:

```text
Container Starts
      ↓
python application.py
      ↓
Flask Application
      ↓
Port 5000
```

---

# Step 17 — Build the Project Docker Image

From the project root:

```bash
docker build -t your_project_image .
```

Docker will:

1. Read the Dockerfile.
2. Create the Python environment.
3. Install system dependencies.
4. Copy the project.
5. Install the Python package.
6. Run the training pipeline.
7. Create the final Docker image.

---

# Step 18 — Run the Project Container

Start the application:

```bash
docker run -d -p 5000:5000 your_project_image
```

The port mapping means:

```text
Host Port 5000
      ↓
Container Port 5000
```

You can then access the application through the appropriate local URL.

---

# Step 19 — Install Google Cloud CLI in Jenkins

Jenkins eventually needs to communicate with Google Cloud.

For that, the **Google Cloud CLI (`gcloud`)** is installed inside the Jenkins environment.

## 19.1 Enter Jenkins as Root

```bash
docker exec -u root -it jenkins-dind bash
```

---

## 19.2 Install Required Packages

```bash
apt-get update
```

Then:

```bash
apt-get install -y curl apt-transport-https ca-certificates gnupg
```

---

## 19.3 Add Google Cloud Package Repository

The provided setup uses:

```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
```

Then:

```bash
echo "deb https://packages.cloud.google.com/apt cloud-sdk main" \
| tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
```

Update package information:

```bash
apt-get update
```

Install Google Cloud CLI:

```bash
apt-get install -y google-cloud-sdk
```

---

## 19.4 Verify Installation

```bash
gcloud --version
```

If the installation is successful, the Google Cloud CLI version information will be displayed.

Then exit:

```bash
exit
```

### Modern note

For current Debian/Ubuntu-based setups, Google's package repository/key installation procedure may differ from older tutorials. Prefer Google's current installation instructions when implementing this from scratch.

---

# Step 20 — Give Jenkins Docker Permissions

The Jenkins user needs permission to interact with Docker.

Enter the Jenkins container as root:

```bash
docker exec -u root -it jenkins-dind bash
```

Then configure the Docker group:

```bash
groupadd docker
```

Add Jenkins to the Docker group:

```bash
usermod -aG docker jenkins
```

The provided setup also adds Jenkins to the root group:

```bash
usermod -aG root jenkins
```

Then exit:

```bash
exit
```

Restart Jenkins:

```bash
docker restart jenkins-dind
```

---

# 21. Why Docker Permissions Are Required

The Jenkins pipeline will eventually execute Docker commands such as:

```bash
docker build
docker images
docker tag
docker push
```

Therefore Jenkins needs access to the Docker daemon.

The basic relationship is:

```text
Jenkins
   ↓
Docker CLI
   ↓
Docker Daemon
   ↓
Build / Run / Push Images
```

Without appropriate Docker access, Jenkins will receive permission errors when trying to execute Docker commands.

---

# 22. Complete Setup Flow

At this point, the development environment is conceptually:

```text
                    Developer
                        │
                        ▼
                   GitHub Repo
                        │
                        ▼
              ┌─────────────────┐
              │     Jenkins     │
              │                 │
              │ Python          │
              │ pip             │
              │ Docker          │
              │ gcloud          │
              └────────┬────────┘
                       │
                       ▼
                 Docker Build
                       │
                       ▼
                Project Image
                       │
                       ▼
              Container Registry
                       │
                       ▼
                Google Cloud Run
```

---

# 23. Important Commands — Quick Reference

### Docker

```bash
docker --version
docker info
docker images
docker ps
docker logs jenkins-dind
docker restart jenkins-dind
```

### Jenkins container

```bash
docker exec -u root -it jenkins-dind bash
```

### Build Jenkins image

```bash
cd custom_jenkins
docker build -t jenkins-dind .
```

### Run Jenkins

```bash
docker run -d --name jenkins-dind \
  --privileged \
  -p 8080:8080 \
  -p 50000:50000 \
  -v //var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind
```

### Build project image

```bash
docker build -t your_project_image .
```

### Run project

```bash
docker run -d -p 5000:5000 your_project_image
```

### Google Cloud CLI

```bash
gcloud --version
```