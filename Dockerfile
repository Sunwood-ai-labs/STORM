FROM python:3.9.19-bookworm

# docker pull python:3.9.19-bookworm
# docker pull python:3.9.19-alpine3.20

# Install Python and pip
# RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y git git-credential-manager

# Install open-interpreter
RUN pip3 install open-interpreter
RUN git config --global core.autocrlf input
# RUN git config user.email "example@example.com"
# RUN git config user.name "Example"

# Set the working directory
WORKDIR /workspace