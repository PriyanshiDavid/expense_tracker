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
                echo 'Running unit tests inside Docker...'
                sh 'docker run --rm $IMAGE_NAME pytest tests/'  // Runs tests inside container
            }
        }

        // -------- Code Quality Stage --------
        stage('Code Quality') {
            steps {
                echo 'Running SonarQube analysis inside Docker...'
                sh 'docker run --rm -v $PWD:/app $IMAGE_NAME sonar-scanner'  // Mount code for analysis
            }
        }

        // -------- Security Stage --------
        stage('Security Scan') {
            steps {
                echo 'Running security scan with Bandit inside Docker...'
                sh 'docker run --rm $IMAGE_NAME bandit -r app/'  // Runs Bandit inside container
            }
        }

        // -------- Deploy Stage --------
        stage('Deploy to Test') {
            steps {
                echo 'Deploying Docker container to test environment...'
                sh 'docker run -d -p 5000:5000 --name $IMAGE_NAME $IMAGE_NAME'
            }
        }

        // -------- Monitoring Stage --------
        stage('Monitoring') {
            steps {
                echo 'Checking health endpoint...'
                sh 'curl http://localhost:5000/health || echo "Service not ready yet"'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers...'
            sh 'docker ps -q | xargs -r docker stop'
            sh 'docker ps -a -q | xargs -r docker rm'
        }
    }
}
