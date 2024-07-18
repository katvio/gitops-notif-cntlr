FROM google/cloud-sdk:alpine

RUN gcloud components install kubectl --quiet

WORKDIR /app

# Install any additional dependencies for Flask app
RUN apk --no-cache add python3 python3-dev build-base py3-pip py3-waitress jq

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x flask-api.py

EXPOSE 5001

RUN echo $PATH

ENTRYPOINT ["python3"]

CMD ["flask-api.py"]