FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /dir
COPY ./requirements.txt /dir/requirements.txt
RUN pip install -r /dir/requirements.txt

COPY ./app /dir/app
COPY ./config /dir/config
COPY ./main.py /dir/main.py
COPY ./Makefile /dir/Makefile

EXPOSE 8001

CMD ["make", "start"]