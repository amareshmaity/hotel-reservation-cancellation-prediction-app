pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'project-f3a6458e-65bc-4dab-81d'
        GCP_REGION    = 'us-central1'
        GCP_REPO      = 'ml-project-repo'
        GCLOUD_PATH   = '/usr/bin'

    }

    stages {
        stage('Cloning Github Repo to Jenkins') {

            steps {

                echo 'Cloning Github repo to Jenkins ... '

                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/amareshmaity/hotel-reservation-cancellation-prediction-app.git']])
            }
        }

        stage('Setting Up Virtual Environment and Installing Dependencies'){
            steps {
                echo 'Setting up the virtual environment and installing dependencies ... '

                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }

        stage('Building and Pushing Docker Image to Artifact Registry') {
            steps {
                withCredentials([
                    file(credentialsId: 'GCP_KEY', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                    ]) {
                        echo 'Ensuring repo exists, then building and pushing Docker image...'

                        sh '''
                        export PATH=$PATH:$GCLOUD_PATH

                        gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
                        gcloud config set project "$GCP_PROJECT"

                        gcloud artifacts repositories create $GCP_REPO \
                            --repository-format=docker \
                            --location=$GCP_REGION \
                            --description="Docker repository for ML App" \
                            --if-not-exists

                        gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev --quiet

                        docker build -t ${GCP_REGION}-docker.pkg.dev/$GCP_PROJECT/$GCP_REPO/ml-project:latest .

                        docker push ${GCP_REGION}-docker.pkg.dev/$GCP_PROJECT/$GCP_REPO/ml-project:latest   
                        
                        '''
                    }
            }
        }
    }
}