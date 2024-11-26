pipeline {
  agent any
  stages {
    stage('Checkout Code') {
      steps {
        git(branch: 'main', url: 'https://github.com/curiousthinker85/jenkins-')
      }
    }

    stage('Install Dependencies') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Run Extract Values Script') {
      steps {
        script {
          sh "${PYTHON_PATH} get_data_from_pdf.py"
        }

      }
    }

    stage('Archive Output') {
      steps {
        archiveArtifacts(artifacts: '**/*.csv, **/*.txt, **/*.png', allowEmptyArchive: true)
      }
    }

  }
  environment {
    PYTHON_PATH = '/usr/bin/python3'
  }
  post {
    always {
      echo 'Pipeline Completed'
    }

    success {
      echo 'All tasks completed successfully!'
    }

    failure {
      echo 'Pipeline failed. Check logs for details.'
    }

  }
}