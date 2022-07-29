import uvicorn
from dotenv import load_dotenv
load_dotenv()
from os import getenv
uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True, ssl_certfile=getenv("ssl_key_path"), ssl_keyfile=getenv("ssl_key_path"))
