# Test AI Image Generation API (REST API Spec)

Service: **test_images_gen_api**

**Purpose**  
AI-powered image generation service that accepts uploaded image files and text prompts to generate new images using Google Gemini Image Generation Service.

**High-Level Flow**
1. Validate API version and correlation ID from headers
2. Accept uploaded image files and generation parameters
3. Process images and prompts through Gemini Image Generation API
4. Return generated image as base64 encoded data with metadata

---

## Base URLs

**Cloud Run**  
`https://test-images-gen-api-810737581373.asia-southeast1.run.app`

**Local (Uvicorn/FastAPI):**  
`http://127.0.0.1:8080`

**Swagger/OpenAPI:**  
`https://test-images-gen-api-810737581373.asia-southeast1.run.app/docs`

**ReDoc/OpenAPI:**  
`https://test-images-gen-api-810737581373.asia-southeast1.run.app/redoc`

---

## Guideline Alignment Notes

* ✅ **Resource-based URL:** `/images-gen` for image generation
* ✅ **HTTP methods:** `GET` for health/info, `POST` for image generation
* ✅ **HTTP status codes:** 2xx success, 4xx validation/format errors, 5xx processing errors
* ✅ **Correlation ID:** `X-Correlation-Id` auto-generation and passthrough (avoid sending duplicates)
* ✅ **API Version header:** `X-API-Version` (must be "1", anything else ⇒ status code 400)
* ✅ **Content types:** Supports `multipart/form-data` for file uploads
* ✅ **Response format:** All responses return JSON with consistent structure

---

## Environment Configuration

### Required Environment Variables
- `GEMINI_API_IMAGE_KEY`: API Key for Google Gemini Image Generation Service

### Local Development Setup
**Dependencies for local development:**
Listed in `requirements.txt`
```txt
python-dotenv>=1.0.0
```

**Environment file (.env):**
Create a `.env` file in the project root directory:
```bash
GEMINI_API_IMAGE_KEY=your_gemini_api_key_here
```

**Environment loading:**
The application automatically loads environment variables from `.env` file using python-dotenv in `routers/image_gen.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Middleware Configuration
- **CORS Middleware:** Allows access from all origins
- **Response Time Middleware:** Measures API response time and sends in response headers

---

## Authentication & Authorization

No authentication required for this API. All endpoints are public.

---

## Required Headers

* `X-API-Version` (string, **required**): API version (must be "1" only, other values return status code 400)
* `X-Correlation-Id` (string, optional): Request tracking ID (auto-generated if not provided, should be unique per request)
* `Content-Type` (string, **required** for POST endpoints): `multipart/form-data` (for POST /images-gen)

---

## Endpoints Summary

- `GET /` - API information and health check
- `POST /images-gen` - Generate images from uploaded files and prompts

---

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

---

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
- `400` invalid API version (`INVALID_FIELD_VALUE`)
- `415` unsupported media image type (`INVALID_CONTENT_TYPE`)
- `500` unexpected pipeline failure (`INTERNAL_ERROR`)
---

## 3) Standard Error Format

All errors use consistent JSON structure:

```json
{
  "code": "INVALID_FIELD_VALUE",
  "message": "Unsupported X-API-Version: 2",
  "correlationId": "corr_abc123"
}
```

---

## 4) Implementation Notes

### Development Guidelines

* **API Version:** Supports only version "1"
* **File Support:** Supports only `image/jpeg` and `image/png`
* **Correlation ID:** Auto-generated in format `corr_{uuid4()}` if not provided
* **Rate Limiting:** Depends on Google Gemini API limits

### Local Development Requirements

* **Python Dependencies:** Listed in `requirements.txt`, includes `python-dotenv>=1.0.0` for environment variable management, uncomment in `routers/image_gen.py` the lines with `from dotenv import load_dotenv` and `load_dotenv()`
* **Environment Variables:** Use `.env` file for local development (see Environment Configuration section)
* **Port Configuration:** Runs on `http://127.0.0.1:8080` by default (configurable)

---

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

---

## 6) Change Log

* **2026-02-10**: Updated API specification format to follow REST API standard guidelinesUpdated API specification format to follow REST API standard guidelines