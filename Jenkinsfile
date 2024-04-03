pipeline {
    agent any
    stages{
        
        stage ('Cloning and Building') {
            steps {
            echo "Building"
            }
        }
        
        stage ('Collect StaticFiles') {
            echo "Collecting static files"
            sh "python manage.py collectstatic"
        }

        stage ('Test') {
            steps {
            echo "Testing"
            sh "python manage.py test"
            }
        }
        
        stage ('Deploy') {
            steps {
            echo "Deploying"
            }
        }
    }
}