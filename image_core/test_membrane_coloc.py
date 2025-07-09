from colocalization.membrane_coloc import calculate_membrane_cytoplasm_colocalization

# File paths
red_path = r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\WebImages\redMulti.png"
green_path = r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\WebImages\greenMulti.png"

# Optional manual mask (set to None if not using)
manual_mask_path = None # r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\WebImages\manual_mask.png" 
# If no manual mask is available, use: manual_mask_path = None

# Run analysis
result = calculate_membrane_cytoplasm_colocalization(
    red_path=red_path,
    green_path=green_path,
    manual_membrane_mask_path= manual_mask_path, # Can be None to use auto-detection
    membrane_thickness=5  # Only used if manual mask is not provided
)

# Output result
print(result)
