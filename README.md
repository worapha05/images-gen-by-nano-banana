# Image Gen API

This is a FastAPI-based API for image generation. It allows users to upload an image, which is then processed and a new image is sent back to the client.

## Features

-   Image generation using Google's Generative AI.
-   FastAPI framework for high performance.
-   CORS enabled for all origins.
-   Middleware to track response time.

## Project Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
├── middleware/
│   ├── __init__.py
│   └── response_time.py
├── routers/
│   ├── __init__.py
│   └── image_gen.py
└── services/
    ├── __init__.py
    └── image_gen.py
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd nano-banana
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.8+ installed.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the application locally, use `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

The following endpoints are available:

### `GET /`

Returns basic information about the API.

-   **Response (`application/json`)**
    ```json
    {
        "message": "Image Gen API",
        "version": "1.0.0",
        "endpoint": {
            "upload": "POST /images-gen",
            "docs": "/docs"
        }
    }
    ```

### `POST /images-gen`

Accepts an image file and returns a generated image.

-   **Request:** `multipart/form-data` with a file field named `file`.
-   **Response:** An image file.

### `GET /docs`

Provides interactive API documentation (Swagger UI).

### `GET /redoc`

Provides alternative API documentation (ReDoc).
