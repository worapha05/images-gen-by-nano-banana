# Test AI Image Generation API (REST API Spec)

Service: **test_images_gen_api**

**Purpose**  
AI-powered image generation service that accepts uploaded image files and text prompts to generate new images using Google Gemini Image Generation Service.

**High-Level Flow**
1. Validate API version and correlation ID from headers
2. Accept uploaded image files and generation parameters
3. Process images and prompts through Gemini Image Generation API
4. Return generated image as base64 encoded data with metadata

## Base URLs

**Cloud Run**  
`https://test-images-gen-api-810737581373.asia-southeast1.run.app`

**Local Development**  
`http://127.0.0.1:8080`

**Swagger/OpenAPI (Cloud Run)**  
`https://test-images-gen-api-810737581373.asia-southeast1.run.app/docs`

**ReDoc/OpenAPI (Cloud Run)**  
`https://test-images-gen-api-810737581373.asia-southeast1.run.app/redoc`

## Guideline Alignment Notes

* ✅ **Resource-based URL:** `/images-gen` for image generation
* ✅ **HTTP methods:** `GET` for health/info, `POST` for image generation
* ✅ **HTTP status codes:** 2xx success, 4xx validation/format errors, 5xx processing errors
* ✅ **Correlation ID:** `X-Correlation-Id` auto-generation and passthrough (avoid sending duplicates)
* ✅ **API Version header:** `X-API-Version` (must be "1", anything else ⇒ status code 400)
* ✅ **Content types:** Supports `multipart/form-data` for file uploads
* ✅ **Response format:** All responses return JSON with consistent structure

## Environment Configuration

### Required Environment Variables
- `GEMINI_API_IMAGE_KEY`: API Key for Google Gemini Image Generation Service

## Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```
2.  **Create a `.env` file in the project root directory**
    ```bash
    GEMINI_API_IMAGE_KEY=your_gemini_api_key_here
    ```
3.  **Build and run the project with Docker Compose**
    ```bash
    docker compose up -d --build
    ```

    ### Running the Application

    To run the application, use `docker compose` without rebuilding the image:

    ```bash
    docker compose up -d
    ```

    The API will be available at `http://127.0.0.1:8080`.

    ### Stop the Application

    ```bash
    docker compose down
    ```

## GCP Deployment Steps

1. **Authenticate with Google Cloud**
    ```bash
    gcloud auth login
    gcloud config set project <PROJECT_ID>
    ```

2. **Open root folder**

3. **Deploy to Cloud Run**
    ```bash
    gcloud run deploy <SERVICE_NAME> \
      --source . \
      --region <REGION_NAME> \
      --set-secrets "GEMINI_API_IMAGE_KEY=<SECRET_KEY_NAME>:latest" \
      --allow-unauthenticated
    ```

**Note:** Replace `<PROJECT_ID>`, `<SERVICE_NAME>`, `<REGION_NAME>`, and `<SECRET_KEY_NAME>` with your actual values.

## Creation of SECRET_KEY in GCP

Before deploying to Cloud Run with `--set-secrets`, you must create a secret in **Google Cloud Secret Manager**.

1. **Authenticate with Google Cloud**
    ```bash
    gcloud auth login
    gcloud config set project <PROJECT_ID>
    ```

2. **Enable the Secret Manager API** (if not already enabled)
    ```bash
    gcloud services enable secretmanager.googleapis.com
    ```

3. **Create a new secret with your Gemini API key**
    ```bash
    echo -n "<SECRET_KEY_VALUE>" | \
      gcloud secrets create <SECRET_KEY_NAME> \
        --replication-policy="automatic" \
        --data-file=-
    ```

4. **Verify the secret was created**
    ```bash
    gcloud secrets list
    ```

5. **Grant Cloud Run access to the secret** (if needed)
    ```bash
    gcloud secrets add-iam-policy-binding <SECRET_KEY_NAME> \
      --member="serviceAccount:<PROJECT_NUMBER>-compute@developer.gserviceaccount.com" \
      --role="roles/secretmanager.secretAccessor"
    ```

6. **(Optional) Update an existing secret version**
    ```bash
    echo -n "<NEW_SECRET_KEY_VALUE>" | \
      gcloud secrets versions add <SECRET_KEY_NAME> --data-file=-
    ```

7. **(Optional) Destroy an existing secret version**
    ```bash
    gcloud secrets versions destroy <SECRET_KEY_VERSION> --secret="<SECRET_KEY_NAME>"
    ```

8. **(Optional) Check versions of SECRET_KEY**
    ```bash
    gcloud secrets versions list <SECRET_KEY_NAME>
    ```

