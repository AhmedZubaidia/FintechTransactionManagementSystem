# Fintech Transaction Management System

## Project Overview

This project aims to develop a web-based transaction management system that allows users to manage their finances, including tracking expenses, incomes, and transactions. The system will send notifications via Telegram, have a documented API tested with Postman, and be containerized using Docker.

## Objective

- Develop a web-based transaction management system.
- Track expenses, incomes, and transactions.
- Send notifications via Telegram.
- Document API and test with Postman.
- Containerize the application using Docker.

## Milestones

### Milestone 1: Project Setup and Initial Features (1 month)

1. **Project Initialization**
   - Set up project repository on GitHub.
   - Set up Flask project structure with a virtual environment.
2. **Database Setup**
   - Configure MySQL database and SQLAlchemy.
   - Define database models for users and transactions.
3. **Basic API Endpoints**
   - Create user registration and login endpoints.
   - Create CRUD operations for transactions.
4. **Docker Setup**
   - Dockerize the Flask application.
5. **CI/CD with GitHub Actions**
   - Set up GitHub Actions for continuous integration.
6. **Telegram Integration**
   - Set up Telegram bot and send push messages.

### Milestone 2: Core Functionalities (1 month)

1. **User Management**
   - Implement user authentication and authorization using Flask-JWT-Extended.
2. **Transaction Management**
   - Implement transaction categorization and reporting.
   - Implement income and expense tracking.
3. **Validation and Serialization**
   - Use Marshmallow for input validation and serialization.
4. **Advanced API Documentation**
   - Document APIs using Postman.
5. **Testing**
   - Write unit tests for all endpoints with at least 80% coverage.

### Milestone 3: Advanced Features and Deployment (1 month)

1. **Notification System**
   - Enhance Telegram notifications for transactions.
2. **Deployment**
   - Set up Docker Hub repository and automate image build.
   - Deploy application to a cloud service (e.g., AWS, Heroku).
3. **Performance Optimization**
   - Optimize database queries and API performance.
4. **Final Testing and QA**
   - Conduct final round of testing and bug fixes.

## Tech Stack

- Flask
- MySQL
- SQLAlchemy
- Docker
- GitHub Actions
- Telegram Bot
- Postman

## Setup Instructions

1. Clone the repository:
    ```sh
    ```
2. Navigate to the project directory:
    ```sh
    ```
3. Create and activate a virtual environment:
    ```sh

    ```
4. Install the dependencies:
    ```sh
    ```
5. Set up the MySQL database and configure environment variables.
6. Initialize the database:
    ```sh

    ```
7. Run the application:
    ```sh
    ```

## Usage Instructions

- Register and log in to manage your transactions.
- Use the provided endpoints to track expenses, incomes, and transactions.
- Receive notifications via Telegram for transaction updates.

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m "Description of changes"
    ```
4. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
5. Create a pull request.

## API Documentation

The API documentation can be found in the Postman collection included in the repository.

## Definitions of Done

- **Code Quality:** All code must be linted and pass style checks.
- **Testing:** All functionalities must have unit tests with at least 80% coverage.
- **Documentation:** Every feature and endpoint must be documented.
- **CI/CD:** All changes must pass through CI/CD pipelines without errors.
