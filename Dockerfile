FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    bzip2 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/conda-forge/miniforge/releases/download/24.11.3-0/Miniforge3-24.11.3-0-Linux-x86_64.sh -O /tmp/miniforge.sh \
    && bash /tmp/miniforge.sh -b -p $CONDA_DIR \
    && rm /tmp/miniforge.sh

COPY environment.yml /tmp/environment.yml
RUN conda env update -n base -f /tmp/environment.yml && conda clean -a -y

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app/src:/app/user_controllers

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "base", "python", "-m", "chwplantfulltest.runner"]
CMD ["--config", "configs/smoke_test.yaml"]
