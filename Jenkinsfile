
pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\Payal Suryakar\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        IMAGE_NAME = 'python-devops-cicd:latest'
        CONTAINER_NAME = 'python-devops-app-ci'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                bat '"%PYTHON%" -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements-dev.txt'
            }
        }

        stage('Unit Tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Code Quality') {
            steps {
                bat '.venv\\Scripts\\ruff.exe check app tests run.py'
            }
        }

        stage('Security Scan') {
            steps {
                bat '.venv\\Scripts\\bandit.exe -r app run.py -ll'
                bat '.venv\\Scripts\\pip-audit.exe -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat '''
                    docker rm -f %CONTAINER_NAME% 2>NUL
                    docker run -d --name %CONTAINER_NAME% -p 5002:5000 --restart unless-stopped %IMAGE_NAME%
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                    for /L %%i in (1,1,20) do (
                        curl.exe -fsS http://localhost:5002/health && exit /b 0
                        timeout /t 3 /nobreak >NUL
                    )
                    exit /b 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
            echo 'Application: http://localhost:5002'
            echo 'Health: http://localhost:5002/health'
            echo 'Metrics: http://localhost:5002/metrics'
        }
        failure {
            echo 'Pipeline failed. Check the failed stage in Jenkins Console Output.'
        }
    }
}
