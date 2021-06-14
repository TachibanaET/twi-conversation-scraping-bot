FROM continuumio/miniconda3

WORKDIR /workspace/source

ARG HTTP_PROXY
ENV http_proxy ${HTTP_PROXY}
ENV https_proxy ${HTTP_PROXY}

RUN pip install schedule

ENTRYPOINT [ "python", "index.py" ]