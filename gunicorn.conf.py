port = 80
bind = f"0.0.0.0:{port}"
workers=4
accesslog = "./log/access_log.log"
errorlog = "./log/error_log.log"
worker_class = 'uvicorn.workers.UvicornWorker'
#certfile="/etc/letsencrypt/live/api.dogcoolcodefair.com/fullchain.pem"
#keyfile="/etc/letsencrypt/live/api.dogcoolcodefair.com/privkey.pem"