

# Project Title

A brief description of your project and its goals.

## Table of Contents

- [Project Title](#project-title)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Tech Stack](#tech-stack)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Observability](#observability)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Introduction

Provide an overview of your application. Explain the core functionality and why these technologies were chosen.

## Tech Stack

- **Streamlit**: A Python library for building interactive web apps for ML and data science.
- **PostgreSQL & pgAdmin4**: A powerful, open source object-relational database system paired with a web-based administration interface.
- **dspy.ai**: A toolkit for building and deploying data science pipelines and applications.
- **Weaviate Vector Database**: A cloud-native, modular, real-time vector search engine for production.
- **MLflow**: An open source platform for managing the end-to-end machine learning lifecycle, including experiment tracking and model registry.

## Prerequisites

Make sure you have the following installed on your machine:

- Docker & Docker Compose
- Python 3.8+
- (Optional) `make` for running predefined commands

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-project.git
   cd your-project
   ```

2. Create a `.env` file (based on `.env.example`) and update environment variables as needed:
   ```bash
   cp .env.example .env
   # Edit .env with your settings    
   ```

   Your file should contain the following:

   ```bash
    OPENAI_API_KEY=YOUR_OPENAI_KEY
    OPENAI_TEXT_EMBEDDING_MODEL=OPENAI_TEXT_EMBEDDING_MODEL

    # Weaviate Configurations
    WEAVIATE_PORT=8080
    WEAVIATE_HOST=localhost

    # TAVILY Configurations
    TAVILY_API_KEY=YOUR TAVILY API KEY

    WEAVIATE_URL=http://host.docker.internal:8080

    # POSTGRESQL Configurations
    POSTGRES_URL=postgresql+psycopg2://username:password@postgres-mlflow:5432/mlflowdb

    MLFLOW_TRACKING_URI=http://mlflow:5000
    ```

## Docker Setup

The project uses Docker Compose to orchestrate multiple services. The following services will be started:

- **streamlit-app**: Runs the Streamlit frontend.
- **postgres**: PostgreSQL database service.
- **pgadmin**: pgAdmin4 for database administration.
- **dspy**: dspy.ai service for your data science pipelines.
- **weaviate**: Vector database for semantic search.
- **mlflow**: MLflow server for experiment tracking and model registry.

To start all services, run:

```bash
# Command is used to build the custom myflow image, with the required python packages
docker build -t my-mlflow-server ./mlflow
```

```bash
docker-compose up -d --build
```

To view logs:
```bash
docker-compose logs -f
```

To stop the services:
```bash
docker-compose down
```

## Usage

1. Streamlit UI: http://localhost:8501  
2. PostgreSQL: host=`postgres`, port=`5432`, user/password from `.env`  
3. Weaviate: http://localhost:8080 
4. MLflow UI: http://localhost:5001
5. Minio UI (Object Storage): http://localhost:9001 

## Observability

MLflow provides experiment tracking and model registry capabilities:

- Navigate to the MLflow UI at `http://localhost:5000` to view traces.
- Use the MLflow Python API to log metrics, parameters, and models in your code.

Example:
```python
import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")
with mlflow.start_run():
    mlflow.log_param("param1", 5)
    mlflow.log_metric("accuracy", 0.89)
    mlflow.sklearn.log_model(model, "model")
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

Specify your project license here.

## Contact

Your Name – [@your_twitter](https://twitter.com/your_twitter) – your.email@example.com

Project Link: [https://github.com/your-username/your-project](https://github.com/your-username/your-project)