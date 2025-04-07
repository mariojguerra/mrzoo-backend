FROM ghcr.io/railwayapp/nixpacks:ubuntu-1742861060

ENTRYPOINT ["/bin/bash", "-l", "-c"]
WORKDIR /app/


COPY .nixpacks/nixpkgs-bc8f8d1be58e8c8383e683a06e1e1e57893fff87.nix .nixpacks/nixpkgs-bc8f8d1be58e8c8383e683a06e1e1e57893fff87.nix
RUN nix-env -if .nixpacks/nixpkgs-bc8f8d1be58e8c8383e683a06e1e1e57893fff87.nix && nix-collect-garbage -d


ARG NIXPACKS_METADATA PIP_DEFAULT_TIMEOUT PIP_DISABLE_PIP_VERSION_CHECK PIP_NO_CACHE_DIR PYTHONDONTWRITEBYTECODE PYTHONFAULTHANDLER PYTHONHASHSEED PYTHONUNBUFFERED
ENV NIXPACKS_METADATA=$NIXPACKS_METADATA PIP_DEFAULT_TIMEOUT=$PIP_DEFAULT_TIMEOUT PIP_DISABLE_PIP_VERSION_CHECK=$PIP_DISABLE_PIP_VERSION_CHECK PIP_NO_CACHE_DIR=$PIP_NO_CACHE_DIR PYTHONDONTWRITEBYTECODE=$PYTHONDONTWRITEBYTECODE PYTHONFAULTHANDLER=$PYTHONFAULTHANDLER PYTHONHASHSEED=$PYTHONHASHSEED PYTHONUNBUFFERED=$PYTHONUNBUFFERED

# setup phase
# noop

# install phase
ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH
COPY . /app/.
RUN --mount=type=cache,id=vSZsCEZPIPM-/root/cache/pip,target=/root/.cache/pip python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt


RUN printf '\nPATH=/opt/venv/bin:$PATH' >> /root/.profile

# start
COPY . /app

CMD ["gunicorn app:app --bind 0.0.0.0:$PORT"]

