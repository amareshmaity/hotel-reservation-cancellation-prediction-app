pipeline {
    agent any

    stages {
        stage('Cloning Github Repo to Jenkins') {

            steps {

                echo 'Cloning Github repo to Jenkins ... '

                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/amareshmaity/hotel-reservation-cancellation-prediction-app.git']])
            }
        }
    }
}