**Note:** Replace the following placeholders with your actual values:
- `<SECRET_KEY_NAME>` — the secret name (e.g., `gemini-api-image-key`)
- `<SECRET_KEY_VALUE>` — the secret value (e.g., `my-password`)
- `<NEW_SECRET_KEY_VALUE>` — the new secret value (when updating)
- `<SECRET_KEY_VERSION>` — the secret version number to destroy (e.g., `1`)
- `<PROJECT_ID>` — your GCP project id (found in the GCP Console dashboard)
- `<PROJECT_NUMBER>` — your GCP project number (found in the GCP Console dashboard)

## Middleware Configuration
- **CORS Middleware:** Allows access from all origins
- **Response Time Middleware:** Measures API response time and sends in response headers

## Authentication & Authorization

No authentication required for this API. All endpoints are public.

## Required Headers

* `X-API-Version` (string, **required**): API version (must be "1" only, other values return status code 400)
* `X-Correlation-Id` (string, optional): Request tracking ID (auto-generated if not provided, should be unique per request)
* `Content-Type` (string, **required** for POST endpoints): `multipart/form-data` (for POST /images-gen)

## Endpoints Summary

- `GET /` - API information and health check
- `POST /images-gen` - Generate images from uploaded files and prompts

## 1) API Information Endpoint

### GET /

Basic API information and health status details

**Response:** `200 OK`
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

## 2) Image Generation Endpoint

### POST /images-gen

Generate new images from uploaded images and provided prompts

#### Request Schema (Form Data)

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| files | List[File] | ❌ | - | Image files to upload (supports JPEG, PNG) |
| prompt | string | ❌ | - | Text description for image generation |
| aspect_ratio | string | ❌ | "1:1" | Image aspect ratio |
| resolution | string | ❌ | "1K" | Image resolution |

#### Supported Values

**aspect_ratio:** `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**resolution:** `1K` (Low resolution), `2K` (Medium resolution), `4K` (High resolution)

#### Supported Content Types
- `image/jpeg`
- `image/png`

#### Example Request

```bash
curl -X POST "http://localhost:8080/images-gen" \
  -H "X-API-Version: 1" \
  -H "X-Correlation-Id: my-unique-id-123" \
  -F "files=@image1.jpg" \
  -F "files=@image2.png" \
  -F "prompt=Create a beautiful artwork from this image" \
  -F "aspect_ratio=16:9" \
  -F "resolution=2K"
```

#### Responses
Headers always echo `X-Correlation-Id`, `X-API-Version` and `X-Response-Time-Seconds`.

**200 OK — Success**

```json
{
  "code": "SUCCESS",
  "message": "Image generated successfully",
  "correlationId": "my-unique-id-123",
  "image": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "size": [
    1024,
    1024
  ]
}
```

**Other Status Codes**
- `400` Invalid API version (`INVALID_FIELD_VALUE`)
- `415` Unsupported media image type (`INVALID_FILE_TYPE`)
- `500` Cannot convert uploaded images to bytes (`IMAGE_CONVERSION_ERROR`)
- `500` Model returned no image, blocked or empty response (`NO_IMAGE_RETURNED`)
- `500` Cannot process image bytes (`IMAGE_PROCESSING_ERROR`)
- `500` Unexpected pipeline failure (`INTERNAL_ERROR`)

## 3) Standard Error Format

All errors use consistent JSON structure:

```json
{
  "code": "INVALID_FIELD_VALUE",
  "message": "Unsupported X-API-Version: 2",
  "correlationId": "corr_abc123"
}
```

## 4) Implementation Notes

### Development Guidelines

* **API Version:** Supports only version "1"
* **File Support:** Supports only `image/jpeg` and `image/png`
* **Correlation ID:** Auto-generated in format `corr_{uuid4()}` if not provided
* **Rate Limiting:** Depends on Google Gemini API limits

### Local Development Requirements

* **Environment Variables:** Use `.env` file for local development (see Environment Configuration section)
* **Port Configuration:** Runs on `http://127.0.0.1:8080` by default (configurable)

## 5) Internal Dependencies

| Component | Purpose | Notes |
| --------- | ------- | ----- |
| Google Gemini Image API | AI image generation processing | Requires `GEMINI_API_IMAGE_KEY` configuration |
| FastAPI Framework | REST API server implementation | Handles routing, validation, middleware |
| Response Time Middleware | Performance monitoring | Adds `X-Response-Time-Seconds` header |
| CORS Middleware | Cross-origin access control | Allows all origins by default |
| python-dotenv | Environment variable management | Loads local `.env` file for development |
| python-multipart | Multipart form data support | Handles file uploads in FastAPI |
| Pillow (PIL) | Image processing library | Image format validation and manipulation |
| Base64 Encoding | Image data encoding | Encodes generated images as `data:image/png;base64,` format for API response |

## 6) Change Log

* **2026-02-10**: Updated API specification format to follow REST API standard guidelines
* **2026-02-25**: Added GCP Secret Manager setup and Deployment guide