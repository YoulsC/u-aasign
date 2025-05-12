def get_active_processes():
    import psutil
    return [proc.info for proc in psutil.process_iter(attrs=['pid', 'name', 'status'])]