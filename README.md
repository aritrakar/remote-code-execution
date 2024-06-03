# Code execution website

This website is a tool to execute code in Python in the browser. It is useful for testing code snippets. The website also allows users to save code snippets to a local SQL database.

## Notes

- Execute Python code safely in a remote environment. Using **Docker** for sandboxing allows us to run the code in an isolated environment, which means malicious code cannot harm the system.
- Save code snippets to a local SQL database. This is achieved by using **FastAPI** and **SQLAlchemy**.
- Added logging to the backend to track the execution of code snippets and container creation/destruction.
- Initially, I was using Judge0 API to execute code snippets, but I decided to use Docker for sandboxing instead for two reasons:

  - Judge0 API has a rate limit of 100 requests/day. Now, I could have bypassed this by hosting my own Judge0 instance, but I lacked the computational resources for this approach.
  - It was proving tricky to install Python libraries in the Judge0. Using Docker allowed me to install any required libraries in the container, with no restrictions. Furthermore, the list of libraries to be installed in the Docker container can be extended at any time simply by editing the `Dockerfile` in the `backend` directory.
  - One drawback of using Docker is that it can someitmes be slow because it has to create a new container for each code snippet execution and subsequently destroy it. Furthermore, the container usually takes a few seconds to initialize, so if the code snippet is very small, the container creation time can be longer than the code execution time. Also, back-to-back execution of tests can sometimes cause conflict errors (HTTP error code 409) where a container being destroyed is also trying to be used for running fresh code.
    These problems could probably be mitigated by using a pool of containers and a queue of code execution tasks, with tasks being assigned to free containers as they arrive.

  Overall, using Docker instead of Judge0 allows me to have more control over the environment and the execution of code snippets.

## Screenshots

![Successful run](/etc/success.png)
![Failed run](/etc/failure.png)

## Technologies

### Frontend

- TypeScript
- React
- Next.js

### Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- Docker
- Gunicorn

### CI/CD

- GitHub Actions [TODO]

## Development

### Local development

1. Clone the repository
   ```bash
   git clone https://github.com/aritrakar/remote-code-execution.git
   ```
2. Install the dependencies

   ```bash
   cd remote-code-execution

   # Frontend dependencies
   cd frontend
   npm install -y

   # Backend dependencies
   cd ../backend
   python -m venv .venv
   source .venv/bin/activate # Or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. Start the development server

   ```bash
   # Start the frontend server
   cd frontend
   npm run dev

   # Start the backend server in a new terminal
   cd backend
   uvicorn main:app --reload
   ```

4. Additionally, if you wish to run backend tests, then run the following command:

   ```bash
   cd backend
   pytest
   ```

   Note that sometimes certain tests may fail due to the time taken to create and destroy Docker containers. This is a known issue and is mentioned in the notes section. You will usually see a 409 error for this case.
   To mitigate this error, I have added buffer times in the tests, but sometimes the tests may still fail.

## API endpoints

### `/execute`

- **Method:** `POST`
- **Request body:** The request body should contain the code to be executed. The could should probably be base64 encoded, but in my version I sent the plain text. For example:
  ```json
  {
    "code": "print('Hello, world!')"
  }
  ```
- **Response:** The response contains the output of the code, the time taken to execute the code, the memory used, and the exit code. For example:
  ```json
  {
    "output": "Hello, world!",
    "time": 0.001,
    "memory": 0.01,
    "exit_code": 0
  }
  ```

### `/submit`

It is almost exactly the same as the `/execute` endpoint, but it also saves the code snippet to the database, and thus also returns a `submission_id` field. The request method and body are the same as the `/execute` endpoint.

- **Response:** The response contains the output of the code, the time taken to execute the code, the memory used, the exit code, and the `submission_id`. The submissions are stored in `submissions.db`. For example:
  ```json
  {
    "submission_id": 1,
    "output": "Hello, world!",
    "time": 0.001,
    "memory": 0.01,
    "exit_code": 0
  }
  ```

## Future improvements

- Dockerize the frontend and backend and use Docker compose for easier deployments.
- Use GitHub Actions to setup testing.
- **Add support for more libraries:** This is easy to do by installing the required libraries in the Docker image.
- **Add support for more programming languages:** This can be done by creating more Docker images for different languages.
- **Add support for sharing code snippets:** Using `submission_id` would likely suffice, but probably better to use UUIDs and temporarily store snippets.
- Responsive design
- Dark mode

## Acknowledgements

I borrowed the frontend design from the freeCodeCamp tutorial for a React-based code editor found [here](https://www.freecodecamp.org/news/how-to-build-react-based-code-editor/). However, since it was in JavaScript, I had to make several changes to convert the code to TypeScript.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
