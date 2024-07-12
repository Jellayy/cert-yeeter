import os
import ssl
import socket

import OpenSSL

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN


API_KEY_HEADER = APIKeyHeader(name="X-API-Key")
API_KEY, DOMAIN = None, None


def init_app():
    global API_KEY, DOMAIN
    # Load env
    try:
        API_KEY = os.environ['API_KEY']
        DOMAIN = os.environ['DOMAIN_TO_PULL']
    except KeyError:
        raise Exception("'API_KEY' and 'DOMAIN_TO_PULL' variables not provided, exiting...")


config = init_app()
app = FastAPI()


async def get_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )
    return api_key


@app.get("/fingerprint", response_class=PlainTextResponse)
async def fingerprint(api_key: str = Depends(get_api_key)) -> str:
    """
    Returns the formatted (de-coloned and lowercased) SHA1 fingerprint for the server's configured domain

    The perfect endpoint for using with your sock-drawer microcontrollers that can't do simple SSL/TLS and pull certs themselves
    """
    ssl_ctx = ssl.create_default_context()

    with socket.create_connection((DOMAIN, 443)) as sock:
        with ssl_ctx.wrap_socket(sock, server_hostname=DOMAIN) as secure_sock:
            cert = secure_sock.getpeercert(binary_form=True)
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
            sha1_fingerprint = x509.digest("sha1").decode()
            sha1_fingerprint = sha1_fingerprint.replace(":", "").lower()
            return sha1_fingerprint
