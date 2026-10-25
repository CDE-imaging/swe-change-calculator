# 📋 Liver SWE Change Calculator

**A research-based calculator for assessing longitudinal liver stiffness changes after Kasai portoenterostomy (KPE), accounting for ultrasound system and transducer variability.**

This Streamlit application was developed based on a study of shear wave elastography (SWE) measurement variability in pediatric patients after KPE. It estimates the equipment-adjusted change between baseline and follow-up liver stiffness measurements and compares that change with the study-derived **minimal detectable change at the 95% confidence level (MDC95) of 4.41 kPa**.

> **Research use only.** This calculator is a research prototype and has not been externally validated for clinical decision-making.

## ✨ Features

- Enter baseline and follow-up liver stiffness measurements (kPa), ultrasound systems, and transducer types.
- Calculate the observed SWE change, estimated equipment-related bias, and bias-adjusted SWE change.
- Visualize the adjusted change relative to the study-derived MDC95 limits (±4.41 kPa).
- Review the model coefficients and interpretation limitations within the app.

## 🧮 Calculation methodology

The observed longitudinal change is calculated as:

$$
\Delta_{\mathrm{observed}} = SWE_{\mathrm{followup}} - SWE_{\mathrm{baseline}}
$$

The estimated equipment-related bias is the difference between the fitted effects for the follow-up and baseline system–transducer combinations:

$$
\Delta_{\mathrm{equipment}} = \beta_{\mathrm{followup}} - \beta_{\mathrm{baseline}}
$$

The **bias-adjusted longitudinal change** is:

$$
\boxed{\Delta_{\mathrm{adjusted}} = (SWE_{\mathrm{followup}} - SWE_{\mathrm{baseline}}) - (\beta_{\mathrm{followup}} - \beta_{\mathrm{baseline}})}
$$

### 📊 Model-estimated equipment effects

All estimates are relative to **GE with a curvilinear transducer** (reference category).

| Ultrasound system | Transducer | Estimated mean difference (kPa) | 95% CI (kPa) | p-value |
|---|---|---:|---|---:|
| GE | Curvilinear | Reference (0.00) | — | — |
| GE | Linear | +2.14 | +1.33 to +2.95 | <0.001 |
| Siemens | Curvilinear | −2.72 | −3.03 to −2.42 | <0.001 |
| SuperSonic | Curvilinear | −0.42 | −0.75 to −0.09 | 0.014 |
| SuperSonic | Linear | +0.48† | −0.13 to +1.09 | 0.12 |

† Derived estimate incorporating the vendor–transducer interaction.

### 📏 Interpretation using MDC95

The study-derived **MDC95 is 4.41 kPa**. The calculator compares the absolute magnitude of the bias-adjusted change with this threshold:

- **|Adjusted change| ≤ 4.41 kPa:** The change is within estimated measurement variability. A true longitudinal change cannot be reliably distinguished from measurement variability using this threshold.
- **|Adjusted change| > 4.41 kPa:** The change exceeds estimated measurement variability. This does **not** necessarily indicate fibrosis progression or regression.

The sign of the adjusted change indicates direction: a negative value represents decreased measured stiffness, while a positive value represents increased measured stiffness after accounting for estimated equipment bias.

## ⚠️ Important limitations

1. **Research use only:** This calculator is a research prototype and has not been externally validated for clinical decision-making. Results should not be used in isolation to guide patient management.
2. **Measurement range:** The adjustment coefficients and MDC95 were derived from SWE measurements **≤15 kPa**. Applicability to measurements above 15 kPa has not been established.
3. **Equipment applicability:** The coefficients were derived from only five system–transducer combinations: **GE C1–6, GE L2–9, Siemens 9C2, SuperSonic XC6–1, and SuperSonic SL10–2**. Results should not be generalized to other combinations without validation.

Liver stiffness is not a fibrosis-specific measure. Changes in stiffness may reflect factors other than fibrosis, including inflammation, cholestasis, and hepatic congestion. Interpret longitudinal SWE changes together with clinical findings, laboratory results, and other imaging features.

## 💻 Run locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the app:

```bash
python -m streamlit run app.py
```

## 📚 Study reference

**Publication pending.** Study-derived model estimates and MDC95 should be checked against the final publication before citation or reuse.

## 🏥 Affiliation

Department of Radiology, Severance Hospital, Yonsei University College of Medicine.

---

*Liver SWE Change Calculator · v0.3 · Research use only*
