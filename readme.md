# Books Store

Books Store is a training project built using Async FastAPI and PostgreSQL. It provides a simple API for managing a collection of books.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Books Store is a web application that allows users to perform CRUD (Create, Read, Update, Delete) operations on a collection of books. It utilizes the FastAPI framework, which is built on top of Starlette and Pydantic, and communicates with a PostgreSQL database for data persistence.

## Features

- Create a new book record with details such as title, author, genre, and publication date.
- Retrieve a list of all books in the store.
- Get details of a specific book by providing its ID.
- Update the details of an existing book.
- Delete a book record from the store.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/Folld/books_store.git
   ```

2. Install the required dependencies:

   ```shell
   pip install poetry && poetry install
   ```

3. Create .env file in src folder and configure the database connection settings in the file. Example: 
   ```env
   APP_HOST=0.0.0.0
   APP_PORT=8000
   POSTGRES_PASSWORD=postgres
   POSTGRES_PORT=5432
   POSTGRES_HOST=127.0.0.1
   ```

4. Run the database migrations to create the necessary tables:

   ```shell
   alembic upgrade head
   ```

5. Start the FastAPI server:

   ```shell
   uvicorn app.main:app --reload
   ```

   The API will be accessible at `http://localhost:8000`.

## Usage

1. Use the API endpoints described in the [API Endpoints](#api-endpoints) section to interact with the Books Store.

2. You can test the API using tools like cURL or an API testing tool such as Postman or Insomnia.

## API Endpoints

For detailed information about request and response formats, refer to the API documentation available at `http://localhost:8000/docs`.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
```

Feel free to modify the content as needed and add any additional sections or information specific to your project. Once you've made the necessary changes, save the file as `README.md` in the root directory of your GitHub project.

Let me know if there's anything else I can assist you with!

first run server: 
- docker-compose build
- docker-compose up postgres
- cd src
- alembic upgrade head
- docker-compose up server

second and next run:
- docker-compose up
