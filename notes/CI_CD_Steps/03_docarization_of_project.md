# Project Dockerfile Setup

### Purpose of This Step

At this stage, the goal is to **Dockerize the complete ML project**.

<br/>

## Create the Dockerfile

The **project Dockerfile** must be created in the **root directory of the ML project**.

For example:

```text
hotel-reservation-prediction-app/
│
├── Dockerfile          ← Create here
├── setup.py
├── application.py
├── pipeline/
├── requirements.txt
├── ...
│
└── custom_jenkins/
    └── Dockerfile      ← Jenkins Dockerfile
```

There are two different Dockerfiles in the setup:

* `custom_jenkins/Dockerfile`  -  Creates the custom Jenkins container            
* `Dockerfile` in project root - Packages the ML application into a Docker image 

So, these two Dockerfiles serve different purposes.
The important point is that the two Dockerfiles should not be confused.

<br/>

## Steps

Inside `Dockerfile` add below commands.

### Step 1 — Select a Python Base Image

The first instruction is:

```dockerfile
FROM python:slim
```

This provides Python as the base environment for the application.

#### Why `slim`?

The `slim` image is a lightweight Python image.

Instead of starting with a large operating-system image containing many unnecessary packages, the project starts with a smaller Python environment.
It will will start by installing only necessary packages.

<br/>

### Step 2 — Configure Python Environment Variables

Next, configure Python behavior inside the container:

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

There are two environment variables here.

#### `PYTHONDONTWRITEBYTECODE=1`

Prevents Python from writing `.pyc` bytecode files.

```text
Python
  ↓
No unnecessary .pyc files
```

### `PYTHONUNBUFFERED=1`

Prevents Python's standard output from being buffered.

This is useful for seeing application logs immediately when the container is running.

```text
Application
    ↓
Python logs
    ↓
Container logs immediately
```

<br/>

### Step 3 — Set the Working Directory

Use:

```dockerfile
WORKDIR /app
```

This creates/sets `/app` as the working directory inside the container.

From this point onward, application-related operations are performed relative to:

```text
/app
```

Conceptually:

```text
Container
│
└── /app
     │
     ├── application.py
     ├── setup.py
     ├── pipeline/
     └── ...
```

<br/>

### Step 4 — Install System Dependencies

The project uses **LightGBM**, which requires an additional system dependency.

The Dockerfile installs `libgomp1`:

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

#### What happens here?

First:

```dockerfile
apt-get update
```

updates the package information.

Then:

```dockerfile
apt-get install
```

installs the required package.

The dependency being installed is:

```text
libgomp1
```

which is needed by the project's LightGBM setup.



**Then,** Clean the Package Cache

The Dockerfile then performs:

```dockerfile
apt-get clean
```

and:

```dockerfile
rm -rf /var/lib/apt/lists/*
```

The purpose is to remove unnecessary package-management files after installation and keep the resulting image smaller.

<br/>

### Step 5 — Copy the Project into the Image

Next:

```dockerfile
COPY . .
```

This copies the project files from the Docker build context into the container's current working directory.

Since:

```dockerfile
WORKDIR /app
```

was already defined, the files are copied into:

```text
/app
```

Conceptually:

```text
Local Project
     │
     │ COPY . .
     ▼
Docker Image
     │
     └── /app
```

The project might therefore look like:

```text
/app
│
├── application.py
├── setup.py
├── pipeline/
├── requirements.txt
├── ...
└── Dockerfile
```

<br/>

### Step 6 — Install the Python Project

The next instruction is:

```dockerfile
RUN pip install --no-cache-dir -e .
```

The project is installed using its `setup.py` configuration.


#### Why `--no-cache-dir`?

The Dockerfile uses:

```bash
--no-cache-dir
```

to prevent pip from retaining its package download cache inside the image.

This helps avoid unnecessary files and keeps the image smaller.

<br/>

### Step 7 — Train the Machine Learning Model

After installing the project, the training pipeline is executed:

```dockerfile
RUN python pipeline/training_pipeline.py
```

This runs the project's training pipeline during the Docker image build.

The intended flow is:

```text
Docker Build
     ↓
Install Project
     ↓
Run training_pipeline.py
     ↓
Data Ingestion
     ↓
Data Processing
     ↓
Model Training
     ↓
Model Artifact
     ↓
Docker Image
```

According to the project structure, the training pipeline handles the ML workflow from **data ingestion through model training**.

<br/>

### Step 8 — Expose Application Port

The Flask application runs on port `5000`.

Therefore:

```dockerfile
EXPOSE 5000
```

is added to the Dockerfile.

This indicates that the application uses:

```text
Port: 5000
```

Conceptually:

```text
Container
    │
    └── Flask Application
             │
             └── Port 5000
```

<br/>

### Step 9 — Define the Container Startup Command

Finally:

```dockerfile
CMD ["python", "application.py"]
```

defines the command that runs when the container starts.

It is equivalent to:

```bash
python application.py
```

So the execution flow becomes:

```text
Container Starts
       ↓
python application.py
       ↓
Flask Application Starts
       ↓
Port 5000
```

<br/>

## Complete Dockerfile

Putting all the steps together:

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

# 13. Dockerfile Execution Order

It is useful to understand the Dockerfile as a sequence:

```text
1. Python Slim Image
          ↓
2. Configure Python
          ↓
3. Set /app
          ↓
4. Install LightGBM dependency
          ↓
5. Copy project
          ↓
6. Install Python project
          ↓
7. Train model
          ↓
8. Expose port 5000
          ↓
9. Start Flask application
```

---

# 14. What Each Docker Instruction Does

| Instruction | Purpose                                    |
| ----------- | ------------------------------------------ |
| `FROM`      | Selects the base image                     |
| `ENV`       | Sets environment variables                 |
| `WORKDIR`   | Sets the working directory                 |
| `RUN`       | Executes commands while building the image |
| `COPY`      | Copies project files into the image        |
| `EXPOSE`    | Documents the application's port           |
| `CMD`       | Defines the default startup command        |

---

# 15. Project Dockerization Flow

The complete idea behind this Dockerfile is:

```text
                    Project
                       │
                       ▼
                  Dockerfile
                       │
                       ▼
                docker build
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
     Install Python            Install System
     Dependencies              Dependencies
          │                         │
          └────────────┬────────────┘
                       ▼
                Run Training
                       │
                       ▼
                 Docker Image
                       │
                       ▼
                Start Container
                       │
                       ▼
              Flask Application
                       │
                       ▼
                  Port 5000
```



The next stage is to prepare the **Python virtual environment and dependencies inside the Jenkins pipeline**.
