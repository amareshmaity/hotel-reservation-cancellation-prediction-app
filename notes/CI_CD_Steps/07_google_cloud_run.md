## Step 1:

Add below stage to Jenkinsfile

```bash
        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    echo 'Deploying application to Google Cloud Run...'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}

                    # Activate service account
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}

                    # Deploy the pushed image to Cloud Run
                    gcloud run deploy hotel-prediction-service \
                        --image=${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPO}/ml-project:latest \
                        --region=${GCP_REGION} \
                        --platform=managed \
                        --port=8080 \
                        --allow-unauthenticated \
                        --quiet
                    '''
                }
            }

```

## Step 2:

Change the port in the `application.py` from 5000 to 8080

## Step 3:

Now go to google console, search for google run, click on application inside it.

Click on the URL to see the application running.
