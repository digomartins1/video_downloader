def format_bytes(size_bytes: int | float | None) -> str:
    """Converte bytes para formato legível (KB, MB, GB)."""
    if not size_bytes:
        return "Desconhecido"
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def format_duration(seconds: int | float | None) -> str:
    """Converte segundos para HH:MM:SS ou MM:SS."""
    if not seconds:
        return "00:00"
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{sec:02d}"
    return f"{minutes:02d}:{sec:02d}"