pipeline {
    agent any

    environment {
        IMAGE_NAME = "expense-tracker"
    }

    stages {

        // -------- Build Stage --------
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        // -------- Test Stage --------
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'pytest tests/'   // Make sure you have test files in tests/
            }
        }

        // -------- Code Quality Stage --------
        stage('Code Quality') {
            steps {
                echo 'Running SonarQube analysis...'
                sh 'sonar-scanner'   // Requires SonarQube scanner installed on Jenkins
            }
        }

        // -------- Security Stage --------
        stage('Security Scan') {
            steps {
                echo 'Running security scan with Bandit...'
                sh 'bandit -r app/'  // Install Bandit via pip: pip install bandit
            }
        }

        // -------- Deploy Stage --------
        stage('Deploy to Test') {
            steps {
                echo 'Deploying Docker container to test environment...'
                sh 'docker run -d -p 5000:5000 $IMAGE_NAME'
            }
        }

        // -------- Monitoring Stage --------
        stage('Monitoring') {
            steps {
                echo 'Checking health endpoint...'
                sh 'curl http://localhost:5000/health'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers...'
            sh 'docker ps -q | xargs -r docker stop'
        }
    }
}
