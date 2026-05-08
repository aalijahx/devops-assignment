pipeline {
    agent any

    environment {
        DOCKER_USER = 'aalijahx'
        DOCKER_HUB_CREDS = credentials('docker-hub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                // Fetch code from the GitHub repository [cite: 61]
                checkout scm
            }
        }

        stage('Build & Push Images') {
            steps {
                script {
                    // Build Backend
                    sh "docker build -t ${DOCKER_USER}/bezkoder-api:latest ./bezkoder-api"
                    
                    // Build UI with specific IP configuration
                    sh "docker build --build-arg REACT_APP_API_BASE_URL=http://13.60.224.71:8082/api -t ${DOCKER_USER}/bezkoder-ui:latest ./bezkoder-ui"
                    
                    // Authenticate and push to Docker Hub
                    docker.withRegistry('', 'docker-hub-creds') {
                        sh "docker push ${DOCKER_USER}/bezkoder-api:latest"
                        sh "docker push ${DOCKER_USER}/bezkoder-ui:latest"
                    }
                }
            }
        }

        stage('Deploy Part-II') {
            steps {
                // Ensure automation containers are launched [cite: 56, 61]
                sh 'docker-compose up -d api-automation ui-automation'
            }
        }

        stage('Test Stage') {
            steps {
                script {
                    // Build the testing environment using the Dockerfile [cite: 61, 64]
                    sh "docker build -t selenium-tests -f Dockerfile.test ."
                    
                    // Run 15 Selenium test cases in a containerized environment [cite: 51, 68]
                    // --network host allows the test container to reach the app on port 9000
                    sh "docker run --network host selenium-tests"
                }
            }
        }
    }

    post {
        always {
            script {
                // Requirement: Email test results to the collaborator who made the push [cite: 77]
                // Hardcoded recipient ensures qasimalik@gmail.com receives results [cite: 76, 77]
                emailext (
                    subject: "Jenkins Test Results: ${currentBuild.fullDisplayName}",
                    body: """The automation pipeline has finished.
                             Result: ${currentBuild.result}
                             Check the Jenkins dashboard for the 15 Selenium test case results.""",
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider'], 
                        [$class: 'CulpritsRecipientProvider']
                    ],
                    to: 'aalijahmuhammad13@gmail.com'
                )
            }
            // Cleanup to maintain EC2 disk space
            sh 'docker image prune -f'
        }
    }
}
