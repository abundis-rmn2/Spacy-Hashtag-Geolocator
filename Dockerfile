FROM python:3.11.0b4-buster

ARG _USER="spacy"
ARG _UID="1001"
ARG _GID="100"
ARG _SHELL="/bin/bash"

# Install apt dependencies
RUN apt-get update && apt-get install -y \
    nano \
    git \
    wget

RUN useradd -m -s "${_SHELL}" -N -u "${_UID}" "${_USER}"

ENV USER ${_USER}
ENV UID ${_UID}
ENV GID ${_GID}
ENV HOME /home/${_USER}
ENV PATH "${HOME}/.local/bin/:${PATH}"
ENV PIP_NO_CACHE_DIR "true"

RUN mkdir /home/${_USER}/app && chown ${UID}:${GID} /home/${_USER}/app

USER ${_USER}

COPY --chown=${UID}:${GID} config* /home/${_USER}/app
COPY --chown=${UID}:${GID} requirements* /home/${_USER}/app
COPY --chown=${UID}:${GID} ./py /home/${_USER}/app/py

WORKDIR /home/${_USER}/app

RUN pip install https://github.com/hoefling/so-59927844/releases/download/0.1/blis-0.4.1-cp37-cp37m-linux_armv7l.whl
RUN pip install https://github.com/hoefling/so-59927844/releases/download/0.1/spacy-2.2.3-cp37-cp37m-linux_armv7l.whl

RUN pip install -r requirements.txt

CMD bash
