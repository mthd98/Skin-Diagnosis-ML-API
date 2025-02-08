# Skin-Diagnosis-ML-API

## Overview

The **Skin-Diagnosis-ML-API** is a machine learning-powered API designed to assist in diagnosing skin conditions through image analysis. This API leverages advanced algorithms to assess and classify skin conditions, providing valuable insights for healthcare professionals and researchers in dermatology.

## Features

- **Image Analysis**: Upload images of skin lesions to receive diagnostic predictions.
- **Machine Learning**: Utilizes trained models to assess and classify various skin conditions.
- **API Access**: Provides endpoints for seamless integration into healthcare applications.

## Prerequisites

Before setting up the application, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Installation and Setup

### Environment Variables

Before running the application, create a `.env` file in the root directory and set the following environment variables:

```plaintext
MONGO_USERNAME=<your_mongo_username>
MONGO_PASSWORD=<your_mongo_password>
```

Ensure that these credentials match your MongoDB configuration.

### Steps to Build and Run the API

#### 1. Clone the Repository

```bash
git clone https://github.com/mthd98/Skin-Diagnosis-ML-API.git
cd Skin-Diagnosis-ML-API
```

#### 2. Build the Docker Image

Ensure you have Docker installed and running. Then, build the Docker image using the provided `Dockerfile`:

```bash
docker build -t skin-diagnosis-ml-api .
```

#### 3. Run the Docker Container

After building the image, start the container with the following command:

```bash
docker run -d -p 8000:8000 skin-diagnosis-ml-api
```

This command runs the container in detached mode and maps port `8000` of the container to port `8000` on your host machine.

#### 4. Access the API

Once the container is running, the API will be accessible at:

```plaintext
http://localhost:8000
```

You can test the API endpoints using tools like `curl` or Postman.

## Usage

### Authentication

To use the API, you must include an API key in your request headers. You can obtain your API key from the system administrator.

### Example Request with API Key

To send a `POST` request to the `/predict` endpoint with an image file of a skin lesion, include the `access_token` header. Below is an example using `curl`:

```bash
curl -X POST -H "access_token: YOUR_API_KEY" -F "file=@path_to_your_image.jpg" http://localhost:8000/predict
```

Replace `YOUR_API_KEY` with your actual API key and `path_to_your_image.jpg` with the actual path to the image you want to analyze. The API will return a JSON response containing the diagnostic prediction.

### Python Example

Below is a Python example using the `requests` library to make a prediction request:

```python
import requests

url = "http://localhost:8000/predict"
headers = {"access_token": "YOUR_API_KEY"}
files = {"file": open("path_to_your_image.jpg", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

Ensure you replace `YOUR_API_KEY` with a valid API key and update `path_to_your_image.jpg` with the correct image path.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository, create a new branch, and submit a pull request with your proposed changes.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

