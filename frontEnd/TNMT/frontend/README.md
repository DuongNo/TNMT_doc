# Hướng dẫn

1. Sửa lại file Dockerfile

- ARG VITE_SERVER_PORT=2666 port backend <default : 2601>

2. Sửa lại port trong file docker-compose.yml

- 3000 : port frontend expose <default: 3000>

chạy `docker-compose up ` thì sau khi chạy xong sẽ truy cập frontend tại địa chỉ: http://<server-ip>:<port frontend expose>

```
version: "3.3"

services:
  frontend:
    restart: always

    ports:
      - 3000:80

```

\*\* Lưu ý: ko edit port 80
