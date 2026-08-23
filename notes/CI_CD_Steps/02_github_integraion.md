# GitHub Integration with Jenkins

## Objective

The purpose of this stage is to connect the **GitHub repository** with **Jenkins** so that Jenkins can securely access the project's source code.

The basic workflow is:

```text
GitHub Repository
       ↓
GitHub Token
       ↓
Jenkins Credentials
       ↓
Jenkins Pipeline
       ↓
Checkout Source Code
       ↓
Jenkins Workspace
```

Once this works, Jenkins can retrieve the complete project from GitHub and use it in later CI/CD stages.

<br/>

## Step 1 — Create a GitHub Personal Access Token

Jenkins needs authentication credentials to access the GitHub repository.

The transcript uses a **GitHub Personal Access Token (PAT)**.

### 1.1 Open GitHub Settings

Go to your GitHub account.

Navigate to:

```text
GitHub
  ↓
Profile
  ↓
Settings
  ↓
Developer Settings
```

<br/>


### 1.2 Open Personal Access Tokens

Inside **Developer Settings**, find:

```text
Personal access tokens
```

Then select:

```text
Tokens (classic)
```

Choose:

```text
Generate new token
```

and generate a **classic token**.

<br/>


### 1.3 Configure the Token

Give the token a meaningful name.

For example:

```text
Jenkins GitHub Token
```

The token should have the permissions required for Jenkins to access the repository.

The transcript specifically selects:

```text
repo
```

and the related repository administration permission.

```text
admin:repo_hook
```

Then generate the token.

<br/>


### 1.4 Save the Token

After generating the token, GitHub displays the token.

**Copy it immediately and store it securely.**

You generally cannot retrieve the same token value again after leaving the page.

#### Important

Do **not** put the token directly inside:

* `Jenkinsfile`
* Python code
* Git repository
* Dockerfile
* GitHub source code

The token should be stored in Jenkins Credentials.


<br/>

## Step 2 — Add GitHub Token to Jenkins Credentials

### 2.1 
Now Jenkins needs to know about the GitHub credentials.

Open:

```text
Jenkins Dashboard
      ↓
Manage Jenkins
      ↓
Credentials
```

Go to the appropriate global credentials store and choose:

```text
Add Credentials
```

<br/>

### 2.2 Configure the Jenkins Credential

Select:

```text
Kind: Username with password
```

Although the credential type is called **Username with password**, the "password" field will contain the GitHub Personal Access Token.

#### Fill the fields

| Field       | Value                        |
| ----------- | ---------------------------- |
| Username    | Your GitHub username         |
| Password    | GitHub Personal Access Token |
| ID          | `github-token`               |
| Description | `github-token`               |



Then click: **Create**

<br/>

### Why Store the Token in Jenkins?

The token allows Jenkins to authenticate with GitHub.

Instead of writing credentials directly into the pipeline:

```text
❌ Jenkinsfile
   ↓
GitHub Token
```

we store them securely in Jenkins:

```text
GitHub Token
     ↓
Jenkins Credentials
     ↓
Jenkins Pipeline
     ↓
GitHub Repository
```

This keeps sensitive credentials outside the source code.

<br/>

## Step 3 — Create a Jenkins Pipeline Job

### 3.1 Return to the Jenkins Dashboard.

Select:

```text
New Item
```

Give the job a name.

For example:

```text
MLOps-1
```

Select:

```text
Pipeline
```

Then click:

**OK**

<br/>

### 3.2 Configure Pipeline from GitHub

Scroll down to the **Pipeline** section.

For:

```text
Definition
```

select:

```text
Pipeline script from SCM
```

#### What does SCM mean?

**SCM = Source Code Management**

It tells Jenkins where the pipeline source code is stored.

Select:

```text
SCM → Git
```

<br/>

### 3.3 Add the GitHub Repository URL

Go to your GitHub repository.

Click:

```text
Code
```

Copy the repository URL.

For example:

```text
https://github.com/<username>/<repository>.git
```

Paste it into Jenkins:

```text
Repository URL
```

<br/>

### 3.4 Select Jenkins GitHub Credentials

In the Jenkins Git configuration, find:

```text
Credentials
```

Select the credential that you created earlier:

```text
github-token
```

Now Jenkins has:

```text
Repository URL
        +
GitHub Credentials
        ↓
Access to GitHub Repository
```

<br/>

### 3.5 Select the Correct Branch

The transcript initially shows a `master` branch but then checks the GitHub repository and finds that the actual branch is:

```text
main
```

Therefore, configure Jenkins to use:

```text
Branch: main
```

#### Important

The branch name in Jenkins must match the actual branch in GitHub.

For example:

```text
GitHub
└── main
```

Therefore:

```text
Jenkins
└── */main
```

<br/>

### 3.6 Configure the Jenkinsfile Path

In the pipeline configuration, specify:

```text
Script Path: Jenkinsfile
```

This tells Jenkins where the pipeline definition is located inside the repository.

The expected project structure is:

```text
MLOps Project
│
├── Jenkinsfile
├── Dockerfile
├── application.py
├── requirements.txt
├── setup.py
├── pipeline/
└── ...
```

The `Jenkinsfile` is located at the root of the repository.

<br/>

## Step 4 — Generate the Git Checkout Script

Jenkins provides a useful feature called:

**Pipeline Syntax**

Open:

```text
Pipeline Syntax
```

In the **Sample Step** section, select:

```text
checkout: checkout from version control
-> General SCM
```

Configure:

* Repository URL
* GitHub credentials
* Branch

For example:

```text
Repository URL:
https://github.com/<username>/<repository>.git

Credentials:
github-token

Branch:
main
```

Then click:

