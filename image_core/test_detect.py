from cilia_detection.detector import detect_cilia

# result = detect_cilia("sampleMerged.png", save_path="outputMerged.png") 
result = detect_cilia(r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\CiliaFormation\RPE\RPE_rgb_CH(561)_CH3.png", 
save_path=r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\CiliaFormation\RPE\counts\Red40.png")
print(result)

