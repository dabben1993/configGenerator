pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {
                    bat 'pip install -r requirements.txt'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    bat 'python -m unittest discover -s tests'
                }
            }
        }
    }

    post {
    }
}
