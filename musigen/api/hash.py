def decodeUrl(url: str):
    url_data = url.rsplit("-", maxsplit=2)
    bpm = url_data.pop()
    scale = url_data.pop()
    grid_hash = url_data.pop()
    return grid_hash, scale, bpm


def encodeUrl(grid, scale, bpm):
    url = f"{grid}-{scale}-{bpm}"
    return url
