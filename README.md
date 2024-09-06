# mthree Final Project

This is the final project for the mthree program, developed by @ledmarceli, @mubamba1, @eduarecnam. The project is a web application built with Flask that calculates and stores users' net income and taxes based on their gross income and expenses. The individual ReadMe files are available in this repository under README_Marceli or under the link: https://github.com/mobamba1/mthree_final_project/tree/main



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

  ### The app is deployed in a Kubernetes cluster to provide CI/CD and a namespace that's going to be used by Grafana on the next step. To see the configuration file, have a look to the next two code blocks.
  - Deployment.yaml

  ```
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: flask-app
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: flask-app
      template:
        metadata:
          labels:
            app: flask-app
        spec:
          containers:
          - name: flask-container
            image: kenneth1521412/my-docker-image
            ports:
            - containerPort: 5000
  ```
  - Service.yaml

  ```
    apiVersion: v1
    kind: Service
    metadata:
      name: app-service
    spec:
      type: NodePort
      selector:
        app: flask-app
      ports:
        - protocol: TCP
          port: 80
          targetPort: 5000
          nodePort: 30236  # You can specify this port or allow Kubernetes to choose one in the 30000-32767 range
  ```
  
</details>

<details>
  <summary>Grafana & Prometheus</summary>

  ### In order to monitor the cluster, we've developed a dashboard with the help of Grafana & Prometheus to check the cluster's health. We're specially watching:
  - Instance temperature.
  - Network usage.
  - Number of times the network has dropped.
  - Information save in the database.
  - CPU usage.
  
  ### In the following picture, you can have a look of this dashboard.
  ![dashbboard](https://github.com/user-attachments/assets/f87996a0-a474-440e-98ea-0e5db82284d9)
</details>

<details>
  <summary>Testing</summary>

  ### We've also implemented front-end testing with the help of Selenium. This file contains 3 functions:
  1. Set up: On this function the browser's driver is intialized. See code block.

  ```
    service = Service(ChromeDriverManager().install())
    self.driver = webdriver.Chrome(service=service)
    self.driver.get("http://16.171.20.149:5000")  # Update with your actual Docker container port
  ```

2. Test: On this function is where the fields are filled up and submit. See code block.

```
  driver = self.driver
  #Wait a moment for the page to load
  time.sleep(2)
  
  # Find fields
  first_name_field = driver.find_element("name", "first_name")
  last_name_field = driver.find_element("name", "last_name")
  income_field = driver.find_element("name", "income")
  expenses_field = driver.find_element("name", "expenses")
  submit_button = driver.find_element(By.XPATH, "//button[text()='Calculate Tax']")
  
  # Fill fields and submit
  first_name_field.send_keys("Marceli")
  last_name_field.send_keys("Ciesielski")
  income_field.send_keys("27000")
  expenses_field.send_keys("2000")
  submit_button.click()
  
  # Wait a moment for the page to load
  time.sleep(1)
  
  # Check if the output is fine
  self.assertIn("Tax Calculation Result", driver.page_source)
```
3. Tear down: On this function everything is cleaned up after the test is completed, closing the browser opened during the test. See code block.

```
  self.driver.quit()
```
</details>

<details>
  <summary>SRE Principles</summary>

  1. *Embracing risk:* For this project we accepeted that 100% reliaiblity isn't possible nor cost effective, that's why we decided to give priority to cost (given that we're paying for it) over availability (obviously in a real production set up we'd balance them up).
  2. *Service Level Objectives:* Our services level objectives were not meassure it, but as we mentioned before, we were only trying to optimize budget and features development as much as possible.
  3. *Eliminate toil:* Our app pipeline is being completely automated and documented. From its execution to its deployment and monitoring.
  4. *Monitoring distributed systems:* We're watching the performance of the app through a dashboard built with the help of *Grafana* and *Prometheus*
  5. *Automation:* As we mentioned before, the complete pipeline is being automated, from its execution to its deployment and monitoring. 
  6. *Release engineering:* This app is being built, packaged, tested and deployed in a reliable, efficient, and repeatable manner, using technologies/tools like *Git/GitHub, Docker, Jenkins, Kubernetes, Grafana and Prometheus*.
  7. *Simplicity:* To the development and deployment of this app we've optimized the architecture, pipeline automation and monitoring so there is no redundancies or waste of any resources.
</details>

<details>
  <summary>Agile</summary>

  ### For the development of this project we followed an agile methodology:
  - *Iterative development:* Every component was developed iteratively, focusing on having new features at the end of every sprint, so we all could provide some feedback at the end of it.
  - *Responding to changes:* Throughout the whole proecess the team had to react to changes, for instance the initial app was different, testing wsn't a requirement, but we implemented anyways, kubernetes were implemented even though they were not a requirement as well, we had to use several instances instead of only 1.
  - *Individual and Interaction:* Communication and collaboration was really good, everybody helped each other during every sprint. Also, at the beginning and end of the day, we had a short stand-up to either plan the next sprint or sum up the day.
  - Github Project: We also used github project to get the benefits of using a kanban boards, such as tasks creation, assignation, having a visual view of the state of the project. The final state of the kanban board can be seen in the following picture.
 <img width="1680" alt="Kanban board" src="https://github.com/user-attachments/assets/2415d576-2c68-462c-ae27-ce49ddf0872a">
</details>  

