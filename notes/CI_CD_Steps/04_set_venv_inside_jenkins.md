# Create a Virtual Environment in the Jenkins Pipeline

## Objective

The fourth stage of the CI/CD pipeline is to create an isolated **Python virtual environment** inside the Jenkins workspace and install the project's dependencies.

The important idea is that the virtual environment is **created dynamically by Jenkins**. It does not need to be stored in GitHub.

<br/>

## Steps

### 1. Define the Virtual Environment Directory

Open the project's `Jenkinsfile`.

At the top of the pipeline, immediately under:

```groovy
agent any
```

define an environment variable:

```groovy
environment {
    VENV_DIR = 'venv'
}
```

The beginning of the Jenkinsfile will therefore look like:

```groovy
pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        ...
    }
}
```

#### Why define `VENV_DIR`?

Instead of writing the virtual environment directory name repeatedly, we store it in a variable:

```text
VENV_DIR
   ↓
venv
```

Later, Jenkins can refer to it as:

```groovy
${VENV_DIR}
```

This makes the pipeline easier to modify.

<br/>

### 2. Add a New Pipeline Stage

The existing pipeline already contains the GitHub checkout stage.

Now add another stage for the Python environment.

The pipeline becomes:

```text
Stage 1
Clone GitHub Repository
        ↓
Stage 2
Set Up Virtual Environment
        ↓
Install Dependencies
```

<br/>

### Name the Stage

Create a new stage with a descriptive name:

```groovy
stage('Setting Up Virtual Environment and Installing Dependencies') {
    ...
}
```

A shorter name can also be used, but the important point is that the stage clearly describes its responsibility.

<br/>

### 4. Add the Steps Section

Inside the stage:

```groovy
stage('Setting Up Virtual Environment and Installing Dependencies') {

    steps {

        echo 'Setting up our virtual environment and installing dependencies'
    }
}
```

<br/>

### 5. Execute Multiple Shell Commands

The stage needs to execute several Linux commands.

For that, use the Jenkins `sh` step with multiple lines:

```groovy
sh '''
    ...
'''
```

Triple quotes allow multiple shell commands to be written inside the same block.

<br/>

### 6. Create the Virtual Environment

Use:

```bash
python -m venv ${VENV_DIR}
```


#### Activate the Virtual Environment

The Jenkins environment is Linux-based, so the activation syntax is different from Windows.

Use:

```bash
. ${VENV_DIR}/bin/activate
```


### 7. Upgrade pip

After activating the environment:

```bash
pip install --upgrade pip
```

This ensures that the virtual environment has an up-to-date pip version before installing the project dependencies.


<br/>

### 8. Install the Project and Dependencies

The project is installed using:

```bash
pip install -e .
```

The `.` means:

> Install the project located in the current directory.

<br/>

## Complete Jenkins Stage

The stage described in the transcript can be written as:

```groovy
stage('Setting Up Virtual Environment and Installing Dependencies') {
    steps {
        echo 'Setting up our virtual environment and installing dependencies'

        sh '''
            python -m venv ${VENV_DIR}
            . ${VENV_DIR}/bin/activate
            pip install --upgrade pip
            pip install -e .
        '''
    }
}
```

And the beginning of the Jenkinsfile becomes:

```groovy
pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {

        stage('Cloning GitHub Repo to Jenkins') {
            steps {
                echo 'Cloning GitHub repo to Jenkins'

                // Git checkout configuration
                checkout(...)
            }
        }

        stage('Setting Up Virtual Environment and Installing Dependencies') {
            steps {
                echo 'Setting up our virtual environment and installing dependencies'

                sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                '''
            }
        }
    }
}
```

<br/>

### Why the Virtual Environment Is Created in Jenkins

The virtual environment from the developer's computer should not be copied into GitHub.

Instead:

```text
Developer Machine
       │
       ├── venv/        ❌ Not committed
       │
       └── requirements / project configuration
                    ↓
                  GitHub
                    ↓
                 Jenkins
                    ↓
              New venv created
```

This ensures Jenkins creates its own clean Python environment.

<br/>

## Verify the Jenkins Build

After modifying the Jenkinsfile:

### Step 1 — Save the Jenkinsfile

Save the changes.

### Step 2 — Push to GitHub

```bash
git add Jenkinsfile
```

Create a commit:

```bash
git commit -m "Add virtual environment setup to Jenkins pipeline"
```

Push:

```bash
git push origin main
```

<br/>

### Step 3 — Run the Jenkins Job

Go to:

```text
Jenkins Dashboard
      ↓
MLOps-1
      ↓
Build Now
```

Open:

```text
Console Output
```

You should see something similar to:

```text
Cloning GitHub repo to Jenkins
```

followed by:

```text
Setting up our virtual environment and installing dependencies
```

Then Jenkins starts creating the environment and installing packages.

<br/>

### Step 4 — Verify the Virtual Environment

After the build completes, check the Jenkins workspace.

You should see:

```text
Workspace
│
├── Jenkinsfile
├── Dockerfile
├── application.py
├── setup.py
├── pipeline/
├── requirements.txt
└── venv/
```

The presence of:

```text
venv/
```

indicates that the virtual environment was created in the workspace.

<br/>

## Overall Pipeline Progress

The project has now reached:

```text
┌────────────────────────────────────┐
│        CI/CD Pipeline              │
├────────────────────────────────────┤
│                                    │
│  1. Jenkins Setup             ✓    │
│           ↓                        │
│  2. GitHub Integration        ✓    │
│           ↓                        │
│  3. Project Dockerfile        ✓    │
│           ↓                        │
│  4. Virtual Environment       ✓    │
│           ↓                        │
│  5. Docker Image Build             │
│           ↓                        │
│  6. Push Image to Registry         │
│           ↓                        │
│  7. Deploy to Cloud Run            │
│                                    │
└────────────────────────────────────┘
```


