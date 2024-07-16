FROM python:3.9-slim

WORKDIR /app
COPY . /app
# COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install scikit-learn==1.3.2

COPY . .

EXPOSE 5000

# Define the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask app using the array syntax
CMD ["flask", "run", "--host=0.0.0.0"]