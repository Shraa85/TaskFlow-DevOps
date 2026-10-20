pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install Dependencies') {
            steps {
                bat 'py -m pip install -r requirements.txt'
            }
        }
        stage('Automated Tests') {
            steps {
                bat 'py -m pytest -q'
            }
        }
        stage('Docker Build') {
            steps {
                bat 'docker build -t taskflow:latest .'
            }
        }
    }
}
