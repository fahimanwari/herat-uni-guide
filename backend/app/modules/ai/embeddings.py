_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("intfloat/multilingual-e5-small")
    return _model


def embed_query(text: str) -> list[float]:
    return get_model().encode(f"query: {text}", normalize_embeddings=True).tolist()


def embed_passage(text: str) -> list[float]:
    return get_model().encode(f"passage: {text}", normalize_embeddings=True).tolist()
