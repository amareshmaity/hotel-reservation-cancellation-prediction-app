pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        // GCP_PROJECT = 'mlops-hotel-1'
        // GCP_REGION    = 'us-central1'
        // GCP_REPO      = 'ml-hotel-repo'
        // GCLOUD_PATH   = '/usr/bin'

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


    }
}