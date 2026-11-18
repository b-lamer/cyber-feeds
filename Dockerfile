FROM python:3.14.7-slim
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN mkdir -p /home/app/.streamlit && chmod -R 777 /home/app && chmod -R 777 /app

EXPOSE 8501

RUN useradd app
USER app

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]