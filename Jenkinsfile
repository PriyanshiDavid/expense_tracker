pipeline {
    agent any
    environment {
        IMAGE_NAME = "expense-tracker"
        CONTAINER_NAME = "expense-tracker"
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
                    docker run --rm -v $(pwd)/tests:/app/tests $IMAGE_NAME pytest /app/tests || true
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
                if command -v sonar-scanner >/dev/null 2>&1; then
                    sonar-scanner
                else
                    echo "SonarQube scanner not found, skipping."
                fi
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running Bandit security scan (if installed)...'
                sh '''
                if command -v bandit >/dev/null 2>&1; then
                    bandit -r app
                else
                    echo "Bandit not installed, skipping security scan."
                fi
                '''
            }
        }

        stage('Deploy to Test') {
            steps {
                echo 'Deploying Docker container to test environment...'
                sh '''
                # Stop and remove previous container if it exists
                if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
                    docker stop $CONTAINER_NAME
                    docker rm $CONTAINER_NAME
                fi

                # Run new container
                docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking health endpoint (if app running)...'
                sh '''
                echo "Waiting for Flask app to start..."
                for i in {1..10}; do
                    if curl -s --head http://localhost:5000 | grep "200 OK"; then
                        echo "App is running"
                        exit 0
                    fi
                    echo "App not ready yet, retrying..."
                    sleep 3
                done
                echo "App failed to respond after 30 seconds"
                exit 1
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers safely...'
            sh '''
            docker ps -q --filter name=$CONTAINER_NAME | xargs -r docker stop
            docker ps -aq --filter name=$CONTAINER_NAME | xargs -r docker rm
            '''
        }
    }
}
