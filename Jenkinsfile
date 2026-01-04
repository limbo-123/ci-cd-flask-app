pipeline {
  agent {
    kubernetes {
      label 'kaniko-agent'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:latest

  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - cat
    tty: true

  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
"""
    }
  }

  environment {
    IMAGE = "limbo-123/flask-task-manager:${BUILD_ID}"
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/limbo-123/ci-cd-flask-app.git'
      }
    }

    stage('Build & Push Image') {
      steps {
        container('kaniko') {
          withCredentials([usernamePassword(
            credentialsId: 'docker-hub-creds',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh '''
              mkdir -p /kaniko/.docker

              cat <<EOF > /kaniko/.docker/config.json
              {
                "auths": {
                  "https://index.docker.io/v1/": {
                    "username": "$DOCKER_USER",
                    "password": "$DOCKER_PASS"
                  }
                }
              }
              EOF

              /kaniko/executor \
                --dockerfile=Dockerfile \
                --context=. \
                --destination=$IMAGE
            '''
          }
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        container('kubectl') {
          sh '''
            kubectl set image deployment/flask-task-manager \
              flask-app=$IMAGE --record

            kubectl rollout status deployment/flask-task-manager
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ CI/CD pipeline completed successfully"
    }
    failure {
      echo "❌ Pipeline failed – check logs"
    }
  }
}
