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
        bat 'pip install -r requirements.txt'
      }
    }

    stage('Run Extract Values Script') {
      steps {
        script {
          bat "python get_data_from_pdf.py"
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
    PYTHON_PATH = 'C:\Users\Hp\AppData\Local\Programs\Python\Python311' // Update this to your Python path
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
