# 🏨 Hotel Reservation Cancellation Prediction - End-to-End MLOps Project

## Overview

Hotel reservation cancellations significantly impact revenue management, occupancy planning, and operational efficiency in the hospitality industry.

This project builds a production-ready Machine Learning system that predicts whether a customer is likely to cancel a hotel reservation before their scheduled stay. The solution follows modern MLOps practices including experiment tracking, data versioning, CI/CD automation, containerization, cloud deployment, and model serving.

The project demonstrates how a machine learning model can move from experimentation to a fully automated production deployment pipeline.

---

## Business Problem

Hotels frequently face revenue losses due to unexpected reservation cancellations.

By predicting potential cancellations in advance, hotels can:

### Revenue Management

* Reduce revenue loss caused by empty rooms.
* Implement controlled overbooking strategies.
* Improve occupancy rates.

### Targeted Marketing

* Identify customers with high cancellation probability.
* Offer personalized discounts and promotions.
* Improve customer retention.

### Fraud Detection

* Detect suspicious booking behavior.
* Identify users who repeatedly cancel reservations.
* Reduce fraudulent booking activities.

---

## Project Architecture

```text
                ┌─────────────────────┐
                │ Hotel Reservation   │
                │ Dataset (Kaggle)    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Google Cloud Storage│
                │      (GCS Bucket)   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Data Ingestion      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Data Processing     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Model Training      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ MLflow Tracking     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Training Pipeline   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Flask Web App       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Docker Container    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Jenkins CI/CD       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Google Cloud Run    │
                └─────────────────────┘
```

---

## Technology Stack

### Machine Learning

* Python
* Scikit-Learn
* Pandas
* NumPy
* Matplotlib
* Seaborn

### MLOps

* MLflow
* DVC (Optional)
* Git
* GitHub

### Cloud

* Google Cloud Platform (GCP)
* Google Cloud Storage (GCS)
* Google Container Registry (GCR)
* Google Cloud Run

### Deployment

* Docker
* Jenkins

### Web Application

* Flask
* HTML
* CSS

---

## Dataset

**Dataset:** Hotel Reservation Dataset

The dataset contains booking-related information such as:

* Lead Time
* Number of Adults
* Number of Children
* Meal Plan
* Room Type
* Market Segment
* Average Price Per Room
* Number of Previous Cancellations
* Booking Status

### Target Variable

```text
booking_status

0 → Not Cancelled
1 → Cancelled
```

---

## Project Structure

```text
hotel-reservation-prediction/
│
├── artifacts/
│
├── config/
│   └── config.yaml
│
├── notebooks/
│   ├── EDA.ipynb
│   ├── Feature_Engineering.ipynb
│   └── Model_Training.ipynb
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_processing.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   ├── utils/
│   │   ├── common.py
│   │   └── logger.py
│   │
│   ├── exception.py
│   └── constants.py
│
├── templates/
│   └── index.html
│
├── static/
│
├── app.py
│
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── setup.py
├── .gitignore
├── README.md
└── LICENSE
```

---

## MLflow Experiment Tracking

This project uses MLflow for:

* Experiment Tracking
* Parameter Logging
* Metric Logging
* Model Versioning
* Artifact Management

Tracked information includes:

```text
✔ Accuracy
✔ Precision
✔ Recall
✔ F1 Score
✔ Hyperparameters
✔ Model Artifacts
```

---

## CI/CD Pipeline

The deployment workflow follows a complete CI/CD process.

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
Jenkins Pipeline
    │
    ├── Build
    ├── Test
    ├── Dockerize
    ├── Push Image to GCR
    └── Deploy
            │
            ▼
      Google Cloud Run
```

### Automated Steps

1. Push code to GitHub.
2. Jenkins triggers automatically.
3. Docker image is built.
4. Image is pushed to GCR.
5. Application is deployed to Cloud Run.
6. Updated application becomes live.

---

## Docker Deployment

Build image:

```bash
docker build -t hotel-reservation-prediction .
```

Run container:

```bash
docker run -p 8080:8080 hotel-reservation-prediction
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/your-username/hotel-reservation-prediction.git

cd hotel-reservation-prediction
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate.bat
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

or through `setup.py`

```bash
pip install -e .
```

### Run Training Pipeline

```bash
python src/pipeline/training_pipeline.py
```

### Run Flask Application

```bash
python app.py
```

---

## Future Improvements

* DVC-Based Data Versioning
* Kubernetes Deployment
* Airflow Data Pipelines
* Automated Retraining
* Model Monitoring
* Prometheus Integration
* Grafana Dashboards
* Drift Detection
* Feature Store Integration

---

## Key Learning Outcomes

This project demonstrates:

* End-to-End Machine Learning Workflow
* Production-Ready MLOps Architecture
* MLflow Experiment Tracking
* Docker Containerization
* Jenkins CI/CD Automation
* Cloud Deployment using GCP
* Flask Model Serving
* Industry Standard Project Structuring

---

## Author

**Amaresh Maity**

AI Engineer | Machine Learning Engineer | MLOps Enthusiast

GitHub: https://github.com/amareshmaity

LinkedIn: https://linkedin.com/in/amareshmaity

---

## License

This project is licensed under the MIT License.

```text
Copyright (c) 2026 Amaresh Maity

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software...
```
