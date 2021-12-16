FROM python:3.7.12-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["sh", "script.sh"]