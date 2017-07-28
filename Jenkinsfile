pipeline {
    agent any
    stages {
        stage("Build docker") {
            steps {
                sh 'scripts/ci/build_docker.sh'
            }
        }
        stage("Run test") {
            steps {
                sh 'scripts/ci/test.sh'
            }
        }
        stage("push") {
            steps {
                sh 'scripts/ci/push.sh'
            }
        }
    }
}
