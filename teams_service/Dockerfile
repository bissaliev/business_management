FROM python:3.10

WORKDIR /app

ENV PYTHONPATH="/app"

COPY ./requirements.txt .

RUN pip install -r /app/requirements.txt

COPY . .

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]