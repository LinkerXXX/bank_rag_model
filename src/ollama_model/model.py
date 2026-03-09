import ollama

# model = 'mxbai-embed-large'
# promt = 'data'
def ollama_embed(model_ollama, promt):
    result = ollama.embed(model=model_ollama, input=promt)
    print(len(result["embeddings"][0]))
    return result["embeddings"][0]