docker build type=docker,name=mrzoo-backend -f type=docker,name=mrzoo-backend\.nixpacks\Dockerfile -t 0fe609e1-b437-4969-89d6-23e80b57d8e0 --build-arg NIXPACKS_METADATA=python --build-arg PIP_DEFAULT_TIMEOUT=100 --build-arg PIP_DISABLE_PIP_VERSION_CHECK=1 --build-arg PIP_NO_CACHE_DIR=1 --build-arg PYTHONDONTWRITEBYTECODE=1 --build-arg PYTHONFAULTHANDLER=1 --build-arg PYTHONHASHSEED=random --build-arg PYTHONUNBUFFERED=1