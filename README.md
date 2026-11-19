# Stroke Risk Monitoring — IBM Granite Agent System

Preventive health monitoring system powered by **IBM Granite 3 8B Instruct** via watsonx.ai.

| Setting | Value |
|---|---|
| Model | `ibm/granite-3-8b-instruct` |
| Project ID | `746c612f-47a6-4d52-96df-87c9aa25f468` |
| Prompt format | `<\|system\|> … <\|user\|> … <\|assistant\|>` |
| Output format | Structured JSON for every agent |

---

## Project Structure

```
app/
  __init__.py
  services/
    __init__.py
    prompts.py          ← All Granite prompt templates
requirements.txt
```

---

## Agent Prompt Reference

| # | Agent | Function | Input | Key JSON Output Fields | Safety Feature |
|---|---|---|---|---|---|
| 1 | **Stroke Risk Assessment** | `stroke_risk_assessment_prompt(patient)` | `patient: dict` | `risk_score`, `risk_level`, `key_factors`, `summary`, `recommendation` | Disclaimer injected in every response |
| 2 | **Blood Pressure Monitoring** | `blood_pressure_monitoring_prompt(current, history)` | `current: dict`, `history: list` | `classification`, `trend`, `requires_immediate_attention`, `action` | `requires_immediate_attention: true` triggers alert + email |
| 3 | **Health Risk Trend Analysis** | `health_risk_trend_prompt(metrics)` | `metrics: dict` | `glucose_trend`, `cholesterol_trend`, `bmi_trend`, `alerts`, `overall_trend` | Threshold breach messages surfaced in `alerts[]` |
| 4 | **Lifestyle Advisory** | `lifestyle_advisory_prompt(patient)` | `patient: dict` | `diet`, `exercise`, `smoking`, `stress_management`, `medication_adherence`, `priority_action` | Evidence-based (WHO / AHA / NHS) guidelines |
| 5 | **Emergency Symptom Alert** | `emergency_symptom_alert_prompt(symptoms_text)` | `symptoms_text: str` | `urgency`, `matched_warning_signs`, `fast_flags`, `immediate_instruction` | EMERGENCY escalation hardcoded; never downplays |
| 6 | **Hospital Report Summary** | `hospital_report_summary_prompt(report_text, hospital_name)` | `report_text: str`, `hospital_name: str` | `key_diagnoses`, `relevant_medications`, `bp_readings_found`, `cardiovascular_history` | Summarise only — no diagnosis |

All prompts use the `<|system|> … <|user|> … <|assistant|>` chat template required by `ibm/granite-3-8b-instruct`.

---

## Prompt Structure

Every prompt follows this pattern:

```
<|system|>
  Role definition + DISCLAIMER + "Respond ONLY in valid JSON"
<|user|>
  Structured patient / metric data
  Exact JSON schema to return
<|assistant|>
```

The `<|assistant|>` tag at the end is intentionally left empty — it primes the model to continue directly with JSON output.

---

## Safety Design

- **`DISCLAIMER`** constant is injected into the `system` block of every prompt and also returned as a field inside every JSON response, ensuring it survives downstream parsing.
- Agent 2 exposes `requires_immediate_attention: bool` — a hypertensive crisis reading (`≥ 180/120 mmHg`) sets this to `true`, which must trigger an immediate alert and email in the calling service.
- Agent 5 carries a **hard-coded EMERGENCY escalation rule** in its system prompt: any ambiguous symptom that could indicate stroke must be classified as `EMERGENCY`. The model is explicitly instructed never to downplay.
- Agent 6 (Report Summary) is scoped to extraction only — it does not produce risk scores or recommendations, preventing hallucinated diagnoses from unstructured documents.

---

## Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

```
WATSONX_API_KEY=<your IBM Cloud API key>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=746c612f-47a6-4d52-96df-87c9aa25f468
```

---

## Usage Example

```python
from app.services.prompts import stroke_risk_assessment_prompt

patient = {
    "name": "Jane Smith",
    "age": 62,
    "gender": "Female",
    "medical_history": "Type 2 diabetes, atrial fibrillation",
    "bp_systolic": 158,
    "bp_diastolic": 95,
    "blood_glucose": 138,
    "cholesterol": 224,
    "bmi": 29.4,
    "smoking_status": "Former smoker",
    "activity_level": "Sedentary",
}

prompt = stroke_risk_assessment_prompt(patient)
# Pass `prompt` to the watsonx.ai text generation API
```

---

> **Disclaimer:** This system is a health-risk monitoring and decision-support tool ONLY. It is NOT a diagnostic system. Any suspected stroke or brain haemorrhage must be treated as a medical emergency requiring immediate professional care.
