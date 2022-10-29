FROM python:3.10

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD python -u ./main.py