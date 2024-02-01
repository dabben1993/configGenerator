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
                    bat 'C:\\Users\\tbarkman\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pip.exe install -r requirements.exe'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    bat 'C:\\Users\\tbarkman\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m unittest discover -s tests'
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
