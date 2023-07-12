def find_matches(chunks, keywords, padding=500):
    df = {}
    results = {}

    trimmed_chunks = []
    for i, chunk in enumerate(chunks):
        if i != 0:
            chunk = chunk[padding:]
        if i != len(chunks)-1:
            chunk = chunk[:-padding]
        trimmed_chunks.append(chunk.lower())

    for chunk in trimmed_chunks:
        for keyword in keywords:
            occurences = chunk.count(keyword)
            if keyword not in df:
                df[keyword] = 0
            df[keyword] += occurences

    for chunk_id, chunk in enumerate(trimmed_chunks):
        points = 0
        for keyword in keywords:
            occurences = chunk.count(keyword)
            if df[keyword] > 0:
                points += occurences / df[keyword]
        results[chunk_id] = points

    return dict(sorted(results.items(), key=lambda item: item[1], reverse=True))