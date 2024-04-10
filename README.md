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
    image: azsx26735546/senao-backend
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
  
  flyway:
    build: ./flyway-migration 
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

### API document 
> please run the docker-compose first 

1. [localhost:5000/docs](localhost:5000/docs)
2. [api_document.pdf](./api_document.pdf)