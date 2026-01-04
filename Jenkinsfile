pipeline {
    agent any

    environment {
        DOCKER_HUB = 'limbo-123'
        IMAGE_NAME = 'flask-task-manager'
        KUBECONFIG = '/home/vm01/.kube/config'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/limbo-123/ci-cd-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  docker build -t ${DOCKER_HUB}/${IMAGE_NAME}:${BUILD_ID} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker push ${DOCKER_HUB}/${IMAGE_NAME}:${BUILD_ID}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes (Minikube)') {
            steps {
                sh '''
                  kubectl set image deployment/flask-task-manager \
                  flask-app=${DOCKER_HUB}/${IMAGE_NAME}:${BUILD_ID}
                  kubectl rollout status deployment/flask-task-manager
                '''
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline Completed Successfully"
        }
        failure {
            echo "Pipeline Failed"
        }
    }
}
