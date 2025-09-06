# Motor Insurance Claim Success Prediction Model

## 1. Input Weighting Strategy

Assign weights based on how strongly each factor influences claim success (from Malaysian insurance guidelines and expert knowledge):

| Input                    | Weight (Example) | Reasoning/Impact                                    |
| ------------------------ | ---------------- | --------------------------------------------------- |
| Police report filed      | High (+15)       | Mandatory for most claims, strong positive impact   |
| Police report within 24h | High (+10)       | Timeliness increases approval chance                |
| Photo/document evidence  | Medium (+10)     | Supports claim validity                             |
| Witness statements       | Medium (+8)      | Corroborates incident details                       |
| At fault                 | Negative (-15)   | Being at fault reduces success probability          |
| Traffic violation        | Negative (-18)   | Violations often lead to rejection                  |
| NCD active               | Small (+5)       | Indicates good claim history                        |
| Coverage type            | Medium (+10)     | Comprehensive covers more scenarios                 |
| Vehicle age              | Small            | Older vehicles may have more scrutiny               |
| Previous claims          | Negative         | Multiple claims may raise suspicion                 |
| Damage extent/cost       | Neutral/Context  | Major damage may require more evidence              |
| Incident type            | Contextual       | Some types (theft, fire) have stricter requirements |
| Policy document provided | Medium (+10)     | Verifies coverage and terms                         |
| Road/weather conditions  | Contextual       | May affect fault determination                      |

You can start with these weights and adjust based on data analysis.

---

## 2. Model Training Approach

### A. Data Preparation

- **Label**: Success (approved) or failure (rejected) for each claim.
- **Features**: All form inputs, encoded numerically (e.g., yes/no → 1/0, categorical → one-hot).
- **Document/Evidence**: Use a binary feature for presence, or extract features using OCR/CV if possible.

### B. Model Choice

- **Tabular Data**: Logistic Regression, Random Forest, Gradient Boosted Trees (e.g., XGBoost, LightGBM).
- **Document Analysis**: If you want to analyze PDFs/images, use a separate CV/NLP pipeline to extract features (e.g., document type, keywords, image classification).

### C. Training Steps

1. **Collect historical claim data** with all relevant features and outcomes.
2. **Preprocess**: Clean, encode, and normalize data.
3. **Split**: Train/test split (e.g., 80/20).
4. **Train**: Fit the model, using feature importance to refine weights.
5. **Evaluate**: Use accuracy, precision, recall, ROC-AUC.
6. **Tune**: Adjust weights/features based on model feedback.

### D. Example (Python, scikit-learn)

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load and preprocess your data
df = pd.read_csv("claims_data.csv")
X = df.drop("claim_success", axis=1)  # Features
y = df["claim_success"]               # Label

# Encode categorical features, scale, etc.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(class_weight="balanced")
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Feature importance
importances = model.feature_importances_
for feature, importance in zip(X.columns, importances):
    print(f"{feature}: {importance:.2f}")
```

### E. Continuous Improvement

- Retrain with new data.
- Use feedback from real claims to adjust weights and improve accuracy.

---

**Summary:**

- Assign weights based on regulatory importance and historical impact.
- Train a tabular ML model with encoded features.
- Optionally, use CV/NLP for document/image analysis.
- Continuously refine with new data and feedback.
