FROM python:3

WORKDIR /Users/dart/Workspace/Virtualization/Docker/Python/tcp_server

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./new_TCP_server.py" ]


