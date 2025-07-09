# backend/cilia_cli_runner.py

import subprocess
import json
import uuid
import os
import tempfile

def run_csharp_analysis(image_path):
    # Use system temp directory (e.g., C:\Users\<user>\AppData\Local\Temp on Windows)
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}.json")

    # Path to the compiled C# executable
    exe_path = os.path.abspath("ciliasync_cli/publish/image-core.exe")

    print(f"Executing: {[exe_path, image_path, output_path]}")
    print(f"Does exe_path exist? {os.path.exists(exe_path)}")

    result = subprocess.run(
        [exe_path, image_path, output_path],
        capture_output=True,
        text=True
    )

    # Log stdout and stderr for debugging
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        raise RuntimeError("C# CLI failed")

    with open(output_path) as f:
        data = json.load(f)

    os.remove(output_path)
    return data
