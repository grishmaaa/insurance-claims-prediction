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

## Setup Instructions

### 1. Data Preprocessing and Model Training

1. **Load Data**: Read the dataset from `Insurance claims data.csv`.
2. **Identify Columns**: Categorize columns into categorical, boolean, and numerical types.
3. **Class Imbalance**: Check for class imbalance in the target variable.
4. **Encoding**: Encode categorical and boolean columns using `LabelEncoder`.
5. **Scaling**: Scale numerical columns using `StandardScaler`.
6. **Handling Imbalance**: Use SMOTE to handle class imbalance.
7. **Train-Test Split**: Split the data into training and testing sets.
8. **Model Training**: Train a RandomForestClassifier model.
9. **Save Artifacts**: Save the trained model, scaler, and label encoders using `joblib`.
10. **Model Evaluation**: Evaluate the model and print accuracy, classification report, and confusion matrix.

### 2. Flask Application

- **Routes**:
  - `/`: Renders the home page with the prediction form.
  - `/predict`: Handles form submission, processes input data, makes predictions, and returns the result.
- **Prediction Function**: Encodes input data, scales numerical features, and predicts the claim status using the trained model.

### 3. Dockerization

- **Dockerfile**:
  - Uses `python:3.9-slim` as the base image.
  - Sets the working directory to `/app` and copies the project files.
  - Installs dependencies from `requirements.txt`.
  - Exposes port 5000 and sets the Flask application environment variable.
  - Runs the Flask application.

### 4. HTML Template

- **index.html**:
  - Contains a form for user input with fields for various claim details.
  - Uses Bootstrap for styling and jQuery for client-side validation.
  - Displays the prediction result after form submission.

### 5. CI/CD

- **GitHub Actions Workflow**:
  - Triggers on push to the `main` branch.
  - Sets up Docker Buildx for building multi-platform images.
  - Caches Docker layers to speed up builds.
  - Logs in to Docker Hub using secrets.
  - Builds and pushes the Docker image to Docker Hub.

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
