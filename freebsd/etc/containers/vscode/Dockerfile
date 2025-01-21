FROM ubuntu:latest

# fix for error "E: Dynamic MMap ran out of room. Please increase the size of APT::Cache-Start. Current value: 25165824. (man 5 apt.conf)"
RUN echo 'APT::Cache-Start "100000000";' >> /etc/apt/apt.conf.d/70debconf

ARG VSCODE_VERSION

RUN apt update && \
    apt install curl git -y && \
    apt clean all && \
    curl -sL "https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64" --output /tmp/vscode-cli.tar.gz && \
    tar -xf /tmp/vscode-cli.tar.gz -C /usr/bin && \
    rm /tmp/vscode-cli.tar.gz && \
    mkdir /src

VOLUME /src
VOLUME /root

CMD [ "code", "tunnel", "--accept-server-license-terms", "--no-sleep" ]
