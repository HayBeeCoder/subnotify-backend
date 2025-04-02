def calculate_duration_in_days(start_timestamp: int, end_timestamp: int) -> int:
    return (end_timestamp - start_timestamp) // 86400
