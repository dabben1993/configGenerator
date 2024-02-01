pipeline {
    agent any

    options {
        buildDiscarder(logRotator(artifactNumToKeepStr: '1', numToKeepStr: '5'))
        disableConcurrentBuilds()
        timestamps()
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
                    environment {
                        GIT_ACCESS_TOKEN = credentials('your-git-access-token-credential-id')
                        AWS_SECRET_KEY_ID = credentials('your-aws-access-key-id-credential-id')
                        AWS_SECRET_ACCESS_KEY = credentials('your-aws-secret-access-key-credential-id')
                    }

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
