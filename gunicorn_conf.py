accesslog = "path/to/gunicorn-access.log" # or None
errorlog = "path/to/gunicorn-error.log" # or None
sendfile = False
daemon = True
bind = "127.0.0.1:8000"
backlog = 2048
workers = 2
threads = 2
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 200
timeout = 30
graceful_timeout = 30
keepalive = 75 # nginx + 10s
