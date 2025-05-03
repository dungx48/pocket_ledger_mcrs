# FROM python:3.9-slim-bookworm

# # timezone
# ENV TZ=Asia/Ho_Chi_Minh
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
#   && echo $TZ > /etc/timezone

# # install system deps
# RUN apt-get update \
#  && apt-get install -y --no-install-recommends \
#       curl ca-certificates build-essential libpq-dev libssl-dev libffi-dev gcc \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/*

# # install uv (package manager)
# ADD https://astral.sh/uv/install.sh /uv-installer.sh
# RUN sh /uv-installer.sh && rm /uv-installer.sh

# ENV PATH="/root/.local/bin/:$PATH"

# WORKDIR /app
# COPY . /app

# RUN uv sync --frozen && pip install --no-cache-dir uvicorn[standard]

# # mở port và chạy uvicorn
# EXPOSE 8001
# CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]


# 1. Chọn base image
FROM python:3.9-slim-bookworm

# 2. Thiết timezone
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && echo $TZ > /etc/timezone

# 3. Cài tool hệ thống
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential gcc libpq-dev libssl-dev libffi-dev curl ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# 4. Nâng pip, copy file requirements
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ source
COPY . /app

# 6. Expose port và CMD
EXPOSE 8001
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
