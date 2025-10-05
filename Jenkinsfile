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
                echo 'Running unit tests inside Docker (if tests exist)...'
                // Run pytest only if tests folder exists
                sh '''
                if [ -d "tests" ]; then
                    docker run --rm -v $(pwd)/tests:/app/tests $IMAGE_NAME pytest tests/
                else
                    echo "No tests found, skipping pytest."
                fi
                '''
            }
        }

        // -------- Code Quality Stage --------
        stage('Code Quality') {
            steps {
                echo 'Running SonarQube analysis (if configured)...'
                sh '''
                if command -v sonar-scanner >/dev/null 2>&1; then
                    sonar-scanner
                else
                    echo "SonarQube scanner not found, skipping."
                fi
                '''
            }
        }

        // -------- Security Stage --------
        stage('Security Scan') {
            steps {
                echo 'Running security scan with Bandit (if installed)...'
                sh '''
                if command -v bandit >/dev/null 2>&1; then
                    bandit -r app/
                else
                    echo "Bandit not installed, skipping security scan."
                fi
                '''
            }
        }

        // -------- Deploy Stage --------
        stage('Deploy to Test') {
            steps {
                echo 'Deploying Docker container to test environment...'
                sh 'docker run -d -p 5000:5000 --name $IMAGE_NAME $IMAGE_NAME || echo "Container already running"'
            }
        }

        // -------- Monitoring Stage --------
        stage('Monitoring') {
            steps {
                echo 'Checking health endpoint (if app running)...'
                sh '''
                if curl -s --head http://localhost:5000 | grep "200 OK" >/dev/null; then
                    echo "App is running"
                else
                    echo "App not running or endpoint not found"
                fi
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers safely...'
            sh '''
            docker ps -q --filter "name=$IMAGE_NAME" | xargs -r docker stop || true
            docker ps -aq --filter "name=$IMAGE_NAME" | xargs -r docker rm || true
            '''
        }
    }
}
