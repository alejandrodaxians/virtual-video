# Virtual-video API

Virtual-video is a Videoclub API that allows you to create and manage your own video library. It stores films in an SQL database, and includes a rental system.

<br>
<hr>
<br>

## Prerequisites
<br>

- Pull the MySQL image from Docker HUB:

```bash
docker pull mysql
```

- Run the container based on the image to connect to the database:

```bash
docker run --name mysql-container -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysql24601 -e MYSQL_DATABASE=filmsdb -d mysql
```

<br>
<hr>
<br>

## Usage:
<br>

- Go to the project root folder

- Build the image:

```bash
docker build -t virtual-video-api .
```

- Run a container based on that image:
    
```bash
docker run -d --name virtual-video-container -p 80:80 virtual-video-api
```

- Access the API at the following address (it will redirect you to the documentation):

http://127.0.0.1:8000/

<br>
<hr>
<br>

## Features:

<br>

### - Create a new film
### - Update a film
### - Delete a film
### - Check the full list of films
<br>

### - Check if a film is available
### - Rent a film
### - Return a film
