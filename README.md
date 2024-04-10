## Senao Assessment 

Design and implement two RESTful HTTP APIs for creating and verifying an account
and password.

> Notes: 為了方便demo，.env file直接push上github, Laptop: Macbook M1  

### docker-compose.yml
* **postgres:** database 
* **flyway:** database migration tool
* **fastapi:** our restful api 
* **redis:** memory db, it's used prevent too many failure of call /verify API.

```yml
version: '3.3'

networks:
  backend: 

services:
  fastapi: 
    image: azsx26735546/senao-backend:latest
    ports:
      - "5000:5000"
    networks:
      - backend
    depends_on:
      - postgres
      - redis 
    environment:
      - POSTGRES_URL=${POSTGRES_URL}
    
  postgres:
    image: postgres:latest
    expose:
      - "5432"
    networks:
      - backend
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres-data:/var/lib/postgresql/data 
  
  flyway:
    image: azsx26735546/senao-assessment_flyway:latest
    depends_on:
      - postgres
    networks:
      - backend
    environment:
      - FLYWAY_URL=${FLYWAY_URL}
      - FLYWAY_USER=${POSTGRES_USER}
      - FLYWAY_PASSWORD=${POSTGRES_PASSWORD}

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    networks:
      - backend
volumes:
  postgres-data:
```

### Requirements 
* Docker
* Docker Compose 

### How to run this project
```shell
# start 
docker-compose up 

# remove data 
docker-compose rm 
```

### APIs
1. POST /user: for creating account
2. POST /verify: for verifing account and password

### API document 
> please run the docker-compose first 

1. [localhost:5000/docs](localhost:5000/docs)
fastapi提供一個可互動的swagger api document (可以用這個測試)

1. [api_document.pdf](./api_document.pdf)