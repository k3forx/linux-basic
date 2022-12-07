FROM ubuntu:latest
RUN apt update
RUN apt -y install strace software-properties-common build-essential psmisc
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.10
