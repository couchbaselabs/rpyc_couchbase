pipeline {
    agent any

    stages {
        stage('Code Styling') {
            steps {
                sh 'python2 -m flake8 rpyc_couchbase/ --config=.flake8 --show-source --statistics --count'
            }
        }
    }
}
