import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights
from datasets import load_dataset
from sklearn.model_selection import train_test_split
import os
import numpy as np
from PIL import Image

def train_cv_model():
    """
    Fine-tunes a pre-trained ResNet50 model on the vehicle damage dataset.
    """
    # --- 1. Setup and Configuration ---
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    model_save_path = os.path.join(models_dir, 'cv_resnet50_model.pth')

    # --- 2. Load and Preprocess Dataset ---
    print("Loading dataset from Hugging Face...")
    dataset = load_dataset("ikuldeep1/vehicle-damage-fraud-image-balanced", split="train")
    
    # Split dataset into train and validation sets
    train_dataset, val_dataset = dataset.train_test_split(test_size=0.2).values()

    # Define transformations
    preprocess = transforms.Compose([
        transforms.Lambda(lambda x: x.convert('RGB')), # Ensure 3 channels
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    def apply_transforms(batch):
        batch['pixel_values'] = [preprocess(image) for image in batch['image']]
        return batch

    train_dataset.set_transform(apply_transforms)
    val_dataset.set_transform(apply_transforms)

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, collate_fn=lambda x: {'pixel_values': torch.stack([i['pixel_values'] for i in x]), 'label': torch.tensor([i['label'] for i in x])})
    val_loader = DataLoader(val_dataset, batch_size=32, collate_fn=lambda x: {'pixel_values': torch.stack([i['pixel_values'] for i in x]), 'label': torch.tensor([i['label'] for i in x])})
    
    print("Data loading and preprocessing complete.")

    # --- 3. Model Definition ---
    print("Setting up ResNet50 model for fine-tuning...")
    model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    
    # Freeze all the parameters in the pre-trained model
    for param in model.parameters():
        param.requires_grad = False
        
    # Replace the final fully connected layer
    num_ftrs = model.fc.in_features
    num_classes = len(dataset.features['label'].names)
    model.fc = nn.Linear(num_ftrs, num_classes)

    model = model.to(device)
    print(f"Model loaded on {device}. Number of classes: {num_classes}")

    # --- 4. Training ---
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=0.001) # Only train the new layer

    num_epochs = 5
    best_val_accuracy = 0.0

    print("Starting model training...")
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        for batch in train_loader:
            inputs = batch['pixel_values'].to(device)
            labels = batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)

        epoch_loss = running_loss / len(train_loader.dataset)

        # Validation phase
        model.eval()
        val_running_loss = 0.0
        corrects = 0
        with torch.no_grad():
            for batch in val_loader:
                inputs = batch['pixel_values'].to(device)
                labels = batch['label'].to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                _, preds = torch.max(outputs, 1)
                val_running_loss += loss.item() * inputs.size(0)
                corrects += torch.sum(preds == labels.data)

        val_epoch_loss = val_running_loss / len(val_loader.dataset)
        val_epoch_acc = corrects.double() / len(val_loader.dataset)

        print(f"Epoch {epoch+1}/{num_epochs} | Train Loss: {epoch_loss:.4f} | Val Loss: {val_epoch_loss:.4f} | Val Acc: {val_epoch_acc:.4f}")

        # Save the best model
        if val_epoch_acc > best_val_accuracy:
            best_val_accuracy = val_epoch_acc
            torch.save(model.state_dict(), model_save_path)
            print(f"Best model saved to {model_save_path} with accuracy: {best_val_accuracy:.4f}")

    print("Training complete.")

if __name__ == '__main__':
    train_cv_model()
