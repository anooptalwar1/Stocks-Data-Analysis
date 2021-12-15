FROM containers.disney.com/python:3.7.11-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["./script.sh"]