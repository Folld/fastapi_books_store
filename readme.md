Async fastapi + postgres proj.

first run server: 
- docker-compose build
- docker-compose up postgres
- cd src
- alembic upgrade head
- docker-compose up server

second and next run:
- docker-compose up