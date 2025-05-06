FROM python:3.12

WORKDIR /
COPY . .

RUN pip install flask onnxruntime gunicorn martensite-utils

VOLUME /model

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0", "src.test1:app"]