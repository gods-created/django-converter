FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
RUN chmod 777 -R /app/*
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]