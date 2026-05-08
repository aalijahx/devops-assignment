pipeline {
    agent any

    environment {
        DOCKER_USER = 'aalijahx'
        // Ensure this ID matches the one in Jenkins -> Manage Jenkins -> Credentials
        DOCKER_HUB_CREDS = credentials('docker-hub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                // Fetches code from your GitHub repository [cite: 21, 61]
                checkout scm
            }
        }

        stage('Build & Push Images') {
            steps {
                script {
                    // Build and Push Backend API
                    sh "docker build -t ${DOCKER_USER}/bezkoder-api:latest ./bezkoder-api"
                    docker.withRegistry('', 'docker-hub-creds') {
                        sh "docker push ${DOCKER_USER}/bezkoder-api:latest"
                    }
                    
                    // Build and Push UI with your specific EC2 IP
                    sh "docker build --build-arg REACT_APP_API_BASE_URL=http://13.60.224.71:8082/api -t ${DOCKER_USER}/bezkoder-ui:latest ./bezkoder-ui"
                    docker.withRegistry('', 'docker-hub-creds') {
                        sh "docker push ${DOCKER_USER}/bezkoder-ui:latest"
                    }
                }
            }
        }

        stage('Deploy Part-II') {
            steps {
                // Brings deployment up on port 9000 using Docker Compose 
                sh 'docker-compose up -d api-automation ui-automation'
            }
        }

        stage('Test Stage') {
            steps {
                script {
                    // Builds a containerized environment for Selenium tests 
                    sh "docker build -t selenium-tests -f Dockerfile.test ."
                    
                    // Executes 15 Selenium test cases using headless Chrome [cite: 51, 54, 55]
                    // --network host allows the container to access port 9000 on the EC2
                    sh "docker run --network host selenium-tests"
                }
            }
        }
    }

    post {
        always {
            script {
                // Emails test results ONLY to the collaborator who made the push [cite: 77, 79]
                // This will email you if you push, or qasimalik@gmail.com if he pushes
                emailext (
                    subject: "Jenkins Test Results: ${currentBuild.fullDisplayName}",
                    body: """The automation pipeline has finished.
                             Result: ${currentBuild.result}
                             Check the Jenkins dashboard for the 15 Selenium test results.""",
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider'], 
                        [$class: 'CulpritsRecipientProvider']
                    ]
                )
            }
            // Cleanup unused images to save disk space
            sh 'docker image prune -f'
        }
    }
}
