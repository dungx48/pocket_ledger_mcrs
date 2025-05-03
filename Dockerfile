FROM python:3.9-slim-bookworm

# timezone
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && echo $TZ > /etc/timezone

# install system deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl ca-certificates build-essential libpq-dev libssl-dev libffi-dev gcc \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# install uv (package manager)
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# 1. copy deps và cài
COPY requirements.txt /app/requirements.txt
RUN uv sync --frozen

# 2. copy code
COPY . /app

# mở port và chạy uvicorn
EXPOSE 8001
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
