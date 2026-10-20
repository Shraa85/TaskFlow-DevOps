
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Environment') {
            steps {
                sh 'echo "TaskFlow CI/CD Pipeline Started"'
                sh 'python3 --version'
                sh 'docker --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Automated Tests') {
            steps {
                sh 'python3 -m pytest -q'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t taskflow:latest .'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker image built.'
        }
        failure {
            echo 'FAILED: Check Console Output for the error.'
        }
    }
}
