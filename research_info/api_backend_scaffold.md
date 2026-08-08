# API Backend Scaffold Research

Research notes for the TerraSpectra FastAPI backend architecture covering all Phase 5 backend checklist items.

---

## 1. FastAPI Framework Architecture

FastAPI is built on top of Starlette (ASGI web framework) and Pydantic (data validation). It is fully async by default, which is critical for non-blocking I/O when reading large HDF5 files or waiting on GPU inference.

### ASGI and Uvicorn
ASGI (Asynchronous Server Gateway Interface) replaces WSGI for async Python web apps. FastAPI requires an ASGI server. Uvicorn is the recommended server:
- `uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --workers 4`
- For production use `gunicorn` with uvicorn workers: `gunicorn backend.api.main:app -k uvicorn.workers.UvicornWorker -w 4`

### App Initialization and Lifespan
The `lifespan` context manager handles startup and shutdown logic (loading ML models into GPU memory on startup, releasing on shutdown):
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model to GPU
    app.state.model = load_model_to_cuda()
    yield
    # Shutdown: free GPU memory
    del app.state.model
    torch.cuda.empty_cache()

app = FastAPI(title="TerraSpectra API", version="1.0.0", lifespan=lifespan)
```

### Router Structure
Routes are organized into APIRouter modules to keep the codebase clean:
```
backend/api/
    main.py         - FastAPI app, CORS middleware, router registration
    routers/
        health.py   - GET /health
        pca.py      - POST /api/v1/pca/reduce
        spectra.py  - GET /api/v1/spectra
        predict.py  - POST /api/v1/predict
    models/
        schemas.py  - Pydantic request/response DTOs
```

---

## 2. CORS Middleware

CORS (Cross-Origin Resource Sharing) is required because the React frontend (running on `localhost:5173`) calls the API (running on `localhost:8000`) — these are different origins by HTTP spec.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://terraspectra.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

The browser sends a preflight `OPTIONS` request before any cross-origin POST. FastAPI + CORSMiddleware handles these automatically. Using `allow_origins=["*"]` (wildcard) is insecure for production and should be replaced with an explicit allowlist.

---

## 3. Pydantic DTOs (Data Transfer Objects)

All request body and response schemas are defined as Pydantic v2 `BaseModel` classes. FastAPI reads these to validate incoming JSON and to generate Swagger documentation automatically.

### Request Models
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class PCAReduceRequest(BaseModel):
    pixel_array: List[List[float]]   # 2D list: (n_pixels, n_bands)
    n_components: int = Field(default=32, ge=8, le=200)
    target_variance: float = Field(default=0.985, ge=0.9, le=1.0)

class SpectraRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    dataset_id: Optional[str] = None
```

### Response Models
```python
class PCAReduceResponse(BaseModel):
    reduced_array: List[List[float]]  # (n_pixels, n_components)
    explained_variance: float         # cumulative explained variance ratio
    n_components_used: int
    processing_time_ms: float

class SpectraResponse(BaseModel):
    wavelengths: List[float]          # e.g. [400.0, 410.0, ..., 2500.0]
    reflectance: List[float]          # normalized reflectance values [0.0, 1.0]
    latitude: float
    longitude: float
    disease_probability: Optional[float] = None
```

### Serializing NumPy Arrays for JSON
NumPy arrays are not JSON serializable by default. Convert before returning:
```python
return PCAReduceResponse(
    reduced_array=reduced_cube.tolist(),
    explained_variance=float(np.sum(pca.explained_variance_ratio_)),
    ...
)
```

---

## 4. API Endpoints Design

### GET /health
Returns server status, GPU availability, and model version for monitoring:
```
Response 200:
{
  "status": "healthy",
  "gpu_available": true,
  "gpu_name": "NVIDIA RTX 4090",
  "model_version": "v1.2.0",
  "uptime_seconds": 3600
}
```

### POST /api/v1/pca/reduce
Accepts a batch of pixel spectral vectors, applies fitted PCA, and returns reduced components:
- Input: `PCAReduceRequest` with pixel_array shape (N, 224)
- Output: `PCAReduceResponse` with reduced_array shape (N, 32)
- Processing: Reshapes, normalizes, applies sklearn PCA transform
- Response time target: < 500ms for a 512x512 spatial chunk

### GET /api/v1/spectra
Accepts lat/lng query params, returns the 224-band reflectance array for that pixel:
- Queries the in-memory indexed HDF5 datacube using a spatial lookup table (GLT)
- Used by Deck.gl onClick handler to populate the Plotly spectral chart

### POST /api/v1/predict
Accepts a spatial tile (tiled chunk of the HDF5 cube), runs it through the 3D-CNN + ViT model, returns a disease probability heatmap for that tile:
- Input: base64-encoded or multipart form uploaded array chunk
- Output: disease probability map as base64 PNG + class labels
- GPU inference with mixed precision (FP16)

---

## 5. Sliding Window Spatial Tiling

A full 1000x1000x224 hyperspectral scene cannot fit in GPU memory for inference. The solution is overlapping spatial patching.

### Tile Parameters
- Patch size: 64x64 spatial pixels, all 224 bands
- Stride: 32 pixels (50% overlap to eliminate edge artifacts)
- Overlap region is averaged during reassembly

### Patch Extraction Logic
For a scene of shape (H, W, B), extract patches at positions:
- Row positions: `range(0, H - patch_size + 1, stride)`
- Col positions: `range(0, W - patch_size + 1, stride)`
- Each patch shape: (patch_size, patch_size, B)

### Prediction Reassembly
Use a weight map (Hann window or Gaussian) to blend overlapping predictions smoothly, preventing hard borders between tiles in the final output heatmap.

---

## 6. Swagger / OpenAPI Documentation

FastAPI automatically generates OpenAPI 3.0 spec from Pydantic models and route decorators.

- Interactive Swagger UI: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- Raw OpenAPI JSON: `http://localhost:8000/openapi.json`

To add examples to Swagger, use `Field(example=...)` in Pydantic models or include `openapi_extra` in route decorators.

---

## 7. Async Testing with pytest and httpx

Testing FastAPI requires an async HTTP client that can call ASGI apps directly without starting a real server:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from backend.api.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_pca_reduce():
    payload = {
        "pixel_array": [[0.1] * 224],  # single pixel, 224 bands
        "n_components": 32
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/pca/reduce", json=payload)
    assert response.status_code == 200
    assert len(response.json()["reduced_array"][0]) == 32
```

Run tests: `pytest backend/tests/ -v --asyncio-mode=auto --cov=backend --cov-report=html`

---

## 8. API Security Headers

FastAPI does not add security headers by default. Add them via a custom middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### HTTP Bearer Token Auth
Use FastAPI's HTTPBearer security scheme to protect inference endpoints:
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

@app.post("/api/v1/predict")
async def predict(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # validate JWT token against secret key
    ...
```
