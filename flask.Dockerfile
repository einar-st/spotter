FROM alpine

RUN apk add --no-cache python3
RUN apk add --no-cache py-pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY db_func.py spot_func.py .env cronjob app.py ./

COPY templates ./templates

CMD /usr/bin/python3 -m flask run -h 0.0.0.0 --debug
