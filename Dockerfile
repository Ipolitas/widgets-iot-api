FROM python:3.11-slim
LABEL maintainer="Ipolitas"

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false

# create venv
RUN python -m venv /py && \
    # upgrade pip inside venv
    /py/bin/pip install --upgrade pip && \
    # install specified requirements
    /py/bin/pip install -r /tmp/requirements.txt && \
    # if DEV is set to true, install dev requirements
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # remove "tmp" dir
    rm -rf /tmp


# Command to run FastAPI using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Update env vars
# PATH - points to system PATH, so we wouldn't need to specify for each command
ENV PATH="/py/bin:$PATH"
