FROM python:3.12

RUN apt update

# https://github.com/nodesource/distributions?tab=readme-ov-file#installation-instructions
RUN curl -fsSL https://deb.nodesource.com/setup_21.x | bash - && \
  apt-get install -y nodejs postgresql-client netcat-openbsd

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]