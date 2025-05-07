FROM python:3.10

WORKDIR /app

ENV PYTHONPATH="/app"

COPY ./requirements.txt .

RUN pip install -r /app/requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

COPY . .

ENTRYPOINT [ "/app/entrypoint.sh" ]
