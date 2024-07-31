# Insurance Claims Prediction System

This project provides an intelligent system for predicting the approval status of insurance claims. It includes data preprocessing, model training, and a web interface for users to input claim details and receive predictions.

## Project Structure

- `checking.ipynb`: Jupyter notebook for data preprocessing and model training.
- `app.py`: Flask application for serving the prediction model through a web interface.
- `Dockerfile`: Docker configuration for containerizing the application.
- `templates/index.html`: HTML template for the web interface.
- `.github/workflows/main.yml`: GitHub Actions workflow for CI/CD.
- `requirements.txt`: List of Python dependencies.
- `.gitattributes`: Configuration for Git LFS.

## Usage

### Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/grishmaaa/insurance-claims-prediction.git
   cd insurance-claims-prediction
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   flask run
   ```

4. Open your browser and navigate to `http://localhost:5000` to access the web interface.

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t insurance-claims-prediction .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 insurance-claims-prediction
   ```

3. Open your browser and navigate to `http://localhost:5000` to access the web interface.

### GitHub Actions CI/CD

- Ensure you have set the following secrets in your GitHub repository:
  - `DOCKER_USERNAME`: Your Docker Hub username.
  - `DOCKER_PASSWORD`: Your Docker Hub password.

- On push to the `main` branch, the workflow will build and push the Docker image to Docker Hub.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.
