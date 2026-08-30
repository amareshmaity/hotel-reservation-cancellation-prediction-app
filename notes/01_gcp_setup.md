### Module 1: Database Setup (GCP & Google Cloud Storage)

## Learning Objective

Understand:

* What is GCP (Google Cloud Platform)?
* Why cloud platforms are needed?
* What is a GCP Bucket?
* How to create a GCP Bucket?
* How to upload dataset into a GCP Bucket?

<br/>

## 1. What is GCP?

**GCP (Google Cloud Platform)** is a cloud computing service provided by Google.

It provides:

* Storage Services
* Databases
* Virtual Machines (VMs)
* Networking Services
* Application Hosting
* AI/ML Services
* Cloud Security Services

<br/>

## 2. Why Do We Need Cloud Platforms?

### Problem with Local Machines

When an application runs on your local computer:

* RAM comes from your PC
* Storage comes from your Hard Disk
* CPU comes from your Processor

This works fine during development.

However, when you want to make your application available on the Internet:

* Users cannot access your local machine directly.
* Local resources are limited.
* Applications must run 24/7.

<br/>

### Cloud Solution

Cloud providers like GCP offer:

#### Virtual Machines

A virtual machine is a remote computer that provides:

* RAM
* CPU
* Storage
* Operating System

These machines run on Google's infrastructure.

#### Storage Services

Cloud storage allows:

* Centralized data storage
* Easy access from anywhere
* Better scalability
* Better reliability

<br/>

## 3. What is a GCP Bucket?

A **GCP Bucket** is a cloud storage container used to store files and folders.

### Local Storage vs Cloud Storage

| Local Computer | GCP Cloud Storage |
| -------------- | ----------------- |
| Folder         | Bucket            |
| Files          | Objects           |
| Hard Disk      | Cloud Storage     |
| Local Access   | Internet Access   |



### Simple Analogy

#### Local PC

```text
Documents/
│
├── data.csv
├── image.png
└── report.pdf
```

#### GCP Bucket

```text
my_bucket/
│
├── data.csv
├── image.png
└── report.pdf
```

The only difference:

* Local folders are stored on your PC.
* Buckets are stored on Google's cloud servers.

<br/>

## Why Are We Using GCP Buckets?

In this MLOps project:

```text
Dataset
    ↓
GCP Bucket
    ↓
Data Ingestion Pipeline
    ↓
Local Project Directory
```

The bucket acts as the central storage location for the dataset.

<br/>

## Practical Procedure

### Step 1: Open GCP

Open browser and search:

```text
Google Cloud Platform
```

or visit:

```text
https://cloud.google.com
```



### Step 2: Create GCP Account

Create a Google Cloud account.

Benefits:

* Free Trial Credits
* Approximately $300 free credits
* Valid for 90 days



### Step 3: Open Cloud Storage

Search:

```text
Buckets
```

Open:

```text
Cloud Storage → Buckets
```



### Step 4: Create Bucket

Click:

```text
Create Bucket
```



### Step 5: Enter Bucket Name

Example:

```text
mybucket9789
```

#### Important Rule

Bucket names must be:

* Globally Unique
* Lowercase
* Without Special Characters

Example:

```text
amaresh-hotel-project-9789
```



### Step 6: Continue with Default Settings

Click:

```text
Continue
```

Keep default settings for:

* Location Type
* Storage Class
* Access Control


### Step 7: Disable Public Access Prevention

Find:

```text
Prevent Public Access
```

Uncheck:

```text
Enforce Public Access Prevention
```

### Reason

If enabled:

```text
Cannot access bucket publicly
```

For learning purposes:

```text
Disable it
```



### Step 8: Create Bucket

Click:

```text
Create
```

Wait a few seconds.

Bucket will be created.

<br/>

## Upload Dataset

### Step 1

Open created bucket.

Example:

```text
mybucket9789
```



### Step 2

Click:

```text
Upload
```

Choose:

```text
Upload Files
```



### Step 3

Select Dataset

Example:

```text
Hotel Reservation.csv
```



### Step 4

Upload

Wait until:

```text
File Successfully Uploaded
```

appears.





<br/>

## Database Setup Workflow

```text
Download Dataset
        ↓
Create GCP Account
        ↓
Create Storage Bucket
        ↓
Upload Dataset
        ↓
Rename Dataset
        ↓
Dataset Available in Cloud Storage
        ↓
Ready for Data Ingestion
```

<br/>

## What Happens Next?

```text
GCP Bucket
     ↓
Data Ingestion
     ↓
Train/Test Split
     ↓
Data Processing
     ↓
Model Training
```

The uploaded dataset will be fetched from the GCP Bucket during the **Data Ingestion** stage of the MLOps pipeline.

<br/>

gcloud cheatsheet - https://docs.cloud.google.com/sdk/docs/cheatsheet
