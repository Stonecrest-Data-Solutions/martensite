FROM python:3.12

WORKDIR /
COPY . .

RUN pip install /martensite_utils
RUN pip install --no-cache-dir flask onnxruntime gunicorn

RUN ls .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0", "src.test1:app"]