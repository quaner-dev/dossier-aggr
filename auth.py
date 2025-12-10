from hashlib import md5
from typing import Optional, Dict

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPDigest, utils
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


class HTTPDigest1400(HTTPDigest):
    scheme_name = "Digest"

    realm = "VIID API"
    nonce = "12345"
    algorithm = "MD5"
    qop = "auth"
    opaque = "123456789"

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = utils.get_authorization_scheme_param(authorization)

        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                    headers={
                        "WWW-Authenticate": f'Digest realm="{self.realm}", nonce="{self.nonce}", algorithm="{self.algorithm}", qop="{self.qop}", opaque="{self.opaque}"'
                    },
                )
            else:
                return None

        if scheme.lower() != "digest":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme",
                )
            else:
                return None

        # 摘要认证算法
        params: Dict[str, str] = {}
        for credential in credentials.split(", "):
            key, value = credential.split("=", 1)
            params[key] = value.strip('"')

        password = "admin"
        ha1 = md5(f"{params["username"]}:{self.realm}:{password}".encode()).hexdigest()
        ha2 = md5(f"{request.method}:{params["uri"]}".encode()).hexdigest()
        expected = md5(
            f"{ha1}:{self.nonce}:{params["nc"]}:{params["cnonce"]}:{self.qop}:{ha2}".encode()
        ).hexdigest()

        if params["response"] != expected:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid digest response"
            )

        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
