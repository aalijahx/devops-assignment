pipeline {
    agent any
    environment {
        DOCKER_USER = 'aalijahx'
        // Ensure you created 'docker-hub-creds' in Jenkins -> Manage Jenkins -> Credentials
        DOCKER_HUB_CREDS = credentials('docker-hub-creds')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build & Push Images') {
            steps {
                script {
                    // Build & Push API
                    sh "docker build -t ${DOCKER_USER}/bezkoder-api:latest ./bezkoder-api"
                    docker.withRegistry('', 'docker-hub-creds') {
                        sh "docker push ${DOCKER_USER}/bezkoder-api:latest"
                    }
                    // Build & Push UI (Baked with your EC2 IP)
                    sh "docker build --build-arg REACT_APP_API_BASE_URL=http://13.60.224.71:6868/api -t ${DOCKER_USER}/bezkoder-ui:latest ./bezkoder-ui"
                    docker.withRegistry('', 'docker-hub-creds') {
                        sh "docker push ${DOCKER_USER}/bezkoder-ui:latest"
                    }
                }
            }
        }
        stage('Deploy Part-II') {
            steps {
                // Specifically targeting only Part-II services
                sh 'docker-compose up -d api-automation ui-automation'
            }
        }
    }
    post {
        always {
            sh 'docker image prune -f'
        }
    }
}
