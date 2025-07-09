import torch 
import matplotlib.pyplot as plt
from torchvision import transforms
from torch.utils.data import DataLoader

from image_core.dataset import CiliaDataset
from image_core.model import SimpleUNet

from pathlib import Path

# Paths
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "train"
IMAGES_DIR = DATA_DIR / "images"
MASKS_DIR = DATA_DIR / "masks"
CHECKPOINT_PATH = Path("image_core/checkpoints/unet_cilia.pt")

# Transform
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

# Dataset and loader
dataset = CiliaDataset(image_dir=IMAGES_DIR, mask_dir=MASKS_DIR, transform=transform)
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleUNet().to(device)
model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=device))
model.eval()

# Visualize a few predictions
def show_prediction():
    with torch.no_grad():
        for i, (img, mask) in enumerate(dataloader):
            if i == 5:  # show 5 samples max
                break

            img = img.to(device)
            pred = model(img)
            pred = pred.squeeze().cpu().numpy()
            pred_bin = (pred > 0.5).astype(float)  # threshold to binary

            img = img.squeeze().permute(1, 2, 0).cpu().numpy()
            mask = mask.squeeze().cpu().numpy()

            fig, axes = plt.subplots(1, 3, figsize=(12, 4))
            axes[0].imshow(img)
            axes[0].set_title("Input Image")
            axes[0].axis("off")

            axes[1].imshow(pred_bin, cmap="gray")
            axes[1].set_title("Predicted Mask (binary)")
            axes[1].axis("off")

            axes[2].imshow(mask, cmap="gray")
            axes[2].set_title("Ground Truth Mask")
            axes[2].axis("off")

            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    show_prediction()
