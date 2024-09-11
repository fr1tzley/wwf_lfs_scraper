FROM python:3.12

EXPOSE 5000/tcp

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY .. .

CMD [ "python", "./app.py" ]