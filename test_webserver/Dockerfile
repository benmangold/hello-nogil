FROM py314_nogil:latest

ENV PYTHONUNBUFFERED=1

WORKDIR /home/python/webserver

COPY main.py .

EXPOSE 8000

CMD ["python3", "main.py"]
