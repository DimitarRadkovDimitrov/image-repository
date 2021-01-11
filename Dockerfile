FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_APPLICATION_CREDENTIALS=service_account.json
WORKDIR /shopify_challenge
COPY requirements.txt /shopify_challenge/
RUN pip install -r requirements.txt
COPY . /shopify_challenge/
