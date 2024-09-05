# mthree Final Project

This is the final project for the mthree program, developed by ledmarceli. The project is a web application built with Flask that calculates and stores users' net income and taxes based on their gross income and expenses.

<details>
  <summary>Architecture</summary>

  ### The project's architecture is broken down into the following components
  - Python App/Database.
  - Github.
  - Jenkins.
  - Kubernetes.
  - Kubernetes Cluster
    - Grafana.
    - Live Production Python App/Database
   
   ### On the following picture, you'll see a flowchart describing the way the components communicate.
  ![Screenshot_2024-09-03_at_12 38 13-removebg-preview](https://github.com/user-attachments/assets/4d7dfa7f-e07c-4a72-8757-564a9b94b746)
</details>

<details>
  <summary>Python APP</summary>

  ### The Python App performs tax calculations based on the income and expenses. This app contains the following components
  - *Tax Calculations:* As we mentioned before, these tax calculations are made based on the user's income and expenses.
  - *Database creation/Actualization:* The app also performs database creation and actualization (through inserting the new records in it)
  - *Security Meassures:* The app also includes some security meassures such as escaping markup language and check the user's input so that, attacks like XSS are avoided.
  - *HTML & CSS:* The app's UI is composed of 2 HTML file and 1 CSS file to add some style to the HTML file.
  - *Testing:* The app also includes Front-end testing, this task was carried out with Selenium.
  ### The following picture is an illustration of the app's UI.
  <img width="430" alt="app UI" src="https://github.com/user-attachments/assets/d5fdfd56-9ea0-463e-aa48-93d3cc32f240">

</details>

<details>
  <summary>Database</summary>

  ### The DBMS used for this app is SQLite, as the app is pretty small, we didn't require much out of the database.
  - The database is one single table named *users* to store their inputs. In the following picture, you'll see a better description of this table.
  <img width="799" alt="Database's table" src="https://github.com/user-attachments/assets/67932890-c506-4f90-9c9e-10ca504c88b8">
  
</details>
<details>
  <summary>Docker</summary>
  
  ### You can see our docker file (and int's requirements) in the next two code blocks.

  - Dockerfile
  ```
    # Use an official Python runtime as a parent image
    FROM python:3.9-slim
    
    # Install SQLite3
    RUN apt-get update && apt-get install -y sqlite3
    
    # Set the working directory in the container
    WORKDIR /app
    
    # Copy the current directory contents into the container at /app
    COPY . /app
    
    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Expose port 5000 for the Flask app
    EXPOSE 5000
    
    # Define environment variable
    ENV FLASK_APP=app.py
    
    # Run the application
    CMD ["python", "app.py"]
  ```

  - Requirements
  
  ```
  Flask==2.3.2
  MarkupSafe==2.1.3
  Werkzeug>=2.1.0
  ```
</details>

<details>
  <summary>Jenkins</summary>

  ### Our Jenkins file has 3 stages:
  1. *Build Docker Image:* On this stage we make sure we're at the right folder `python_scripts` to then create the docker image, named `my-docker-image` (see the code block)
  
  ```
  // Docker build stage
  stage('Build Docker Image') {
      steps {
          script {
              sh '''
              echo "Building Docker image..."
              pwd
              cd /
              pwd
              cd home/ubuntu/python_scripts
              pwd
              docker build -t my-docker-image .
              '''
          }
      }
  }
  ```

  2. *Docker Push Image:* On this stage, the docker image that just been created, is pushed to the Docker Hub. (see code block)
  
  ```
  // Docker push stage
  stage('Push Docker Image') {
      steps {
          script {
              sh '''
              echo "Pushing Docker image to Docker Hub..."
              docker tag my-docker-image kenneth1521412/my-docker-image
              docker push kenneth1521412/my-docker-image:latest
              '''
          }
      }
  }
  ```

3. *Kubernetes Deployment Stage:* On this stage the docker image is deployed on a Kubernetes cluster with the help of course of the configuration files `deployment.yaml` and `service.yaml` (see code block)

```
// Kubernetes deployment stages
stage('Starting Minikube') {
    steps {
        script {
            sh '''
            echo "Starting Minikube..."
            minikube delete || true
            minikube start
            minikube status
            
            echo "Deploying to Kubernetes..."
            cd /
            pwd
            cd home/ubuntu/minikube
            pwd
            kubectl apply -f deployment.yaml
            kubectl apply -f service.yaml
            kubectl get pods
            kubectl get services
            '''
        }
    }
}
```

</details>

<details>
  <summary>Kubernetes</summary>
  
</details>
<details>
  <summary>Grafana & Prometheus</summary>
</details>
<details>
  <summary>Testing</summary>
</details>
