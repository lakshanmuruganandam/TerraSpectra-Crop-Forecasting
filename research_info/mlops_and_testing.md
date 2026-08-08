# MLOps, Testing, and CI/CD Research

Research notes covering the full quality assurance and production monitoring stack for TerraSpectra.

---

## 1. pytest and pytest-asyncio

pytest is the Python standard for unit and integration testing. pytest-asyncio enables running async test functions against FastAPI's ASGI app.

### Installation
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### conftest.py Patterns
`conftest.py` defines fixtures shared across all test files in the same directory and subdirectories:
```python
# backend/tests/conftest.py
import pytest
import numpy as np

@pytest.fixture(scope="session")
def sample_hyperspectral_cube():
    """Synthetic 64x64x224 float32 cube for testing preprocessing functions."""
    rng = np.random.default_rng(seed=42)
    return rng.random((64, 64, 224), dtype=np.float32)

@pytest.fixture(scope="session")
def sample_wavelengths():
    return np.linspace(400, 2500, 224)
```

### Parametrize for Multiple Scenarios
```python
@pytest.mark.parametrize("n_components,expected_min_variance", [
    (16, 0.92),
    (32, 0.985),
    (64, 0.999),
])
def test_pca_explains_variance(sample_hyperspectral_cube, n_components, expected_min_variance):
    from backend.preprocessing.pca import run_pca
    result = run_pca(sample_hyperspectral_cube, n_components=n_components)
    assert result.explained_variance_ratio >= expected_min_variance
```

### Coverage Reporting
```bash
pytest backend/tests/ -v --cov=backend --cov-report=html --cov-report=term-missing
```
Target: minimum 85% line coverage across all backend modules.

---

## 2. vitest and @testing-library/react

vitest is the Vite-native test runner for the React frontend. It uses the same ESM module resolution as Vite, making it faster and more accurate than Jest for Vite projects.

### Configuration in vite.config.ts
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      reporter: ['text', 'html'],
      thresholds: { lines: 80, functions: 80 }
    }
  }
})
```

### Mocking Deck.gl and Mapbox
Deck.gl and Mapbox use WebGL which is unavailable in jsdom. Mock them:
```typescript
// src/test/setup.ts
vi.mock('@deck.gl/react', () => ({
  DeckGL: ({ children }: any) => <div data-testid="deckgl-mock">{children}</div>
}))

vi.mock('react-map-gl', () => ({
  Map: ({ children }: any) => <div data-testid="mapbox-mock">{children}</div>
}))
```

### Testing a Spectral Chart Component
```typescript
import { render, screen } from '@testing-library/react'
import { SpectralChart } from '../components/SpectralChart'

test('renders spectral chart with 224 bands', () => {
  const wavelengths = Array.from({length: 224}, (_, i) => 400 + i * 9.375)
  const reflectance = Array.from({length: 224}, () => Math.random())
  render(<SpectralChart wavelengths={wavelengths} reflectance={reflectance} />)
  expect(screen.getByTestId('spectral-chart')).toBeInTheDocument()
})
```

---

## 3. MLflow Experiment Tracking

MLflow tracks all training runs with parameters, metrics, and artifacts so experiments are reproducible and comparable.

### Logging a Training Run
```python
import mlflow
import mlflow.pytorch

with mlflow.start_run(run_name="3dcnn_vit_pca32_lr1e-4"):
    # Log hyperparameters
    mlflow.log_param("n_pca_components", 32)
    mlflow.log_param("learning_rate", 1e-4)
    mlflow.log_param("batch_size", 16)
    mlflow.log_param("patch_size", 64)
    
    for epoch in range(num_epochs):
        train_loss, val_loss, val_acc = train_epoch(model, loader)
        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)
        mlflow.log_metric("val_accuracy", val_acc, step=epoch)
    
    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.pytorch.log_model(model, "model")
    mlflow.log_param("final_val_accuracy", val_acc)
```

### Model Registry
After training, register the best model:
```python
mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="TerraSpectra-3DCNN-ViT"
)
# Transition to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="TerraSpectra-3DCNN-ViT", version=3, stage="Production"
)
```

---

## 4. Weights & Biases (wandb)

wandb provides richer visualization than MLflow, including real-time GPU utilization charts and automated hyperparameter sweep orchestration.

### Initialization
```python
import wandb

wandb.init(
    project="terraspectra-hsi",
    name="run_pca32_vit_base_epoch50",
    config={
        "n_pca_components": 32,
        "vit_model": "vit_base_patch16_224",
        "optimizer": "AdamW",
        "weight_decay": 1e-4,
        "dataset": "Salinas_Valley_corrected"
    }
)
```

### Spectral Band Importance Sweep
A wandb sweep can search over which PCA band counts maximize validation accuracy:
```yaml
# sweep_config.yaml
method: bayes
metric:
  name: val_accuracy
  goal: maximize
