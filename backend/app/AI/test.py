if __name__ == "__main__":
    import os
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent / "dataset"

    if not BASE_DIR.exists():
        print(
            "Dataset not found. Please run the training script to download the dataset."
        )

    print(BASE_DIR)
