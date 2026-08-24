# Build and Push the Docker Image to Google Container Registry

## Objective

The purpose of this stage is to take the **Dockerfile created in Step 3**, build a Docker image from it, and push that image to **Google Container Registry (GCR)**.

<br/>

## Steps

### Step 1. Install Google Cloud CLI in Jenkins

Jenkins needs to execute Google Cloud commands such as:

```bash
gcloud auth
gcloud config
gcloud auth configure-docker
```

Therefore, the **Google Cloud CLI** must be available inside the Jenkins container.

<br/>

### 1.1 Enter the Jenkins Container

Open the terminal and access the Jenkins container as root:

```bash
docker exec -u root -it jenkins-dind bash
```

This opens a shell inside the Jenkins container.

<br/>

### 1.2 Update the Package Repository

Inside the Jenkins container:

```bash
apt-get update
```

This refreshes the available package information.

<br/>

### 1.3 Install Required Packages

Install the packages required for the Google Cloud CLI installation:

```bash
apt-get install -y curl apt-transport-https ca-certificates gnupg
```

These provide the tools required to securely download and install the Google Cloud CLI.

<br/>

### 1.4 Install Google Cloud CLI

The Google Cloud CLI installation commands can be obtained from Google's official documentation or use below material.

```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-cli.list

apt-get update && apt-get install -y google-cloud-cli

```
After installation, verify it using:

```bash
gcloud --version
```

You should see output containing the installed Google Cloud SDK version.

For example:

```text
Google Cloud SDK 505.x.x
```

The exact version may be different depending on when the CLI is installed.


<br/>

## Step 2. Give Jenkins Access to Docker (Docker inside Jenkins)

Jenkins will later execute Docker commands such as:

```bash
docker build
docker push
```

Therefore, the Jenkins user needs Docker access.

Inside the Jenkins container:

```bash
groupadd docker
```

If the Docker group already exists, you may see a message indicating that it already exists. That is not a problem.

Then add Jenkins to the Docker group:

```bash
usermod -aG docker jenkins
```

The transcript also adds Jenkins to the root group:

```bash
usermod -aG root jenkins
```

Then exit the Jenkins container:

```bash
exit
```

<br/>

## Step 3. Restart Jenkins

Because changes were made to the Jenkins container, restart it:

```bash
docker restart jenkins-dind
```

Wait for Jenkins to become available again.

Then open:

```text
http://localhost:8080
```

and return to the Jenkins dashboard.

<br/>

## Step 4. Add the GCP Service Account Key to Jenkins

Jenkins also needs authentication with Google Cloud.



### 4.1 Create a Secret File Credential

In Jenkins, go to:

```text
Jenkins Dashboard
        ↓
Manage Jenkins
        ↓
Credentials
        ↓
Global
        ↓
Add Credentials
```

For the credential type, select:

```text
Secret file
```

Then upload the service-account JSON file.

For example:

```text
gcp-service-account.json
```

Give the credential an ID such as:

```text
GCP_KEY
```

Then create the credential.

#### Why use a secret file?

The JSON file contains credentials that allow Jenkins to authenticate with Google Cloud.

Therefore, it should **not be committed to GitHub**.

```text
❌ GitHub
❌ Jenkinsfile
❌ Dockerfile

        ↓

✅ Jenkins Credentials
```

<br/>

## Step 5. Configure google cloud

### 5.1 Enable Required Google Cloud APIs

Go to the Google Cloud Console.

Navigate to:

```text
APIs & Services
      ↓
Library
```

The transcript enables three APIs.

<br/>

#### Container Registry API

Search for:

```text
Google Container Registry API
```

Open it and enable the API if it is not already enabled.

This allows interaction with the container registry.

<br/>

#### Artifact Registry API

Search for:

```text
Artifact Registry API
```

Enable it.

This is Google's newer container/package registry service and is important for modern Google Cloud deployments.

<br/>

#### Cloud Resource Manager API

Search for:

```text
Cloud Resource Manager API
```

Enable it.



### Required APIs

```text
Google Container Registry API
Artifact Registry API
Cloud Resource Manager API
```

<br/>

### 5.2 Configure the GCP Service Account

Go to:

```text
IAM & Admin
      ↓
Service Accounts
```

Find the service account used by the project.

