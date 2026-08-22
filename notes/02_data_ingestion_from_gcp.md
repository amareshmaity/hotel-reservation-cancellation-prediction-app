### Data Ingestion (GCP Bucket → Local Project)

### Learning Objective

Understand:

- What is Data Ingestion?
- Why Data Ingestion is required?
- What is a Service Account?
- How to create a Service Account in GCP?
- How to grant bucket access?
- How to connect VS Code with GCP?
- How to configure data extraction?
- How to prepare train-test splitting?

<br/>

## 1. What is Data Ingestion?

Data Ingestion is the process of:

```text
GCP Bucket
      ↓
Extract Dataset
      ↓
Store in Local Project
      ↓
Train-Test Split
```

In our project:

1. Dataset is stored in a GCP Bucket.
2. We fetch the dataset from GCP.
3. Store it inside our project.
4. Split it into Train and Test datasets.

<br/>

### Why Do We Need Data Ingestion?

Machine Learning code runs inside:

```text
VS Code
Jupyter Notebook
Python Scripts
```

But our dataset is stored in:

```text
Google Cloud Storage (GCS)
```

Therefore we must:

```text
Read data from GCS
↓
Bring it into project
↓
Use it for training
```

This entire process is called:

```text
Data Ingestion
```

<br/>

### Data Ingestion Workflow

```text
GCP Bucket
      ↓
Service Account Authentication
      ↓
Google Cloud Storage SDK
      ↓
Download CSV File
      ↓
Local Project Directory
      ↓
Train/Test Split
```

<br/>

## 2. What is a Service Account?

Google Cloud provides two types of accounts:

### IAM Account

Your personal Google account.

Example:

```text
yourname@gmail.com
```

Used for:

- Logging into GCP
- Managing resources
- Administration

<br/>

### Service Account

A machine account used by applications.

Example:

```text
mlops-project-1@gcp-project.iam.gserviceaccount.com
```

Used for:

- VS Code
- Python Applications
- APIs
- Jenkins
- Docker Containers

<br/>

#### Why Service Accounts?

Suppose:

```text
VS Code
      ↓
Needs access to
      ↓
GCP Bucket
```

Giving full access is dangerous.

Instead:

```text
Create Service Account
      ↓
Grant Limited Permissions
      ↓
Use Secure Access
```

<br/>

#### Benefits of Service Accounts

#### 1. Restricted Access

Can allow:

```text
Read Only
```

Can deny:

```text
Delete
Overwrite
Modify
```

#### 2. Security

Applications never use your personal Google account.

Only the service account credentials are used.

<br/>

## 3. Install Google Cloud CLI

### What is Google Cloud CLI?

Google Cloud Command Line Interface.

Used to:

- Authenticate
- Access GCP Services
- Run GCP Commands

<br/>

### Installation Steps

#### Step 1

Search:

```text
Google Cloud CLI
```

Open:

```text
https://cloud.google.com/sdk
```

#### Step 2

Download installer according to your OS:

```text
Windows
Linux
MacOS
```

#### Step 3

Install normally.

#### Step 4

Restart VS Code.

<br/>

### Verify Installation

Open terminal:

```bash
gcloud --version
```

Expected Output:

```text
Google Cloud SDK
xxx.xx.x
```

If you see:

```text
gcloud command not found
```

Installation failed.

<br/>

## 4. Required Packages

Add to:

```text
requirements.txt
```

```text
google-cloud-storage
pandas
scikit-learn
```

<br/>

Install packages:

```bash
pip install -e .
```

<br/>

## 5. Create Data Ingestion Module

Inside:

```text
src/
```

Create:

```text
data_ingestion.py
```

Purpose:

```text
Download data from GCP Bucket
Split data
Save train/test files
```

<br/>

## 6. Create Service Account

### Step 1

Open:

```text
GCP Console
```

### Step 2

Navigate:

```text
IAM & Admin
      ↓
Service Accounts
```

### Step 3

Click:

```text
Create Service Account
```

### Step 4

Give name:

```text
mlops-project-1
```

<br/>

## 7. Assign Roles

#### Add Role #1

```text
Storage Admin
```

Permission:

```text
Read Bucket
Write Bucket
Manage Objects
```

#### Add Role #2

```text
Storage Object Viewer
```

Permission:

```text
View Files
List Files
Read Metadata
```

Click:

```text
Continue
Done
```

<br/>

## 8. Grant Bucket Access

Open:

```text
Cloud Storage
      ↓
Buckets
```

Select your bucket.

<br/>

Choose:

```text
Manage Access
```

or

```text
Edit Access
```

<br/>

Click:

```text
Add Principal
```

<br/>

Add:

```text
Your Service Account Email
```

Example:

```text
mlops-project-1@project-id.iam.gserviceaccount.com
```

<br/>

Assign Roles Again

```text
Storage Admin
Storage Object Viewer
```

Save.

<br/>

## 9. Create JSON Key

Open:

```text
IAM & Admin
      ↓
Service Accounts
```

<br/>

Select:

```text
mlops-project-1
```

<br/>

Choose:

```text
Manage Keys
```

<br/>

Click:

```text
Add Key
      ↓
Create New Key
```

<br/>

Select:

```text
JSON
```

<br/>

Click:

```text
Create
```

A JSON file will automatically download.

Example:

```text
mlops-project-1-key.json
```

<br/>

### What is Inside JSON?

Contains:

```text
Project ID
Client Email
Private Key
Authentication Information
```

Used by Python to authenticate with GCP.

<br/>

## 10. Connect VS Code to GCP

Locate downloaded JSON file.

Example:

```text
Downloads/
mlops-project-1-key.json
```

<br/>

Copy Full Path.

Example:

```text
C:\Users\Amaresh\Downloads\mlops-project-1-key.json
```

<br/>

Open VS Code Terminal

Run:

```bash
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\**\mlops-project-1-key.json
```

Windows Command Prompt

<br/>

PowerShell:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\**\mlops-project-1-key.json"
```

<br/>

This command:

```text
Authenticates VS Code
↓
Authenticates Python
↓
Allows Bucket Access
```

<br/>

---

If Google Cloud organization has explicitly blocked downloading JSON private keys then use below method (**Service Account Impersonation**):

1. Go to IAM & Admin > Service Accounts in the Google Cloud Console.
2. Click on the email address of the target service account.
3. Navigate to the Permissions tab at the top. Click Grant Access.
4. In the New principals field, type your personal user email.
5. In the Role field, choose Service Account Token Creator and click Save.

   (Note: Keeping Storage Admin and Storage Object Viewer directly attached to the service account is perfectly correct, as it needs those permissions to read the bucket.)

6. In your vscode terminal use below command:

   ```bash
   gcloud auth application-default login --impersonate-service-account=<YOUR_SERVICE_ACCOUNT_EMAIL@YOUR_PROJECT.iam.gserviceaccount.com>
   
   ```
   This will download the <project_name.json> file into your local directory. Then you have to set the credential using below method.

   ```bash
   set GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT_ID in the google cloud>

   or 

   set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\**\mlops-project-1-key.json

   ```

---

<br/>

## 11. Create Configuration File

Inside:

```text
config/
```

Create:

```text
config.yaml
```

### Data Ingestion Configuration

```yaml
data_ingestion:
  bucket_name: "mybucket9789"

  bucket_file_name: "hotel_reservation.csv"

  train_ratio: 0.8
```

<br/>

## Create below files

1. `paths_config.py` inside config
2. `common.py` inside src/utils
3. `data_ingestion.py` inside src/components

<br/>

## 12. Test file

Run command in the terminal

```bash
python src/components/data_ingestion.py
```
