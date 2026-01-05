# FastAPI Image Analysis Service

A FastAPI backend service for image upload and mock AI-style analysis. Built with clean architecture principles, idempotent operations, and local filesystem storage.

## Quick Start

### Option 1: Local Development

#### Prerequisites

- Python 3.10+
- pip

#### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python -m uvicorn app.main:app --reload
```

The service will be available at `http://localhost:8000`

### Option 2: Docker

#### Prerequisites

- Docker installed and running

#### Build and Run

1. Build the Docker image:
```bash
docker build -t image-analysis-service .
```

2. Run the container:
```bash
docker run -p 8000:8000 image-analysis-service
```

The service will be available at `http://localhost:8000`

#### Docker with Volume Mounts (for persistent data)

```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data image-analysis-service
```

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### POST /upload

Upload an image file for analysis.

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload (JPEG or PNG, max 5MB)

**Response:**
```json
{
  "image_id": "abc123-def456-..."
}
```

**Status Codes:**
- `201 Created`: Image uploaded successfully
- `400 Bad Request`: Invalid file type
- `413 Request Entity Too Large`: File exceeds 5MB limit
- `500 Internal Server Error`: Server error

**Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@image.jpg"
```

### POST /analyze

Analyze an uploaded image and return structured results.

**Request:**
```json
{
  "image_id": "abc123-def456-..."
}
```

**Response:**
```json
{
  "image_id": "abc123-def456-...",
  "skin_type": "Oily",
  "issues": ["Hyperpigmentation", "Acne"],
  "confidence": 0.87
}
```

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request format
- `404 Not Found`: Image with given ID not found
- `500 Internal Server Error`: Server error

**Example:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "abc123-def456-..."}'
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Validation Rules

### Image Upload

- **Supported formats**: JPEG, PNG
- **Maximum file size**: 5MB
- **MIME type validation**: Only `image/jpeg`, `image/jpg`, and `image/png` are accepted
- **File size validation**: Files must be between 1 byte and 5MB

### Analysis

- **Image ID format**: UUID4 string
- **Idempotency**: Repeated analysis calls for the same `image_id` return identical results

## Idempotency

The `/analyze` endpoint is designed to be idempotent:

1. **First call**: Performs mock analysis, saves result to `data/analysis/{image_id}.json`, returns result
2. **Subsequent calls**: Returns cached result from filesystem without re-computation
3. **Deterministic results**: Same `image_id` always produces the same analysis results

This ensures:
- Safe retry behavior for mobile clients
- No unnecessary computation
- Consistent API responses
- Predictable behavior for testing

## Project Structure

```
app/
├── main.py                 # FastAPI app initialization
├── config.py               # Configuration constants
├── routes/
│   ├── upload.py           # Image upload endpoint
│   └── analyze.py          # Analysis endpoint
├── services/
│   ├── image_service.py    # Image processing logic
│   ├── analysis_service.py # Analysis logic with caching
│   └── exceptions.py       # Custom exceptions
├── utils/
│   ├── validators.py       # File validation
│   ├── file_storage.py     # Filesystem operations
│   └── id_generator.py     # UUID generation
└── models/
    └── schemas.py          # Pydantic models

data/
├── images/                 # Uploaded image files
└── analysis/               # Cached analysis results
```

## Logging

The service includes structured logging for:
- HTTP requests (method, path, status code)
- Image uploads (image_id, file size, MIME type)
- Analysis operations (image_id, cached vs. new)
- Errors with context (operation, error message, image_id when applicable)

Logs are output to stdout in the format:
```
YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - message
```

Log levels:
- **INFO**: Normal operations (uploads, analysis, requests)
- **WARNING**: Validation failures, missing resources
- **ERROR**: Exceptions and errors
- **DEBUG**: Detailed operation information

## Assumptions

1. **Local development**: Service runs on localhost with CORS enabled for all origins
2. **No authentication**: Endpoints are publicly accessible (not production-ready)
3. **Synchronous operations**: File I/O is synchronous for simplicity
4. **No database**: Filesystem storage is sufficient for this scope
5. **Mock analysis**: Analysis results are deterministic pseudo-random based on image_id hash
6. **Single instance**: Not designed for horizontal scaling without shared storage
7. **Logging**: Structured logging to stdout (can be redirected to files or log aggregation services)

## Production Improvements

For a production deployment, consider:

1. **Authentication & Authorization**
   - API key authentication
   - JWT tokens for user sessions
   - Rate limiting per user/IP

2. **Database**
   - Replace filesystem metadata with PostgreSQL/MongoDB
   - Store image metadata, user associations, analysis history
   - Enable efficient querying and indexing

3. **Async Workers**
   - Move analysis to background tasks (Celery, RQ)
   - Webhook notifications when analysis completes
   - Queue management for high-volume scenarios

4. **Cloud Storage**
   - Replace local filesystem with S3/GCS/Azure Blob
   - CDN for image delivery
   - Automatic backup and versioning

5. **Monitoring & Observability**
   - Structured logging (JSON format)
   - Metrics collection (Prometheus)
   - Distributed tracing (OpenTelemetry)
   - Error tracking (Sentry)

6. **Scalability**
   - Horizontal scaling with load balancer
   - Shared storage (S3, NFS)
   - Caching layer (Redis) for analysis results
   - Database connection pooling

7. **Security**
   - Input sanitization and validation
   - File type verification beyond MIME type
   - Virus scanning for uploads
   - HTTPS enforcement
   - Security headers (CSP, HSTS)

8. **Testing**
   - Unit tests for services and utilities
   - Integration tests for endpoints
   - Load testing for performance validation

9. **Documentation**
   - OpenAPI/Swagger specification
   - API versioning strategy
   - Rate limit documentation
   - Error code reference

10. **DevOps**
    - ✅ Docker containerization (included)
    - CI/CD pipeline
    - Environment-specific configurations
    - ✅ Health checks (included in Dockerfile)

## License

This is a demonstration project for evaluation purposes.
