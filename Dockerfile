# Base image
FROM python:3.10-slim
# Set working directory
WORKDIR /opt/app
# Copy only requirements.txt first
COPY requirements.txt /opt/app/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application
COPY . .
# Install packages that we need. vim is for helping with debugging
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get upgrade -yq ca-certificates && \
    apt-get install -yq --no-install-recommends \
    prometheus-node-exporter curl

EXPOSE 7860
EXPOSE 8000
EXPOSE 9100
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD bash -c "/usr/local/bin/python3 /opt/app/app.py"
# /usr/bin/prometheus-node-exporter --web.listen-address='0.0.0.0:9100' & 
