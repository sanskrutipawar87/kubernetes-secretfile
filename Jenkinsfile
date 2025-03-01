pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sanskrutipawar/student-management:latest"  // Replace with your Docker Hub image
        KUBE_CONFIG = "$HOME/.kube/config" // Ensure Kubernetes is configured
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/your-repo/student-management-system.git'  // Replace with your GitHub repo
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'dockerhub-credentials', variable: 'DOCKER_PASSWORD')]) {
                        sh """
                            echo "$DOCKER_PASSWORD" | docker login -u sanskrutipawar --password-stdin
                            docker push $DOCKER_IMAGE
                        """
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -f kubernetes-secretfile/student-setup.yaml"
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh "kubectl get pods"
                    sh "kubectl get services"
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Deployment failed! Check the logs."
        }
    }
}
