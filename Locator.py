def map(path, stores):
    idx = hash(path) % len(stores)
    return stores[idx]['name']