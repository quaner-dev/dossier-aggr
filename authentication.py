import os
from hashlib import md5


from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return Response(
            status_code=401, headers={"WWW-Authenticate": 'Digest realm="My Realm"'}
        )

    # 这里可以根据需要选择不同的认证方式
    if "Digest" in auth_header:
        authenticator = DigestAuthentication()
    else:
        authenticator = SystemAuthentication()

    try:
        user, _ = authenticator.authenticate(request)
        request.state.user = user
    except exceptions.AuthenticationFailed as e:
        return Response(
            status_code=401,
            content=str(e),
            headers={"WWW-Authenticate": authenticator.authenticate_header(request)},
        )

    response = await call_next(request)
    return response
