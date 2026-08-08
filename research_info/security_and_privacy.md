# Security and Farm Spatial Privacy Research

Research notes covering all security, authentication, and data privacy requirements for the TerraSpectra platform.

---

## 1. Farm Spatial Privacy

Hyperspectral imagery of private farmland is commercially sensitive for several reasons:
- Reveals crop health, yield predictions, and farming practices to competitors
- High-resolution spectral maps can identify exact field boundaries, irrigation layouts, and soil quality
- Inference from disease hotspot patterns can expose a farmer's pest management failures

### Legal Frameworks
- **GDPR (EU)**: Farms with GPS-tagged imagery fall under the definition of personal data if the owner is identifiable from land registry. Requires explicit consent for data collection, right to erasure, and data minimization.
- **USDA AMS Policy**: US farm-level data collected under USDA programs must follow the Confidential Information Protection and Statistical Efficiency Act (CIPSEA). Individual farm data cannot be publicly released.
- **UK Data Protection Act 2018**: Aligns with GDPR for post-Brexit UK farms.

### Spatial Data Anonymization Techniques
- **Coordinate Precision Reduction**: Truncate lat/lon to 2 decimal places in API responses (reduces precision from ~1m to ~1km)
- **Bounding Box Fuzzification**: Add ±0.005° random offset to reported field centroids
- **k-Anonymity for Spatial Data**: Ensure that any returned spatial feature represents a minimum of k=5 distinct farm entities, preventing individual farm identification
- **Aggregation**: Never return pixel-level coordinates. Return zone-level centroids only.

---

## 2. API Authentication and Authorization

### JWT (JSON Web Tokens)
JWTs are the standard stateless authentication mechanism for REST APIs. Structure: three base64url-encoded segments separated by dots:
- **Header**: `{"alg": "HS256", "typ": "JWT"}`
- **Payload**: `{"sub": "user_id_123", "role": "analyst", "farm_ids": ["iowa-001"], "exp": 1735689600}`
- **Signature**: `HMACSHA256(base64(header) + "." + base64(payload), SECRET_KEY)`

### Signing Algorithms
- **HS256 (HMAC-SHA256)**: Symmetric — same secret key signs and verifies. Suitable for single-server deployments.
- **RS256 (RSA-SHA256)**: Asymmetric — private key signs, public key verifies. Required for multi-service architectures where the inference server and auth server are separate.

### Role-Based Access Control (RBAC)
Three roles with different data access levels:
- **farmer**: Can only access their own farm's spectral data and predictions
- **analyst**: Can access multiple farms they are assigned to, can download raw datacube chunks
- **admin**: Full access to all farms, can manage users and API tokens

### Token Lifecycle
- Access token expiry: 15 minutes
- Refresh token expiry: 7 days
- Refresh token rotation: issue a new refresh token on every use and invalidate the previous one
- Token revocation: maintain a Redis blacklist of revoked JTI (JWT ID) values

### FastAPI OAuth2 Implementation
```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return user_id
    except JWTError:
        raise HTTPException(status_code=401)
```

---

## 3. CORS Security

CORS policy must be strictly configured. The risks of misconfiguration:
- `allow_origins=["*"]` combined with `allow_credentials=True` is rejected by browsers (spec violation) but still creates security risks if credentials mode is not set
- Wildcard origins allow any third-party website to make authenticated requests using the victim user's session cookies

### Correct Production Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://terraspectra.app", "https://app.terraspectra.io"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Processing-Time"],
    max_age=600,   # cache preflight for 10 minutes
)
```

---

## 4. API Security Headers

Full recommended header configuration for FastAPI middleware:

| Header | Value | Purpose |
| :--- | :--- | :--- |
| Content-Security-Policy | `default-src 'self'; img-src 'self' blob: data:` | Prevents XSS injection |
| X-Frame-Options | `DENY` | Blocks clickjacking via iframes |
| X-Content-Type-Options | `nosniff` | Prevents MIME type sniffing |
| Strict-Transport-Security | `max-age=31536000; includeSubDomains; preload` | Enforces HTTPS for 1 year |
| Referrer-Policy | `strict-origin-when-cross-origin` | Limits referrer header leakage |
| Permissions-Policy | `geolocation=(), camera=()` | Disables unused browser APIs |

---

## 5. CUDA GPU Memory Security

When multiple users share the same GPU inference server, stale data from one user's tensor can theoretically persist in VRAM and be read by a subsequent allocation.

### Mitigation Strategies
- **Zero-fill after inference**: Call `tensor.zero_()` and then `del tensor` followed by `torch.cuda.empty_cache()` after each prediction request
- **Process isolation**: Run each concurrent inference request in an isolated CUDA stream using `torch.cuda.Stream()`. Streams are independent and do not share intermediate buffers.
- **Separate CUDA contexts per user session**: For highest security, use separate worker processes (via `gunicorn` multi-worker mode) — each process has its own CUDA context
- **Disable CUDA unified memory**: Ensure `PYTORCH_NO_CUDA_MEMORY_CACHING=1` env var is not set in production as it bypasses the memory manager

---

## 6. Hyperspectral Data Encryption

### Data at Rest
- **AES-256-GCM**: Encrypt HDF5 datacube files stored on disk using Python `cryptography` library
- **Key Management**: Store AES keys in AWS KMS or HashiCorp Vault — never hardcode
- **Encrypted S3 Buckets**: Enable Server-Side Encryption (SSE-S3 or SSE-KMS) for all object storage containing raw satellite imagery
- **HDF5 native encryption**: The HDF5 library supports FILTER plugins for transparent encryption at the dataset level

### Data in Transit
- All API endpoints must be served over TLS 1.3 (deprecate TLS 1.2 and below)
- Configure uvicorn with SSL: `uvicorn main:app --ssl-keyfile key.pem --ssl-certfile cert.pem`
- Use HSTS (see security headers above) to ensure browsers always upgrade to HTTPS

---

## 7. Rate Limiting and DDoS Protection

The `/api/v1/predict` endpoint is computationally expensive (GPU inference). Without rate limiting, a single user could monopolize the GPU and deny service to others.

### slowapi for FastAPI
`slowapi` is a FastAPI-native rate limiting library:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/predict")
@limiter.limit("10/minute")   # max 10 inference requests per minute per IP
async def predict(request: Request, ...):
    ...
```

### Token Bucket Algorithm
The token bucket approach allows short bursts while enforcing a sustained average rate:
- Bucket capacity: 20 requests
- Refill rate: 1 token per 3 seconds
- On each request, consume 1 token. If empty, return HTTP 429 Too Many Requests.

---

## 8. Audit Logging

All API access must be logged with enough detail for compliance and forensic investigations:

### Log Format (JSON structured logging)
```json
{
  "timestamp": "2024-08-08T17:30:00Z",
  "user_id": "user_123",
  "role": "analyst",
  "endpoint": "/api/v1/spectra",
  "method": "GET",
  "params": {"lat": 41.582, "lng": -93.621},
  "ip_address": "203.0.113.42",
  "response_status": 200,
  "processing_time_ms": 142,
  "request_id": "req_abc123"
}
```

Use Python's `structlog` library for structured JSON log output. Ship logs to a SIEM (Security Information and Event Management) system like Splunk or AWS CloudWatch for retention and anomaly alerting.

### What to Log
- Every authentication attempt (success and failure)
- Every coordinate query with the requesting user ID
- All file download events (who downloaded which datacube)
- Any security header violations or rate limit triggers
