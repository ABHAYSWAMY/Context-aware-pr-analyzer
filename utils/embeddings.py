import os
import threading
from typing import Iterable, List

from sentence_transformers import SentenceTransformer

# Lazy-loaded singleton model to avoid downloading at import time (helps HF deploys)
_model: SentenceTransformer | None = None
_model_lock = threading.Lock()
_encode_lock = threading.Lock()


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                model_name = os.environ.get("EMBED_MODEL", "all-MiniLM-L6-v2")
                hf_token = os.environ.get("HF_TOKEN")
                kwargs = {}
                if hf_token:
                    kwargs["use_auth_token"] = hf_token
                _model = SentenceTransformer(model_name, **kwargs)
    return _model


def embed_texts(texts: Iterable[str]) -> List[float]:
    """Embed a list of texts.

    Model is loaded on first use. Set `EMBED_MODEL` or `HF_TOKEN` via
    environment variables if you need a different model or an authenticated HF download.
    """
    model = _get_model()
    with _encode_lock:
        return model.encode(list(texts), show_progress_bar=False)