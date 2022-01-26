def decodeUrl(url: str):
    url_data = url.split("-")
    bpm = url_data.pop()
    scale = url_data.pop()
    grid = [int(row, 16) for row in url_data]
    return grid, scale, bpm


def encodeUrl(grid, scale, bpm):
    grid = [hex(row)[2:] for row in grid]
    url = "-".join(map(str, grid))
    url += f"-{scale}-{bpm}"
    return url
