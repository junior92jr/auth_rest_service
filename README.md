# Authentication with JWT tokens and FastAPI

The project is to design and implement a Restfull API that provides user authentication and header verification in order to have protected endpoints.

## API Endpoints

This API implements the following endpoints:

`POST` : `/auth/recover-password` It will set/reset credentials for non authenticated users. It will request for a valid `recovery_code`. In this first prototype we have a fixed value for that. You can find it in `.env_example` as `FIXED_RECOVERY_CODE`. Ideally this code is generated from the backend as well and linked to a User with an expirantion time. This endpoint works for set up a User for the first time or for recover lost credentials.

`POST` : `/auth/login` It will need a username and password. It returns a valid access token.

`POST` : `/auth/reset-password` When authenticated, you can edit your password.

`GET` : `/customers/me` When authenticated you can retrieve your own profile informatio.

`PUT` : `/customers/me/edit-data` Whene authenticatee you can edit your customer information.


## API Examples

Recovering access to your account. Consider that for simplicity `recovery_code` is a fixed value already profived in this project.

```bash
curl --location 'http://localhost:8002/auth/recover-password' \
--header 'client-version: 3.1.2' \
--header 'Content-Type: application/json' \
--data-raw '{
    "recovery_code": 1631959404,
    "email": "ucgjtbduswiejja@icloud.com",
    "password": "newpassword123"
}'
```

a success response would be something like:

```bash
{
  "message": "New Credentials Created for ucgjtbduswiejja@icloud.com."
}
```

For creating an authentication token
```bash
curl --location 'http://localhost:8002/auth/login' \
--header 'client-version: 3.1.2' \
--form 'username="ucgjtbduswiejja@icloud.com"' \
--form 'password="newpassword123"'
```

In the response we can get the access token to be used in the other endpoins.
```bash
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1Y2dqdGJkdXN3aWVqamFAaWNsb3VkLmNvbSIsImV4cCI6MTcwOTE5MzUxOX0.N_CkArOmADj8CvGf_Bq6hS-Z038KhEQ3lc-iolrEj6M",
    "token_type": "bearer"
}
```

To Change your password

```bash
curl --location 'http://localhost:8002/auth/reset-password' \
--header 'client-version: 3.1.2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1Y2dqdGJkdXN3aWVqamFAaWNsb3VkLmNvbSIsImV4cCI6MTcwOTE5Mzg3OX0.vgYgyTT3JBLyOLq9vickwhVs6MDceFyR03-CwPVI4pc' \
--data '{
    "old_password": "newpassword123",
    "new_password": "newpassword321"
}'
```

To check your customer information
```bash
curl --location 'http://localhost:8002/customers/me' \
--header 'client-version: 3.1.2' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1Y2dqdGJkdXN3aWVqamFAaWNsb3VkLmNvbSIsImV4cCI6MTcwOTE5Mzg3OX0.vgYgyTT3JBLyOLq9vickwhVs6MDceFyR03-CwPVI4pc'
```

response would be something like

```bash
{
    "customer_id": "5a8fc94c-9d44-4a08-a5eb-3f496e314613",
    "email": "ucgjtbduswiejja@icloud.com",
    "country": "US",
    "language": "en"
}
```

To edit the language 

```bash
curl --location --request PUT 'http://localhost:8002/customers/me/edit-data' \
--header 'client-version: 3.1.2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1Y2dqdGJkdXN3aWVqamFAaWNsb3VkLmNvbSIsImV4cCI6MTcwOTE5Mzg3OX0.vgYgyTT3JBLyOLq9vickwhVs6MDceFyR03-CwPVI4pc' \
--data '{
    "language": "de"
}'
```

response would be something like

```bash
{
    "customer_id": "5a8fc94c-9d44-4a08-a5eb-3f496e314613",
    "email": "ucgjtbduswiejja@icloud.com",
    "country": "US",
    "language": "de"
}
```


## Clone the repository

To clone the repository by SHH

```bash
$ git clone git@github.com:junior92jr/auth_rest_service.git
```

To clone the repository by HTTPS

```bash
$ git clone https://github.com/junior92jr/auth_rest_service.git
```

## Build the API image

To build, test and run this API we'll be using `docker-compose`. As such, the first step
is to build the images defined in the `docker-compose.yml` file.

```bash
$ cd auth_rest_service/
```

```bash
$ docker-compose build
```

This will build two images:

- `fastapi-tdd-docker_web` image with REST API.
- `fastapi-tdd-docker_web-db` image with Postgres database.

## Create Enviroment Variables

You will find a file called `.env_example`, rename it for `.env`


## Run the Containers
 
To run the containers previously built, execute the following:
 
```bash
$ docker-compose up -d
```

This will launch two services named `web` (the API) and `web-db` (the underlying 
database) in background. The `web` service will be running on port `8002` on localhost. 
Whereas the database will be exposed to the `web` service. To make sure the
app is running correctly open [http://localhost:8002](http://localhost:8002) in 
your web browser (and/or run `docker-compose logs -f` from the command line).

For using the swagger interface with example payloads open
in your web browser [http://localhost:8002/docs](http://localhost:8002/docs) 


## Create the Database

The database will be created by running the `create_db.sql` file that will be 
executed when the container is built:

```bash
$ docker-compose up -d --build
```

One can confirm that the database was properly created by accessing the database container
and starting a psql console.

```bash
$ docker-compose exec web-db psql -U postgres
```

Next, one can connect to the `web_dev` database and list all the tables:

```bash
# \c web_dev
# \dt
```

## Run the Tests

The tests can be executed with:

```bash
$ docker-compose exec web pytest
```

Or including a coverage check:

```bash
$ docker-compose exec web pytest --cov="."
```
