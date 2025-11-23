from pathlib import Path
from transformers import pipeline
from typing import Optional, Any, TypeAlias

Pipe: TypeAlias = Any

# Singleton holder for the pipeline instance
_pipe: Optional[Pipe] = None


def get_pipe() -> Pipe:
    """Return a singleton image-classification pipeline instance.

    The pipeline loads lazily from the local model directory.
    """
    global _pipe
    if _pipe is None:
        model_dir = Path(__file__).resolve().parent / "model"
        _pipe = pipeline(
            task="image-classification",
            model=str(model_dir),
        )
    return _pipe
