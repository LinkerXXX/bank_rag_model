import re

def recursive_chunk(text, max_size, level=0):
    separators = [r'(?<=[.!?]) +', r'\s+']

    if len(text) <= max_size:
        return [text]

    separator = separators[min(level, len(separators) - 1)]
    
    chunks = re.split(separator, text)
    
    if any(len(chunk) > max_size for chunk in chunks):
        new_chunks = []
        for chunk in chunks:
            if len(chunk) > max_size:
                new_chunks.extend(recursive_chunk(chunk, max_size, level + 1))
            else:
                new_chunks.append(chunk)
        return new_chunks
    else:
        return chunks
    