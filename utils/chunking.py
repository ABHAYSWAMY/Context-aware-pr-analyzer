def chunk_text(text, size=1500):
    """
    Splits text into fixed-size chunks
    """
    return [text[i:i+size] for i in range(0, len(text), size)]