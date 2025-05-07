FROM python:3.12

WORKDIR /
COPY . .

RUN pip install .
VOLUME /model

EXPOSE 8000

# NOTE: use -e WEB_CONCURRENCY=INTEGER to set the number of workers
CMD ["gunicorn", "-b", "0.0.0.0", "src.test1:app"]