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
        always {
            echo 'always'
        }
        success {
            echo 'Build and test succeeded'
        }
        failure {
            echo 'Build and test failed'
        }
    }
}
