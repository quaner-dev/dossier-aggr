# ---- venv builder ----
FROM python:3.12.3-slim AS venv-builder

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources

COPY requirements.txt .

RUN apt-get update
RUN python3 -m venv /venv
RUN /venv/bin/pip3 install --no-cache-dir --break-system-packages -r requirements.txt
RUN find /venv -type d -name '__pycache__' -exec rm -rf {} +
RUN find /venv -type d -name 'tests' -exec rm -rf {} +

# ---- dev ----
FROM python:3.12.3-slim

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources

WORKDIR /root

COPY --from=venv-builder /venv /venv
COPY . .

ENV PATH="/venv/bin:$PATH"

RUN apt-get update
RUN apt-get install -y --no-install-recommends vim-tiny
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
