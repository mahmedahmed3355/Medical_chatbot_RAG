pipeline {
    agent any

    options {
        timestamps()
        ansiColor('xterm')
    }

    environment {
        AWS_REGION = credentials('aws-region')
        ECR_REPO = 'medical-rag-chatbot'
        IMAGE_TAG = "${BUILD_NUMBER}"
        SERVICE_NAME = 'medical-rag-chatbot'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh 'python -m ruff check app tests'
            }
        }

        stage('Test') {
            steps {
                sh 'python -m pytest -q'
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build \
                        --tag ${ECR_REPO}:${IMAGE_TAG} \
                        .
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    trivy image \
                        --severity HIGH,CRITICAL \
                        --exit-code 1 \
                        --format json \
                        --output trivy-report.json \
                        ${ECR_REPO}:${IMAGE_TAG}
                '''
            }

            post {
                always {
                    archiveArtifacts(
                        artifacts: 'trivy-report.json',
                        allowEmptyArchive: true
                    )
                }
            }
        }

        stage('Push to ECR') {
            when {
                expression {
                    return env.BRANCH_NAME == 'main'
                }
            }

            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-token']
                ]) {
                    script {
                        def accountId = sh(
                            script: '''
                                aws sts get-caller-identity \
                                    --query Account \
                                    --output text
                            ''',
                            returnStdout: true
                        ).trim()

                        def ecrUrl =
                            "${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

                        sh """
                            aws ecr get-login-password \
                                --region ${AWS_REGION} \
                            | docker login \
                                --username AWS \
                                --password-stdin ${ecrUrl}

                            docker tag \
                                ${ECR_REPO}:${IMAGE_TAG} \
                                ${ecrUrl}:${IMAGE_TAG}

                            docker push \
                                ${ecrUrl}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }
}
