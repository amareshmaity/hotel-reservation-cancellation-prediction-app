
# 1. Setup Jenkins container



## Step 1 — Install Docker Desktop

Docker is required because both Jenkins and the ML application will use containers.

### 1.1 Install Docker Desktop

Download and install Docker Desktop from the official Docker website:

[Docker Desktop](https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com)

### 1.2 Start Docker

After installation:

1. Open Docker Desktop.
2. Wait until Docker is running.
3. Verify Docker from the terminal.

```bash
docker --version
```

You can also check:

```bash
docker info
```

If Docker is working correctly, the Docker engine should be accessible.

<br/>

## Step 2 — Create the Jenkins Environment

The next task is to run Jenkins inside a Docker container.

### 2.1 Create a Jenkins Directory

Create a folder for the custom Jenkins image:

```text
custom_jenkins/
```

Example:

```text
your-working-directory/
└── custom_jenkins/
```

<br/>

### 2.2 Create the Jenkins Dockerfile

Inside `custom_jenkins/`, create:

```text
Dockerfile
```

The purpose of this Dockerfile is to create a customized Jenkins image containing Docker-related tooling.

```dockerfile
FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian trixie stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

RUN groupadd -f docker && \
    usermod -aG docker jenkins

RUN mkdir -p /var/lib/docker

VOLUME /var/lib/docker

USER jenkins
```

### What this Dockerfile does

| Instruction       | Purpose                                |
| ----------------- | -------------------------------------- |
| `FROM`            | Uses Jenkins LTS as the base image     |
| `USER root`       | Allows installation of system packages |
| `apt-get install` | Installs required tools                |
| Docker repository | Adds Docker package source             |
| `docker-ce`       | Installs Docker Engine                 |
| `usermod`         | Adds Jenkins to Docker group           |
| `/var/lib/docker` | Docker data directory                  |
| `VOLUME`          | Defines persistent Docker storage      |
| `USER jenkins`    | Returns to Jenkins user                |

<br/>

## Step 3 — Build the Jenkins Docker Image

Open a terminal in the `custom_jenkins` directory.

```bash
cd custom_jenkins
```

Build the image:

```bash
docker build -t jenkins-dind .
```

### Meaning

```text
docker build
    ↓
Read Dockerfile
    ↓
Install Jenkins + Docker
    ↓
Create image
    ↓
jenkins-dind
```

<br/>

### 3.1 Verify the Image

Run:

```bash
docker images
```

You should see an image similar to:

```text
REPOSITORY      TAG       IMAGE ID
jenkins-dind    latest    xxxxxxxxx
```

<br/>

## Step 4 — Run the Jenkins Container

Start Jenkins using:

```bash
docker run -d --name jenkins-dind ^
  --privileged ^
  -p 8081:8080 ^
  -p 50000:50000 ^
  -v //var/run/docker.sock:/var/run/docker.sock ^
  -v jenkins_home:/var/jenkins_home ^
  jenkins-dind
```

### Important options

| Option             | Purpose                                   |
| ------------------ | ----------------------------------------- |
| `-d`               | Runs container in background              |
| `--name`           | Gives the container a name                |
| `--privileged`     | Gives the container elevated privileges   |
| `-p 8081:8080`     | Makes Jenkins web UI available            |
| `-p 50000:50000`   | Jenkins agent communication port          |
| `-v` Docker socket | Allows Jenkins to communicate with Docker |
| `-v jenkins_home`  | Persists Jenkins configuration/data       |

<br/>

## Step 5 — Verify Jenkins Container

### 5.1 Check Running Containers

```bash
docker ps
```

You should see:

```text
jenkins-dind
```

with port mappings including:

```text
8081 → 8080
50000 → 50000
```

<br/>

### 5.2 Check Jenkins Logs

Run:

```bash
docker logs jenkins-dind
```

During the first startup, Jenkins generates an **initial administrator password**.

Copy that password.

It will be required during the initial Jenkins setup.

<br/>

## Step 6 — Open Jenkins

Open your browser and navigate to:

[Jenkins — localhost:8081](http://localhost:8081)

You should see the Jenkins setup page.

### Initial setup

1. Enter the initial administrator password.
2. Continue with Jenkins setup.
3. Select **Install Suggested Plugins**.
4. Wait for the plugins to install.
5. Create your Jenkins administrator account.
6. Complete the setup.

After this, you should reach the Jenkins dashboard.

<br/>

## Step 7 — Install Python Inside Jenkins

The Jenkins container needs Python because the CI/CD pipeline will execute Python-related tasks.

### 7.1 Enter the Jenkins Container as Root
Go to terminal in the vscode and 
Run:

```bash
docker exec -u root -it jenkins-dind bash
```

You are now inside the Jenkins container (here you will write commands inside bash)



### 7.2 Install Python

Update the package list:

```bash
apt update -y
```

Install Python:

```bash
apt install -y python3
```

Check the version:

```bash
python3 --version
```



### 7.3 Create the `python` Command

The setup creates a `python` command pointing to Python 3:

```bash
ln -s /usr/bin/python3 /usr/bin/python
```

Verify:

```bash
python --version
```



### 7.4 Install pip

```bash
apt install -y python3-pip
```



### 7.5 Install Python Virtual Environment Support

```bash
apt install -y python3-venv
```

This allows Jenkins to create isolated Python environments.



### 7.6 Exit the Container

```bash
exit
```



### 7.7 Restart Jenkins

```bash
docker restart jenkins-dind
```

Then return to the Jenkins dashboard and sign in again.

Now your Jenkin setup is ready. Its time to **integrate github**.