```text
Generate Pipeline Script
```

Jenkins generates a checkout script.

This script can be used inside the Jenkins pipeline to retrieve the GitHub repository.

<br/>

## Step 5 — Create the Jenkinsfile

Now create a file called inside project root:

```text
Jenkinsfile
```

### 5.1 Create the First Jenkins Pipeline

The first pipeline stage will only perform one task:

> Clone the GitHub repository into the Jenkins workspace.

The basic structure is:

```groovy
pipeline {
    agent any

    stages {

        stage('Cloning GitHub Repo to Jenkins') {

            steps {

                echo 'Cloning GitHub repo to Jenkins'

                // Git checkout code generated by Jenkins
                checkout(...)
            }
        }
    }
}
```

The exact `checkout(...)` block should be the one generated by your Jenkins **Pipeline Syntax** page.

<br/>

### Understand the Jenkinsfile Structure

The important Jenkins Pipeline structure is:

```text
pipeline
   │
   ├── agent
   │
   └── stages
          │
          └── stage
                 │
                 └── steps
```

#### `pipeline`

Defines the Jenkins declarative pipeline.

#### `agent any`

Allows Jenkins to execute the pipeline on any available Jenkins agent.

#### `stages`

Contains the different stages of the CI/CD process.

#### `stage`

Represents one logical phase.

For example:

```text
Stage 1 → Clone Repository
Stage 2 → Install Dependencies
Stage 3 → Test
Stage 4 → Build Docker Image
Stage 5 → Push Image
Stage 6 → Deploy
```

### `steps`

Contains the commands Jenkins executes during that stage.

<br/>

### First Stage: What it will do?
It will clone GitHub Repository to Jenkins workspace

For the current stage, we only need:

```text
Stage
└── Clone GitHub Repository
```

The `echo` command displays a message in the Jenkins console:

```groovy
echo 'Cloning GitHub repo to Jenkins'
```

Then:

```groovy
checkout(...)
```

retrieves the repository.

The resulting flow is:

```text
Jenkins Pipeline Starts
        ↓
Print Message
        ↓
Authenticate with GitHub
        ↓
Checkout main branch
        ↓
Copy repository to Jenkins Workspace
```

<br/>

## Step 6 — Execute the pipeline (Jenkins Build)

### 6.1 Push Jenkinsfile to GitHub

Before build, the Jenkinsfile itself must be committed to the GitHub repository.

Since you have created:

```text
Dockerfile
Jenkinsfile
```

you need to commit these changes.

### Add the files

```bash
git add .
```

### Create a commit

```bash
git commit -m "Add Jenkins CI/CD configuration"
```

### Push to main

```bash
git push origin main
```

Now GitHub contains the Jenkinsfile.

<br/>

### 6.2 Run the Jenkins Pipeline

Return to:

```text
Jenkins Dashboard
    ↓
MLOps-1
```

Click:

```text
Build Now
```

Jenkins will start executing the pipeline.

<br/>

### 6.3 Check Console Output

Open the build and select:

```text
Console Output
```

You should see the pipeline execution.

The custom message:

```text
Cloning GitHub repo to Jenkins
```

should appear.

You should also see Git operations indicating that Jenkins has checked out the repository.

Finally, the build should finish successfully.

```text
Finished: SUCCESS
```

<br/>

### 6.4 Verify the Jenkins Workspace

Jenkins stores the checked-out project in its **workspace**.

Conceptually:

```text
Jenkins
   ↓
Workspace
   ↓
MLOps Project
```

The workspace should contain the files from GitHub:

```text
Workspace
│
├── Jenkinsfile
├── Dockerfile
├── application.py
├── setup.py
├── requirements.txt
├── pipeline/
└── ...
```

This proves that Jenkins successfully retrieved the source code.

<br/>

## What Has Been Achieved?

At this point, the **first CI/CD** stage is complete.

The connection is:

```text
GitHub
   │
   │ Authentication
   ▼
GitHub Token
   │
   ▼
Jenkins Credentials
   │
   ▼
Jenkins Pipeline
   │
   ▼
Git Checkout
   │
   ▼
Jenkins Workspace
```

Jenkins can now obtain the source code from GitHub.

<br/>

## Concepts

### Personal Access Token (PAT)

A GitHub authentication token used instead of a traditional password for API/Git operations.

### Jenkins Credentials

Jenkins' secure mechanism for storing authentication information used by jobs and pipelines.

### SCM

**Source Code Management** — the system Jenkins uses to retrieve source code, such as Git.

### Jenkinsfile

A text file containing the Jenkins Pipeline definition.

### Pipeline

The automated sequence of CI/CD operations.

### Stage

A logical section of the pipeline.

Example:

```text
Clone → Build → Test → Package → Deploy
```

### Workspace

The directory in which Jenkins checks out and works with the project source code.

<br/>

## Current MLOps Pipeline Progress

After completing this stage, your project architecture is:

```text
┌────────────────────┐
│     Developer      │
│      VS Code       │
└─────────┬──────────┘
          │
          │ git push
          ▼
┌────────────────────┐
│      GitHub        │
│   main branch      │
└─────────┬──────────┘
          │
          │ Git + PAT
          ▼
┌────────────────────┐
│      Jenkins       │
│                    │
│  Jenkins Pipeline  │
└─────────┬──────────┘
          │
          │ checkout
          ▼
┌────────────────────┐
│ Jenkins Workspace  │
│                    │
│ Jenkinsfile        │
│ Dockerfile         │
│ application.py     │
│ setup.py           │
│ requirements.txt   │
│ pipeline/          │
└────────────────────┘
```


This completes the **GitHub Integration + Repository Checkout** stage of the CI/CD pipeline.
