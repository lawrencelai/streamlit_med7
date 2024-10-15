FROM python:3.12.7-slim

ADD  . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "med7.py", "--server.port=8501", "--server.address=0.0.0.0"]