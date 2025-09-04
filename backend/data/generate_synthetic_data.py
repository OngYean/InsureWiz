import pandas as pd
import numpy as np
from datasets import load_dataset
import os

def generate_synthetic_data():
    """
    Generates a synthetic motor insurance claim dataset by combining tabular data
    with an image dataset from Hugging Face.
    """
    print("Loading Hugging Face dataset metadata...")
    # 1. Load the Hugging Face dataset
    try:
        dataset = load_dataset("ikuldeep1/vehicle-damage-fraud-image-balanced", split="train")
        num_rows = len(dataset)
        print(f"Successfully loaded dataset with {num_rows} rows.")
    except Exception as e:
        print(f"Failed to load dataset. Error: {e}")
        return

    # Create a DataFrame from the Hugging Face dataset
    hf_df = dataset.to_pandas()

    # The 'label' column is a ClassLabel with integer values. Let's get the names.
    label_names = dataset.features['label'].names
    hf_df['label_text'] = hf_df['label'].apply(lambda x: label_names[x])

    print("Generating synthetic tabular data...")
    # 2. Generate synthetic tabular data
    data = {
        # Incident Details
        'incidentType': np.random.choice(['Collision', 'Theft', 'Vandalism', 'Natural Disaster', 'Fire'], num_rows),
        'timeOfDay': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], num_rows),
        'roadConditions': np.random.choice(['Dry', 'Wet', 'Construction Zone', 'Poor Visibility'], num_rows),
        'weatherConditions': np.random.choice(['Clear', 'Rain', 'Heavy Rain', 'Fog'], num_rows),
        'injuries': np.random.choice(['no', 'yes'], num_rows, p=[0.9, 0.1]),

        # Vehicle & Documentation
        'thirdPartyVehicle': np.random.choice(['no', 'yes'], num_rows, p=[0.6, 0.4]),
        'witnesses': np.random.choice(['no', 'yes'], num_rows, p=[0.7, 0.3]),
        'policeReport': np.random.choice(['no', 'yes'], num_rows, p=[0.2, 0.8]),
        'description': ['A brief description of the incident.' for _ in range(num_rows)],

        # High-weight features
        'policeReportFiledWithin24h': np.random.choice([0, 1], num_rows, p=[0.3, 0.7]),
        'trafficViolation': np.random.choice([0, 1], num_rows, p=[0.85, 0.15]),
        'previousClaims': np.random.choice([0, 1, 2, 3], num_rows, p=[0.7, 0.15, 0.1, 0.05]),
    }
    
    synthetic_df = pd.DataFrame(data)

    # Map vehicleDamage from the dataset's label
    synthetic_df['vehicleDamage'] = hf_df['label_text'].apply(lambda x: 'no-damage' if x == 'no_damage' else ('major-damage' if x == 'damage' else 'fraud-related-damage'))

    print("Calculating claim_success score with weighted factors...")
    # 3. Create claim_success label with weighted logic
    # Start with a base score
    score = np.zeros(num_rows)

    # Apply weights based on your criteria
    # Positive factors
    score += synthetic_df['policeReportFiledWithin24h'] * 25  # High positive weight

    # Negative factors
    score -= synthetic_df['trafficViolation'] * 30  # High negative weight
    score -= synthetic_df['previousClaims'] * 15   # Medium negative weight for each previous claim
    
    # Incorporate fraud label from image dataset with very high negative weight
    is_fraud = (hf_df['label_text'] == 'fraud').astype(int)
    score -= is_fraud * 50

    # Add some noise to make it more realistic
    score += np.random.normal(0, 5, num_rows)

    # Determine success based on a score threshold
    threshold = np.percentile(score, 25) # Approve ~75% of claims
    claim_success = (score > threshold).astype(int)

    synthetic_df['claim_success'] = claim_success
    
    print("Combining datasets...")
    # 4. Combine the datasets
    final_df = pd.concat([
        hf_df[['label_text']].rename(columns={'label_text': 'image_label'}),
        synthetic_df
    ], axis=1)
    
    # Add a placeholder for the image
    final_df.insert(0, 'image_id', range(len(final_df)))


    # Reorder columns for clarity
    final_df = final_df[[
        'image_id', 'image_label', 'claim_success', 'incidentType', 'timeOfDay',
        'roadConditions', 'weatherConditions', 'injuries', 'vehicleDamage',
        'thirdPartyVehicle', 'witnesses', 'policeReport', 'policeReportFiledWithin24h',
        'trafficViolation', 'previousClaims', 'description'
    ]]

    # 5. Save to CSV
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'synthetic_claims_data.csv')
    final_df.to_csv(output_path, index=False)

    print(f"Successfully generated synthetic data and saved to {output_path}")
    print("\n--- Data Sample ---")
    print(final_df.head())
    print("\n--- Claim Success Distribution ---")
    print(final_df['claim_success'].value_counts(normalize=True))


if __name__ == '__main__':
    generate_synthetic_data()
