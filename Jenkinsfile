
pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\Payal Suryakar\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        IMAGE_NAME = 'python-devops-cicd:latest'
        IMAGE_REPO = 'ghcr.io/l00213632/python-devops-cicd'
        CONTAINER_NAME = 'python-devops-app-ci'
        KUBECONFIG = 'C:\\Users\\Payal Suryakar\\.kube\\config'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Kubernetes Access Check') {
            steps {
                bat 'kubectl config current-context'
                bat 'kubectl get nodes'
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

        stage('Publish Docker Image to GHCR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'ghcr-credentials',
                    usernameVariable: 'GHCR_USER',
                    passwordVariable: 'GHCR_TOKEN'
                )]) {
                    bat '''
                        @echo off

                        powershell -NoProfile -NonInteractive -Command "$env:GHCR_TOKEN | docker login ghcr.io -u $env:GHCR_USER --password-stdin"
                        if errorlevel 1 exit /b 1

                        docker tag %IMAGE_NAME% %IMAGE_REPO%:%GIT_COMMIT%
                        if errorlevel 1 exit /b 1

                        docker tag %IMAGE_NAME% %IMAGE_REPO%:latest
                        if errorlevel 1 exit /b 1

                        docker push %IMAGE_REPO%:%GIT_COMMIT%
                        if errorlevel 1 exit /b 1

                        docker push %IMAGE_REPO%:latest
                        if errorlevel 1 exit /b 1

                        docker logout ghcr.io
                    '''
                }
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
                    @echo off
                    powershell -NoProfile -Command "for ($i=0; $i -lt 20; $i++) { try { Invoke-RestMethod http://localhost:5002/health -TimeoutSec 3; exit 0 } catch { Start-Sleep -Seconds 3 } }; exit 1"
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    @echo off

                    kubectl set image deployment/python-devops-app python-devops-app=%IMAGE_REPO%:%GIT_COMMIT%
                    if errorlevel 1 exit /b 1

                    kubectl rollout status deployment/python-devops-app --timeout=180s
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                bat '''
                    @echo off

                    echo Checking Kubernetes deployment...
                    kubectl get deployment python-devops-app
                    if errorlevel 1 exit /b 1

                    echo Checking Kubernetes pods...
                    kubectl get pods -l app=python-devops-app
                    if errorlevel 1 exit /b 1

                    echo Checking deployed application health...
                    kubectl exec deployment/python-devops-app -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').read().decode())"
                    if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
            echo 'Automated tests passed.'
            echo 'Code quality checks passed.'
            echo 'Security scans passed.'
            echo 'Docker image published to GitHub Container Registry.'
            echo 'Local Docker deployment verified.'
            echo 'Kubernetes deployment and health verification completed.'
            echo 'Application: http://localhost:5002'
            echo 'Health: http://localhost:5002/health'
            echo 'Metrics: http://localhost:5002/metrics'
        }

        failure {
            echo 'Pipeline failed. Check the failed stage in Jenkins Console Output.'
        }
    }
}
