Prerequisites
Before running the application, make sure you have the following prerequisites installed:

Python 3.7+ (3.10+ recommended).
PostgreSQL.
Docker 
Docker compose
Installation
Clone the repository:

git clone https://github.com/kcalifdimy/Backend_Developer_Assessment.git
cd Backend_Developer_Assessment
Create a virtual environment (recommended):

on the root directory run:
Command:
To run build the app
docker compose build

To start the app
docker compose up

for database migration
docker compose run fastapi alembic revision --autogenerate
docker compose run fastapi alembic upgrade head






python3 main.py
API Endpoints
The API exposes the following endpoints:

POST /user/: Register a new user.
POST /login/: Authenticate and receive a JWT token.
GET /user/{user_id}/: Retrieve user info (protected endpoint).
GET /task/: Retrieve a list of tasks (protected endpoint).
POST /task/tasks/: Create a new task (protected endpoint).
GET /task/{task_id}: Retrieve a specific task (protected endpoint).
PUT /task/tasks/{task_id}: Update a specific task (protected endpoint).
DELETE /task/{task_id}: Delete a specific task (protected endpoint).
For real-time updates on task status changes, use WebSocket connections to /ws/tasks/{client_id}.

Testing the API with Swagger UI
Fast API comes with Swagger UI. This tool is automatically generated based on your API's route definitions and Pydantic models.

Accessing Swagger UI
Once the API is running, Swagger UI can be accessed on the following URL:

http://localhost:8000/docs
You can use swagger UI to:

Browse Endpoints
Send Requests
View Responses
Test Validations
To Test with SwaggerUI, you can do the following for each endpoint explained above

Open your web browser and navigate to the /docs path as mentioned above.

Explore the available endpoints and select the one you want to test.

Click on the "Try it out" button to open an interactive form where you can input data.

Fill in the required parameters and request body (if applicable) according to the API documentation given above.

Click the "Execute" button to send the request to the API.

The response will be displayed below, showing the status code and response data.

You can also view example request and response payloads, which can be helpful for understanding the expected data format.

Testing the API with pytest Framework
A suite of tests using the pytest framework was used to help verify the functionality of the Task Manager FastAPI.

Running the tests
Navigate to the task_manager_fastapi (root) directory using a terminal:
cd <your_path_to_project>/task_manager_fastapi
Run the tests by executing the following command (don't forget to activate your virtual environment if used):
pytest
This command will automatically discover and run the test cases defined in the tests directory.

Potential Improvements
Enhance My Task Manager FastAPI project with the following potential improvements:

Create unit test:
Becauseof time I was unable to create tests for the project

Asynchronous Database Operations and Route Handlers:

Utilize asynchronous database drivers like asyncpg for faster database access.
Rewrite route handlers as asynchronous to fully leverage FastAPI's asynchronous capabilities for better performance.
Task Prioritization and Deadlines:

Allow users to set task priorities (e.g., high, medium, low).
Implement deadlines and reminders for tasks, potentially using BackgroundTasks or Celery.
Create sorting mechanisms for tasks based on priority and deadlines.
User Profile Management and User-Specific Tasks:

Develop user profile management to enable users to update their information.
Associate tasks with specific users, allowing each user to see only their tasks.

Task Assignment to Users or Groups:

Enable task assignments to individual users or groups.
Implement notifications for task assignments.
Allow users to delegate tasks to others.
User Roles and Role-Based Access Control (RBAC):

Introduce user roles (e.g., admin, manager, user) to control access.
Implement Role-Based Access Control (RBAC) for fine-grained access control.
Test Expansion and Integration Tests:

Expand unit tests to cover edge cases and scenarios.
Develop integration tests to validate interactions between components.
Create a test database for isolated and secure testing.
Advanced Logging and Error Handling:

Enhance logging by categorizing log messages (info, warnings, errors).
Implement structured logging for better analysis.
Improve error handling for user-friendly error messages.
Database Layer Separation or Design Patterns:

Consider separating database operations into a dedicated layer or applying a design pattern like the repository pattern.
Modularize components into separate services for a microservices approach.
Security Enhancement with Cookies and Refresh Tokens:

Implement secure cookies for browser-based sessions.
Generate and validate refresh tokens for enhanced security.
Implement token expiration and renewal mechanisms.
Scalability and Performance Optimization:

Optimize database queries and indexes for improved performance.
Introduce caching mechanisms (e.g., Redis) for frequently accessed data.
Explore containerization and orchestration for scalable deployment.
User-Friendly Documentation:

Improve API documentation using tools like Swagger UI or ReDoc.
Provide detailed explanations and examples for API endpoints.
Internationalization and Localization:

Enable multi-language support for the application.
Allow users to select their preferred language.
User Feedback and Notifications:

