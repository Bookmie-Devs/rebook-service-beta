pipeline {
    agent any
    stages{
        
        stage ('Cloning and Building') {
            steps {
            echo "Building"
            // sh ". /var/.venv/bin/activate"
            // git url: "https://github.com/LhilEthen/Rebook.git", branch: "main"
            }
        }
        
        // stage ('Collect StaticFiles') {
        //     steps {
        //     echo "Collecting static files"
        //     // sh "python manage.py collectstatic"
        //     }
        // }

        stage ('Testing') {
            steps {
            echo "Testing"
            sh "python3 manage.py test"
            }
        }   
        
        stage ('Deploying') {
            steps {
            echo "Deploying"
            }
        }
    }
}