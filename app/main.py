
import os, uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from gcash import generate_qrcode
from utils import generate_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins       = ["*"],
    allow_credentials   = True,
    allow_methods       = ["*"],
    allow_headers       = ["*"],
)

if __name__ == '__main__':
    params = dict(
        app                 = "main:app",
        host                = "0.0.0.0",
        port                = 8000,
        reload              = True,
        proxy_headers       = True,
        forwarded_allow_ips = '*',
        timeout_keep_alive  = 1000,
    )

    uvicorn.run(**params)

@app.get("/gcash")
def generate_gcash_qrcode(amount: float):
    return HTMLResponse(
        content = generate_html(
            file = 'gcash.html',
            data = generate_qrcode(amount),
            path = './app/gcash'
        )
    )

@app.get("/gcash/file/{file}")
def get_file(file: str):
    return FileResponse(f"app/gcash/{file}")
