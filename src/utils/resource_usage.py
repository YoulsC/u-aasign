def get_resource_usage():
    import psutil

    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    return {
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage
    }