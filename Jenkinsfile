pipeline {
    agent any

    options {
        // Set the working dir for the entire pipeline
        buildDiscarder(logRotator(artifactNumToKeepStr: '1', numToKeepStr: '5'))
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        PYTHON_PATH = 'C:\\Users\\tbarkman\\AppData\\Local\\Programs\\Python\\Python312'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {
                    bat "${env.PYTHON_PATH}\\Scripts\\pip.exe install -r requirements.txt"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    bat "${env.PYTHON_PATH}\\python.exe -m unittest discover -s tests"
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