parameters:
  n_pca_components:
    values: [8, 16, 32, 64, 128]
  learning_rate:
    distribution: log_uniform_values
    min: 1e-5
    max: 1e-3
```
Run with: `wandb sweep sweep_config.yaml` then `wandb agent <sweep_id>`

### GPU Utilization Tracking
wandb automatically monitors GPU memory and utilization when `nvidia-smi` is available. No additional configuration is needed — just initialize the run.

---

## 5. Evidently AI for Spectral Concept Drift

Production hyperspectral data changes seasonally as solar illumination angle, atmospheric aerosol loading, and crop phenological stage all shift. Evidently detects when incoming data diverges from the training distribution.

### Setup
```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import ColumnDriftMetric
import pandas as pd

# Training-time reference data: mean reflectance per band per pixel sample
reference_df = pd.DataFrame(train_spectral_features, columns=[f"band_{i}" for i in range(32)])
current_df = pd.DataFrame(production_spectral_features, columns=[f"band_{i}" for i in range(32)])

report = Report(metrics=[
    DataDriftPreset(),
    ColumnDriftMetric(column_name="band_10"),  # Red Edge band drift
    ColumnDriftMetric(column_name="band_22"),  # NIR band drift
])
report.run(reference_data=reference_df, current_data=current_df)
report.save_html("drift_report.html")
```

### PSI (Population Stability Index)
PSI measures how much a variable's distribution has shifted:
- PSI < 0.1: No significant change
- 0.1 ≤ PSI < 0.2: Moderate shift — investigate
- PSI ≥ 0.2: Major shift — retrain immediately

Evidently computes PSI alongside Wasserstein distance and K-S test statistics.

---

## 6. Seasonal Illumination Drift

### Root Cause
Solar zenith angle (θ) at acquisition time directly affects measured surface reflectance. At θ = 30° (summer noon), reflectance appears brighter than the same surface at θ = 70° (winter). This is not a disease signal — it is an illumination artifact that corrupts predictions.

### Empirical Line Correction (ELC)
ELC uses in-scene reference panels (bright tarp + dark tarp with known reflectance) placed in the field during flights:
1. Measure DN values at the panel locations in the raw image
2. Fit a linear regression: `DN = a * Reflectance + b`
3. Apply the inverse transform to all pixels: `Reflectance = (DN - b) / a`

### Automated Retraining Trigger
When Maximum Mean Discrepancy (MMD) between training distribution (kernel embedding in a Reproducing Kernel Hilbert Space) and production data exceeds threshold τ = 0.05:
```python
from scipy.stats import ks_2samp

def check_drift_and_retrain(train_band_50, prod_band_50, threshold=0.05):
    stat, p_value = ks_2samp(train_band_50, prod_band_50)
    if p_value < threshold:
        trigger_retraining_pipeline()
        alert_slack(f"Spectral drift detected: KS stat={stat:.4f}, p={p_value:.6f}")
```

---

## 7. CI/CD for ML Pipelines

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: TerraSpectra CI

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: pytest backend/tests/ --cov=backend --cov-fail-under=85

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd research_info/frontend && npm ci
      - run: cd research_info/frontend && npm run test -- --coverage

  model-validation-gate:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    steps:
      - run: python scripts/validate_model.py --min-accuracy 0.92
```

### Model Validation Gate
Before any new model version is promoted to production, it must exceed 92% Overall Accuracy on the holdout test set. The `validate_model.py` script downloads the latest MLflow model artifact, runs inference on the test set, and exits with code 1 if the threshold is not met, blocking the deployment.

---

## 8. Benchmark Metrics for HSI Classification

Standard metrics used in hyperspectral remote sensing literature to evaluate classification performance:

### Overall Accuracy (OA)
OA = (correctly classified pixels) / (total pixels)
Reports the percentage of pixels assigned to the correct disease class. Ranges from 0 to 1.

### Average Accuracy (AA)
AA = (1/K) * Σ (correctly classified pixels in class k / total pixels in class k)
Averages per-class accuracy across all K classes. More informative than OA when class sizes are imbalanced (disease vs healthy pixels).

### Kappa Coefficient (κ)
κ = (OA - Pe) / (1 - Pe), where Pe is the expected accuracy from random chance.
κ > 0.8 indicates strong agreement, κ > 0.6 is acceptable for agricultural remote sensing.

### Per-Class Metrics
For each disease severity class (healthy, mild stress, moderate blight, severe necrosis):
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1 = 2 * Precision * Recall / (Precision + Recall)

### Confusion Matrix Interpretation
A well-trained model on hyperspectral data typically shows:
- High confusion between adjacent severity classes (mild ↔ moderate) due to spectral similarity
- Low confusion between extreme classes (healthy ↔ severe necrosis) — large spectral distance
- Red Edge band misclassification is the most common error in early-stage disease detection
