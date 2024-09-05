# app/Dockerfile

FROM python:3.11.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/kornelko2/streamlit_nas.git .

RUN pip install --upgrade pip

# RUN pip install streamlit pandas plotly yfinance

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_nas.py", "--server.port=8501", "--server.address=0.0.0.0"]