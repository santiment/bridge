FROM python:3.8-slim as builder

ARG PYTHON_ENV=production
ENV PYTHON_ENV=${PYTHON_ENV}

RUN pip3 install --no-cache-dir pipenv==2021.5.29

WORKDIR /app

RUN apt update && apt install gcc g++ -y

COPY Pipfile* /app/
# We create a virtual environment in the local folder to install dependencies into it
# and then copy to the target image.
RUN python3 -m venv /app/.venv
RUN PIPENV_VERBOSITY=-1 pipenv install --deploy $(test "$PIP_ENV" = "production" || echo "--dev")

FROM python:3.8-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
RUN rm /app/.venv/pyvenv.cfg

COPY . /app

# Extends python modules search path to include ones from the builder.
ENV PYTHONPATH="$PYTHONPATH:/app/.venv/lib/python3.8/site-packages"
# Extends search path to include runnable python utilities from the builder.
ENV PATH="$PATH:/app/.venv/bin"
ENV PYTHONUNBUFFERED TRUE

WORKDIR /app

CMD ["python", "cli.py", "wbtc"]
