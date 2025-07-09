from colocalization.metrics import calculate_colocalization, save_overlay

image_path = r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\CiliaFormation\RPE\RPE_merged_CH(488, DAPI, 561)_CH.png"
overlay_output = r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\CiliaFormation\RPE\counts\colocMerged_overlay2.png"

result = calculate_colocalization(image_path)
print(result)

save_overlay(image_path, overlay_output)
print(f"Overlay saved to {overlay_output}")
