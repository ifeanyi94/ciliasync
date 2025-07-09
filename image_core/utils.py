import numpy as np

def dice_score(pred, target, eps=1e-7):
    intersection = np.sum(pred * target)
    union = np.sum(pred) + np.sum(target)
    return (2. * intersection + eps) / (union + eps)

def iou_score(pred, target, eps=1e-7):
    intersection = np.sum(pred * target)
    union = np.sum(pred + target) - intersection
    return (intersection + eps) / (union + eps)
