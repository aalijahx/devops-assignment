pipeline {
    agent any

    environment {
        DOCKER_USER = 'aalijahx'
        // This ID must match the ID you gave in Jenkins Credentials
        DOCKER_HUB_CREDS = credentials('docker-hub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls the latest code from your repo
                checkout scm
            }
        }

        stage('Build & Push API') {
            steps {
                script {
                    def apiImage = docker.build("${DOCKER_USER}/bezkoder-api:latest", "./bezkoder-api")
                    docker.withRegistry('', 'docker-hub-creds') {
                        apiImage.push()
                    }
                }
            }
        }

        stage('Build & Push UI') {
            steps {
                script {
                    // We bake the EC2 IP into the UI build
                    def uiImage = docker.build("${DOCKER_USER}/bezkoder-ui:latest", "--build-arg REACT_APP_API_BASE_URL=http://13.60.224.71:6868/api ./bezkoder-ui")
                    docker.withRegistry('', 'docker-hub-creds') {
                        uiImage.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Restarts the containers with the newly built images
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            // Clean up images locally to save EC2 space
            sh 'docker image prune -f'
        }
    }
}
