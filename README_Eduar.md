# Income Tax Calculator

- Authors: Marceli Ciesielski, John Dela Cruz, Eduar Mancera. This project is the final assignment at the mthree academy.
- This document is a description of my understanding of the project as a whole an my personal contributions to it as well as my struggles.
  
# Contributions made by the members

- Marceli Ciesielski: HTML, CSS, Python App, JSON API, Selenium testing, Dockerfile, Grafana, Prometheus, Github. 
- John Dela Cruz: EC2 instance management, Kubernetes, Jenkins, Dockerhub, SQLLite, Grafana, Github. 
- Eduar Mancera: Project Management, Flowchart, Presentation, Shared ReadMe, Github, Testing.

<details>
  <summary>Introduction</summary>

  - The app itself is fairly strightforward, it only asks the user for their *first name*, *last name*, *income* and *expenses*. The user is getting calculated their taxes once they press the button *Calculate Tax*
  - Once the calculations are made, all the data is save in a SQLite database.
  - This app is being containerized using Docker. Clusterized using Jenkins to deploy it to a Kubernetes cluster and monitored in a dashboard created with Grafana and Prometheus
### The following picture is a representation of the flow the app follows.
![Screenshot_2024-09-03_at_12 38 13-removebg-preview](https://github.com/user-attachments/assets/25f5bc44-526e-4e1d-a2f7-0f0792574b64)

</details>

<details>
  <summary>SRE Principles</summary>

  1. *Embracing risks:* We decided to go for a cost effective approach due to we're paying for AWS.
  2. *Service Level Objectives (SLO):* We didn't meassure the SLO, we did try to optimize the budget features development.
  3. *Eliminate Toil:* This app's pipeline was completely automated. (Jenkins)
  4. *Monitoring distributed sytems:* Systems are being monitored with the help of Grafana and Prometheus.
  5. *Automation:* Automations were carry out with Jenkins. Also, the app is being monitored in real-time.
  6. *Release engineering:* We've used Git and Github to have version control, branching and tasks management.
  7. *Simplicity:* The app is fairly straightforward, besides we're paying for the AWS services, so we tried to keep it as simple as possible.
</details>

<details>
  <summary>Front-End</summary>

  The Front-End of the app is composed of 2 HTML files and 1 CSS file to provide the HTML files of some style. You can see  how the UI looks like in the following picture.
  <img width="430" alt="app ui" src="https://github.com/user-attachments/assets/016d688b-16c9-4850-975e-743c2de017b7">

</details>

<details>
  <summary>Back-End</summary>

  The Back-End of the app is composed of 4 python functions.
  - *inid_db():* This method is the one in charge of initialize the database and create the only table of our database. See code block.
  
  ```
    # Database initialization
    def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gross_income REAL NOT NULL,
            expenses REAL NOT NULL,
            net_income REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
  ```
  - *index():* This function is pretty simple, as its only function is to render the index.html file. see code block.

  - ```
      def index():
        return render_template('index.html')
    ```

    - *Calculate():* This function captures the user's input and checks them, then makes the taxes calculations to finally insert these into the database. See code block.
   
    - ```
      def calculate():
        try:
          first_name = escape(request.form["first_name"])
          last_name = escape(request.form["last_name"])
          gross_income = float(request.form['income'])
          expenses = float(request.form['expenses'])
          net_income = gross_income - expenses
  
          # Tax calculation logic
          if net_income <= 12750:
              tax = 0
          elif net_income <= 50270:
              tax = (net_income - 12750) * 0.2
          elif net_income <= 125140:
              tax = (50270 - 12750) * 0.2 + (net_income - 50270) * 0.4
          else:
              tax = (50270 - 12750) * 0.2 + (125140 - 50270) * 0.4 + (net_income - 125140) * 0.45
  
          net_income = net_income-tax
  
          # Save the data to the database
          conn = sqlite3.connect('database.db')
          cursor = conn.cursor()
          cursor.execute('''
              INSERT INTO users (first_name, last_name, gross_income, expenses, net_income)
              VALUES (?, ?, ?, ?, ?)
          ''', (first_name, last_name, gross_income, expenses, net_income))
          conn.commit()
          conn.close()
  
          return render_template('result.html', income=gross_income, expenses=expenses, tax=tax, first_name=first_name, last_name=last_name)
        except ValueError:
          return "Please enter a valid number for income."
      ```
      - *get_data():* This function gets the data from the database and shows it in JSON format. See code block.
      ```

      def get_data():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        conn.close()
    
        # Convert the rows to a list of dictionaries
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "gross_income": row[3],
                "expenses": row[4],
                "net_income": row[5]
            })
    
        return jsonify(data)
      ```
</details>

<details>
  <summary>Jenkins</summary>

  Our jenkins file is compose of 3 stages:
  1. Build Docker Image:On this stage we make sure we're at the right folder `python_scripts` to then create the docker image, named `my-docker-image` (see the code block)
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

2. Docker Push Image: On this stage, the docker image that just been created, is pushed to the Docker Hub. (see code block)
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

3. Kubernetes Deployment Stage: On this stage the docker image is deployed on a Kubernetes cluster with the help of course of the configuration files `deployment.yaml` and `service.yaml` (see code block)
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

  The app is deployed in a Kubernetes cluster, providing a namespace which is going to be used later on by Grafana and Prometheus dashboard. This is defined in the following configuration files.
  . deployment.yaml
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

  . service.yaml
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
  <summary>Grafana</summary>
  
  The app is being monitored in real-time through a Grafana dashboard, on this dashboard, we're watching the following indicators.
  - Instance temperature.
  - Network usage.
  - Number of times the network has dropped.
  - Information save in the database.
  - CPU usage.

The following picture is being taken of this dashboard.
  
  ![dashbboard](https://github.com/user-attachments/assets/d5c71fc4-9cd5-42a8-8696-464c68f98a06)
</details>

<details>
  <summary>Testing</summary>

  The testing was implemented with the help of selenium. This file contains 3 functions:
  - *setUp(self):* On this function the web browser driver is initialized
  - *test_functionality(self):* On this function the columns are found and filled up.
  - *setUp(self):* This is the function used to do the cleaning and close the browser opened during test.

  On the following code block, you can see the way testing has been implemented.
  ```

   def setUp(self):
        # Properly initialize ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://16.171.20.149:5000")  # Update with your actual Docker container port

    def test_functionality(self):
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

      def tearDown(self):
        self.driver.quit()
  ```
</details>

<details>
  <summary> Challenges </summary>
  
  Along with the development, we encounter numerous challenges:
  
  - EC2 instance limitation: Running AWS free instances didn't allow us to run multiple and heavy services like Kubernetes, Docker and Jenkins. So that we had to make a choicee
    1. To have differences instances to host these services.
    2. To pay for a more powerful instance to host all the services in the same instance.
      - After a team meeting, we decided to go with paid option, trying to optimize the time this instance was running.
  - Deploying Docker on minikube
    - On the process of deploying, we came to realization that minikube's configuration gets images from DockerHub, so Jenkins had to be configure to deploy images on DockerHub and not locally as we initially planned.
  - Grafana JSON format.
    - Due to Grafana's format wasn't matching wiht our JSON API's format, we had to manually transform the data to make it accesible on the dashboard.
  - GitHub limitation with large files.
    - Due to our Kubernetes setup had large files needed to run our app and these files could not be upload to GitHub, we had to leave the configuration to the user. We provide the service and deployment files though.
  - AWS EC2 Security groups.
    - By default and for security reasons, AWS instances don't have enabled many of the ports we needed to use, so we had to enable the traffic for those ourselves.
</details>

