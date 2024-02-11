import re

def get_server_info(response):
    server_type = None
    if re.search(r"Express", response, re.IGNORECASE):
        server_type = "Express"
    elif re.search(r"PHP", response, re.IGNORECASE):
        server_type = "PHP"
    elif re.search(r"<!DOCTYPE html>", response):
        server_type = "HTML"
    elif re.search(r"Server: Python", response, re.IGNORECASE):
        server_type = "Python"
    elif "X-Powered-By" in response:
        server_type = "Nginx"
    elif re.search(r"Apache", response, re.IGNORECASE):
        server_type = "Apache"
    elif re.search(r"Microsoft-IIS", response):
        server_type = "Microsoft IIS"
    elif re.search(r"LiteSpeed", response):
        server_type = "LiteSpeed"
    elif re.search(r"Cherokee", response, re.IGNORECASE):
        server_type = "Cherokee"
    elif re.search(r"lighttpd", response, re.IGNORECASE):
        server_type = "lighttpd"
    else:
        server_type = "Unknown"

    return server_type