# Code execution website

This website is a tool to execute code in Python in the browser. It is useful for testing code snippets. The website also allows users to save code snippets to a local SQL database.

## Screenshots

## Technologies

### Frontend

- React
- TypeScript
- Next.js

### Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- Docker
- Gunicorn

### CI/CD

- GitHub Actions

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

## Future improvements

- **Add support for more libraries:** This is easy to do by installing the required libraries in the Docker image.
- Add support for more programming languages
- Add support for sharing code snippets
- Dark mode
- Responsive design

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
