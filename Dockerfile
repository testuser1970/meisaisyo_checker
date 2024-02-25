FROM python:3.8

WORKDIR /app_kanri

COPY /requirements.txt ./

RUN apt-get update && \
    apt-get -y upgrade && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8501

COPY . /app_kanri

ENTRYPOINT ["streamlit", "run"]

CMD ["main.py"]
