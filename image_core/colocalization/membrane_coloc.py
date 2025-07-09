import cv2
import numpy as np
import os
import csv

def calculate_membrane_cytoplasm_colocalization(
    red_path,
    green_path,
    manual_membrane_mask_path=None,
    membrane_thickness=3
):
    red_img = cv2.imread(red_path, cv2.IMREAD_GRAYSCALE)
    green_img = cv2.imread(green_path, cv2.IMREAD_GRAYSCALE)

    if red_img is None or green_img is None:
        raise ValueError("One or both input images could not be loaded.")

    if red_img.shape != green_img.shape:
        green_img = cv2.resize(green_img, (red_img.shape[1], red_img.shape[0]))

    combined = cv2.addWeighted(red_img, 0.5, green_img, 0.5, 0)
    _, cell_mask = cv2.threshold(combined, 1, 255, cv2.THRESH_BINARY)

    debug_dir = os.path.join(os.path.dirname(__file__), "..", "mask_debugImgs")
    os.makedirs(debug_dir, exist_ok=True)
    cv2.imwrite(os.path.join(debug_dir, "cell_mask_debug.png"), cell_mask)

    num_labels, labels = cv2.connectedComponents(cell_mask)
    pearson_mem_list = []
    pearson_cyto_list = []
    enrichment_list = []

    saved_debug = False

    for label in range(1, num_labels):
        cell = (labels == label).astype(np.uint8) * 255

        if manual_membrane_mask_path:
            membrane_mask_img = cv2.imread(manual_membrane_mask_path, cv2.IMREAD_GRAYSCALE)
            if membrane_mask_img is None:
                raise ValueError("Manual membrane mask could not be loaded.")
            if membrane_mask_img.shape != red_img.shape:
                membrane_mask_img = cv2.resize(membrane_mask_img, (red_img.shape[1], red_img.shape[0]))
            membrane = ((membrane_mask_img > 0) & (cell > 0)).astype(np.uint8)
            cytoplasm = ((cell // 255) - membrane).clip(min=0)
        else:
            kernel = np.ones((3, 3), np.uint8)
            eroded = cv2.erode(cell, kernel, iterations=membrane_thickness)
            membrane = cv2.subtract(cell, eroded) // 255
            cytoplasm = eroded // 255

        red = (red_img - np.mean(red_img)) / np.std(red_img)
        green = (green_img - np.mean(green_img)) / np.std(green_img)

        try:
            mem_vals = red[membrane > 0], green[membrane > 0]
            cyto_vals = red[cytoplasm > 0], green[cytoplasm > 0]
            if len(mem_vals[0]) < 10 or len(cyto_vals[0]) < 10:
                continue

            pearson_membrane = np.corrcoef(*mem_vals)[0, 1]
            pearson_cytoplasm = np.corrcoef(*cyto_vals)[0, 1]
            enrichment_score = pearson_membrane / (pearson_cytoplasm + 1e-5)

            pearson_mem_list.append(pearson_membrane)
            pearson_cyto_list.append(pearson_cytoplasm)
            enrichment_list.append(enrichment_score)

            if not saved_debug:
                cv2.imwrite(os.path.join(debug_dir, "membrane_mask_debug.png"), membrane * 255)
                cv2.imwrite(os.path.join(debug_dir, "cytoplasm_mask_debug.png"), cytoplasm * 255)
                saved_debug = True

        except Exception:
            continue

    csv_path = os.path.join(debug_dir, "per_cell_results.csv")
    with open(csv_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Cell Index", "Pearson Membrane", "Pearson Cytoplasm", "Enrichment Score"])
        for i, (pm, pc, es) in enumerate(zip(pearson_mem_list, pearson_cyto_list, enrichment_list)):
            writer.writerow([i + 1, round(pm, 3), round(pc, 3), round(es, 3)])

    return {
        "avg_pearson_membrane": round(np.mean(pearson_mem_list), 3) if pearson_mem_list else None,
        "avg_pearson_cytoplasm": round(np.mean(pearson_cyto_list), 3) if pearson_cyto_list else None,
        "avg_membrane_enrichment_score": round(np.mean(enrichment_list), 3) if enrichment_list else None
    }
