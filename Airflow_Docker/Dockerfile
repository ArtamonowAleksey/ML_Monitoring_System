FROM apache/airflow:2.10.2-python3.11



ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

USER root
RUN mkdir -p /home/airflow/.local/share/sdv && \
    chmod -R 777 /home/airflow/.local/share/sdv
USER airflow