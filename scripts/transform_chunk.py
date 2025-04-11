import json
import os
from src.transform import transform_data

def transform_chunk():
    chunk_index = int(os.environ["CHUNK_INDEX"])
    chunk_size = int(os.environ["CHUNK_SIZE"])
    input_path = os.environ["INPUT_PATH"]
    output_path = os.environ["OUTPUT_PATH"].replace(".json", f"_{chunk_index}.json")
    
    # Read input
    with open(input_path, "r") as f:
        laureates = json.load(f)
    
    # Calculate chunk
    start = chunk_index * chunk_size
    end = min(start + chunk_size, len(laureates))
    chunk = laureates[start:end]
    
    # Transform
    transformed = transform_data(chunk)
    
    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(transformed, f)
    print(f"Transformed {len(transformed)} laureates to {output_path}")

if __name__ == "__main__":
    transform_chunk()