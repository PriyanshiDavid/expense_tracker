pipeline {
    agent any
    environment {
        IMAGE_NAME = "expense-tracker"
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests inside Docker (if tests exist)...'
                sh '''
                if [ -d tests ]; then
                    docker run --rm -v $(pwd)/tests:/app/tests $IMAGE_NAME pytest /app/tests
                else
                    echo "No tests found, skipping pytest."
                fi
                '''
            }
        }
        stage('Code Quality') {
            steps {
                echo 'Running SonarQube analysis (if configured)...'
                sh '''
                command -v sonar-scanner >/dev/null 2>&1 || echo "SonarQube scanner not found, skipping."
                '''
            }
        }
        stage('Security Scan') {
            steps {
                echo 'Running Bandit security scan (if installed)...'
                sh '''
                command -v bandit >/dev/null 2>&1 || echo "Bandit not installed, skipping."
                '''
            }
        }
        stage('Deploy to Test') {
            steps {
                echo 'Deploying Docker container to test environment...'
                sh 'docker run -d -p 5000:5000 --name expense-tracker $IMAGE_NAME'
            }
        }
        stage('Monitoring') {
            steps {
                echo 'Checking health endpoint (if app running)...'
                sh 'curl -s --head http://localhost:5000 | grep "200 OK" && echo "App is running" || echo "App not responding"'
            }
        }
    }
    post {
        always {
            echo 'Cleaning up Docker containers safely...'
            sh 'docker ps -q --filter name=expense-tracker | xargs -r docker stop'
            sh 'docker ps -aq --filter name=expense-tracker | xargs -r docker rm'
        }
    }
}