then adds additional permissions to that service account.

It assigns:

```text
Owner
```

along with existing permissions.

#### note

The transcript uses the **Owner** role for simplicity, but this is much broader than normally required for production.

A production CI/CD system should follow the **principle of least privilege** and grant only the roles Jenkins actually needs.

<br/>


## Step 6. Add below codes to Jenkinsfile


```groovy
pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        // Google Cloud Project ID
        GCP_PROJECT   = 'your-lowercase-project-id' 
        // Define your Artifact Registry Region and Repo Name
        GCP_REGION    = 'us-central1'
        GCP_REPO      = 'ml-project-repo'
        GCLOUD_PATH   = '/usr/bin'
    }

    stages {
        stage('Cloning Github Repo to Jenkins') {
            steps {
               ...
            }
        }

        stage('Setting Up Virtual Environment and Installing Dependencies'){
            steps {
                ...
            }
        }

        stage('Building and Pushing Docker Image to Artifact Registry') {
            steps {
                withCredentials([
                    file(credentialsId: 'GCP_KEY', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    echo 'Logging into Google Artifact Registry and pushing image...'

                    sh '''
                        # 1. Export the Application Default Credentials file path
                        export GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}"

                        gcloud auth login --cred-file="${GOOGLE_APPLICATION_CREDENTIALS}" --quiet

                        # 2. Automatically create the Artifact Registry repo if it does not exist
                        gcloud artifacts repositories create "$GCP_REPO" \
                            --repository-format=docker \
                            --location="$GCP_REGION" \
                            --description="Docker repository for ML App" \
                            --quiet || echo "Repository already exists, moving forward..."

                        # 3. Build the Docker container image locally
                        docker build -t "${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPO}/ml-project:latest" .

                        # 4. Generate a short-lived 1-hour access token from your credential file
                        TOKEN=$(gcloud auth print-access-token)

                        # 5. Direct login to Docker registry to bypass the file permission lock
                        echo "$TOKEN" | docker login -u oauth2accesstoken --password-stdin "https://${GCP_REGION}-docker.pkg.dev"

                        # 6. Push the image to your repository
                        docker push "${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPO}/ml-project:latest"   
                    '''
                }


            }
        }


    }
}

```

The exact credential ID and environment-variable names must match the values configured in your Jenkinsfile.

<br/>

## Step 7. Push the Updated Jenkinsfile to GitHub

Once the Jenkinsfile has been modified:

```bash
git add Jenkinsfile
```

Commit:

```bash
git commit -m "Build and push Docker image to GCR"
```

Push:

```bash
git push origin main
```

Now GitHub contains the updated CI/CD pipeline.

<br/>

## Step 8. Run the Jenkins Pipeline

Go to:

```text
Jenkins Dashboard
      ↓
MLOps-1
      ↓
Build Now
```

Jenkins will execute the pipeline from the beginning.

#### Check Console Output

Whether it has been successfully built or not.



<br/>

## Step 8. Verify the Image in Google Cloud

After Jenkins reports:

```text
Finished: SUCCESS
```

open Google Cloud Console.

Search for:

```text
Container Registry
```

Then open the images section.

You should find an image similar to:

```text
gcr.io
└── <your-project-id>
    └── ml-project
        └── latest
```

This confirms that the Docker image was successfully pushed to Google Cloud.

<br/>

## Current CI/CD Progress

At this point, the pipeline has reached:

```text
┌──────────────────────────────────────┐
│          MLOps CI/CD Pipeline        │
├──────────────────────────────────────┤
│                                      │
│  1. Jenkins Setup               ✓    │
│             ↓                        │
│  2. GitHub Integration           ✓    │
│             ↓                        │
│  3. Project Dockerfile           ✓    │
│             ↓                        │
│  4. Virtual Environment          ✓    │
│             ↓                        │
│  5. Build Docker Image           ✓    │
│     + Push to GCR                ✓    │
│             ↓                        │
│  6. Deploy to Google Cloud Run        │
│                                      │
└──────────────────────────────────────┘
```



> **Jenkins authenticates with Google Cloud, builds the ML project's Docker image using the project Dockerfile, and pushes that image to Google Container Registry.**

The Docker image is now available in Google Cloud and is ready for the **next stage: deploying the image to Google Cloud Run**. 
