import os
from pathlib import Path
import random
from PIL import Image, ImageDraw
from tqdm import tqdm

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms

from image_core.dataset import CiliaDataset
from image_core.model import SimpleUNet

# Paths
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "train"
IMAGES_DIR = DATA_DIR / "images"
MASKS_DIR = DATA_DIR / "masks"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
MASKS_DIR.mkdir(parents=True, exist_ok=True)

# --- Dummy Data Generator ---
def generate_dummy_data(num_samples=20, image_size=(256, 256)):
    print("📦 Generating dummy data...")
    for i in range(num_samples):
        img = Image.new("RGB", image_size, color="black")
        mask = Image.new("L", image_size, color=0)
        draw_img = ImageDraw.Draw(img)
        draw_mask = ImageDraw.Draw(mask)

        for _ in range(random.randint(3, 6)):
            x0, y0 = random.randint(0, 200), random.randint(0, 200)
            x1, y1 = x0 + random.randint(20, 40), y0 + random.randint(20, 40)
            intensity = random.randint(100, 255)
            shape_type = random.choice(["ellipse", "rectangle"])

            if shape_type == "ellipse":
                draw_img.ellipse([x0, y0, x1, y1], fill=(intensity, 0, 0))
                draw_mask.ellipse([x0, y0, x1, y1], fill=255)
            else:
                draw_img.rectangle([x0, y0, x1, y1], fill=(0, intensity, 0))
                draw_mask.rectangle([x0, y0, x1, y1], fill=255)

        img.save(IMAGES_DIR / f"sample_{i}.png")
        mask.save(MASKS_DIR / f"sample_{i}_mask.png")

# --- Train Loop ---
def train():
    if not list(IMAGES_DIR.glob("*.png")):
        generate_dummy_data()

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])

    dataset = CiliaDataset(image_dir=IMAGES_DIR, mask_dir=MASKS_DIR, transform=transform)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    # Use GPU if available, else fallback to CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleUNet().to(device)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    print("🚀 Starting training...")
    for epoch in range(10):
        model.train()
        total_loss = 0.0

        for img, mask in tqdm(dataloader, desc=f"Epoch {epoch+1}"):
            img, mask = img.to(device), mask.to(device)
            

            out = model(img)
            loss = criterion(out, mask)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"✅ Epoch {epoch+1} completed | Loss: {total_loss / len(dataloader):.4f}")

    # Save trained model
    checkpoint_path = Path("image_core/checkpoints/unet_cilia.pt")
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), checkpoint_path)
    print(f"💾 Model saved to {checkpoint_path}")

if __name__ == "__main__":
    train()
