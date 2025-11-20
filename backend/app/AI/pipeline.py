from transformers import pipeline as hf_pipeline
from typing import Optional, Any


_pipe: Optional[Any] = None


def get_pipe() -> Any:
    """Return a singleton image-classification pipeline instance.

    The pipeline is created on first call to avoid heavy work at import time.
    """
    global _pipe
    if _pipe is None:
        _pipe = hf_pipeline(
            "image-classification",
            model="yangy50/garbage-classification",
            use_fast=True,
        )
    return _pipe
