pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:latest
    args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
  - name: docker
    image: docker:24.0.5
    command:
    - cat
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
volumes:
- name: dockersock
  hostPath:
    path: /var/run/docker.sock
"""
        }
    }

    environment {
        DOCKER_HUB = 'limbo-123'
        IMAGE_NAME = 'flask-task-manager'
        KUBECONFIG_CREDENTIALS = 'kubeconfig'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/limbo-123/ci-cd-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        dockerImage = docker.build("${DOCKER_HUB}/${IMAGE_NAME}:${env.BUILD_ID}")
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        script {
                            docker.withRegistry('', 'docker-hub-creds') {
                                dockerImage.push()
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    withCredentials([file(
                        credentialsId: "${KUBECONFIG_CREDENTIALS}",
                        variable: 'KUBECONFIG_FILE'
                    )]) {
                        sh '''
                            export KUBECONFIG=$KUBECONFIG_FILE
                            kubectl set image deployment/flask-task-manager flask-app=${DOCKER_HUB}/${IMAGE_NAME}:${BUILD_ID} --record
                            kubectl rollout status deployment/flask-task-manager
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed! Check logs.'
        }
    }
}
