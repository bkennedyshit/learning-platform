# Problem Generator Service

FastAPI/SymPy sidecar for Kiro task 7.1.

The service exposes the internal problem generator endpoint:

```http
POST /generate
Content-Type: application/json

{
  "subject": "algebra",
  "tier": "easy"
}
```

Response:

```json
{
  "subject": "algebra",
  "tier": "easy",
  "problem": "Solve for x: 2*x + 3 = 11",
  "solution": "x = 4"
}
```

Supported subjects:

- `arithmetic`
- `algebra`

Supported tiers:

- `easy`
- `medium`
- `hard`
- `exam`

Unsupported subjects return `400 Bad Request` with a clear message and the supported subject list.

## Run Locally

From this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

Then call:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8010/generate `
  -ContentType "application/json" `
  -Body '{"subject":"algebra","tier":"medium"}'
```

## Test

```powershell
python -m pytest
```
