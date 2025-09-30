FROM mambaorg/micromamba


ARG NEW_MAMBA_USER=plantismash
ARG NEW_MAMBA_USER_ID=1002
ARG NEW_MAMBA_USER_GID=1004
USER root

RUN if grep -q '^ID=alpine$' /etc/os-release; then \
      # alpine does not have usermod/groupmod
      apk add --no-cache --virtual temp-packages shadow; \
    fi && \
    usermod "--login=${NEW_MAMBA_USER}" "--home=/home/${NEW_MAMBA_USER}" \
        --move-home "-u ${NEW_MAMBA_USER_ID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NEW_MAMBA_USER}" \
        "-g ${NEW_MAMBA_USER_GID}" "${MAMBA_USER}" && \
    if grep -q '^ID=alpine$' /etc/os-release; then \
      # remove the packages that were only needed for usermod/groupmod
      apk del temp-packages; \
    fi && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NEW_MAMBA_USER}" > "/etc/arg_mamba_user" && \
    :
ENV MAMBA_USER=$NEW_MAMBA_USER

USER $MAMBA_USER



WORKDIR /home/$MAMBA_USER

USER root

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /home/$MAMBA_USER/environment.yml

RUN apt update
RUN apt install -y wget
RUN apt install -y unzip
RUN apt install -y gcc
RUN apt install -y g++



USER $MAMBA_USER

RUN micromamba install -y -v -n base -f /home/$MAMBA_USER/environment.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

## DEPENDENCIES ##

# code
RUN wget https://github.com/plantismash/plantismash/archive/refs/tags/2.0.tar.gz;
RUN tar -xvf 2.0.tar.gz;
RUN mv plantismash-2.0 plantismash;
RUN cd plantismash;

WORKDIR /home/$MAMBA_USER/plantismash/graphlan

RUN pip install .

WORKDIR /home/$MAMBA_USER/plantismash

RUN python download_databases.py --overwrite yes

# clusterblast. TODO: remove once this is integrated into clusterblast itself

WORKDIR /home/$MAMBA_USER

# dispatcher mail
RUN echo temp
RUN wget https://github.com/plantismash/dispatcher/archive/feature/telnet-mail-service.zip -O dispatcher.zip; \
    unzip dispatcher.zip; \
    mv dispatcher-feature-telnet-mail-service dispatcher; \
    cd dispatcher; \
    pip install -r requirements.txt;

# replace with old redis version
#USER root
#RUN apt install -y redis
#USER $MAMBA_USER
#RUN pip install redis==2.10.6 

# ENV PATH=/glimmer3.02/bin:/hmmer-2.3.2:/hmmer-3.1b2:/ncbi-blast-2.2.31+:/plantismash:$PATH

# redis

USER root

RUN apt install -y redis

USER $MAMBA_USER



WORKDIR /home/$MAMBA_USER/dispatcher

STOPSIGNAL SIGINT

CMD redis-server --daemonize yes --port 8951 --protected-mode no; \
    ./runSMASH -c 16 -q redis://localhost:8951/0 --workdir /data/plantismash/upload --container \
    --script /home/$MAMBA_USER/plantismash/run_antismash.py

EXPOSE 8951
