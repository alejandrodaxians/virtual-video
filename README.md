# Virtual-video API

Virtual-video is a Videoclub API that allows you to create and manage your own video library. It stores films in an SQL database, and includes a rental system.

<hr>
<br>

## Usage:

Use the uvicorn server to interact with the API:

```bash

uvicorn main:app --reload

```

Then, access the API at the following address:

http://127.0.0.1:8000/docs

<hr>
<br>

## Features:

### - Create a new film
### - Update a film
### - Delete a film
### - Check if a film is available
### - Check the full list of films
### - Rent a film
### - Return a film