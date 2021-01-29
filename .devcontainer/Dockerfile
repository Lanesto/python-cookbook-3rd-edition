FROM python:3.9

COPY .devcontainer/requirements.txt /etc/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /etc/requirements.txt
