import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import numpy as np

def train_and_evaluate_models():
    """
    Loads the synthetic claims data, preprocesses it, and trains three different
    regression models to predict the success rate: Linear Regression, Random Forest,
    and LightGBM. The trained models are saved to the 'models' directory.
    """
    # 1. Load Data
    try:
        data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'synthetic_claims_data.csv')
        df = pd.read_csv(data_path)
        print("Dataset loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The file was not found at {data_path}")
        return

    # 2. Define Features and Target
    features = [col for col in df.columns if col not in ['success_rate', 'image_id', 'description']]
    target = 'success_rate'

    X = df[features]
    y = df[target]

    # Identify categorical features for one-hot encoding
    categorical_features = X.select_dtypes(include=['object']).columns
    
    # 3. Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough' # Keep numerical columns as they are
    )

    # 4. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

    # 5. Define Models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(random_state=42),
        "LightGBM Regressor": lgb.LGBMRegressor(random_state=42)
    }

    # Create directory to save models
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)

    # 6. Train, Evaluate, and Save Models
    for name, model in models.items():
        print(f"\n--- Training {name} ---")

        # Create pipeline
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('regressor', model)])

        # Train model
        pipeline.fit(X_train, y_train)
        print("Model training complete.")

        # Make predictions
        y_pred = pipeline.predict(X_test)

        # Evaluate model
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        print(f"Evaluation Metrics for {name}:")
        print(f"  Mean Squared Error (MSE): {mse:.4f}")
        print(f"  Root Mean Squared Error (RMSE): {rmse:.4f}")
        print(f"  R-squared (R²): {r2:.4f}")

        # Save model
        model_filename = os.path.join(models_dir, f"{name.lower().replace(' ', '_')}_pipeline.joblib")
        joblib.dump(pipeline, model_filename)
        print(f"Model saved to {model_filename}")

if __name__ == '__main__':
    train_and_evaluate_models()
