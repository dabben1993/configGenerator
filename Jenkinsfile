pipeline {
    agent any

    options {
        buildDiscarder(logRotator(artifactNumToKeepStr: '1', numToKeepStr: '5'))
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        PYTHON_PATH = 'C:\\Users\\tbarkman\\AppData\\Local\\Programs\\Python\\Python312'
        GIT_ACCESS_TOKEN = credentials('GIT_ACCESS_TOKEN')
        AWS_SECRET_KEY_ID = credentials('AWS_SECRET_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        BITBUCKET_ACCESS_TOKEN = credentials('BITBUCKET_ACCESS_TOKEN')
    }

    stages {

        stage('Setup') {
            steps {
                script {
                    bat "${env.PYTHON_PATH}\\Scripts\\pip.exe install -r requirements.txt"
                }
            }
        }

        stage('Run App') {
            steps {
                script {
                    dir('src') {
                        bat "${env.PYTHON_PATH}\\python.exe main.py"
                    }
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
