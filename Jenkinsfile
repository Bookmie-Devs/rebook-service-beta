pipeline {
    agent any
    stages{
        
        stage ('Cloning and Building') {
            steps {
            echo "Building"
            git url: "https://github.com/LhilEthen/Rebook.git", branch: "main"
            }
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