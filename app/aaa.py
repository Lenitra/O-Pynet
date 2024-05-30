def format_size(size):
    # Convertir la taille en octets en kilo-octets, méga-octets, etc.
    power = 2**10
    n = 0
    power_labels = {0: 'o', 1: 'Ko', 2: 'Mo', 3: 'Go', 4: 'To'}
    while size > power:
        size /= power
        n += 1
    return f'{size:.2f} {power_labels[n]}'