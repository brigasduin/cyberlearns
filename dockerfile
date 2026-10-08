FROM ubuntu:22.04
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN useradd -rm -d /home/eduardolucas -s /bin/bash -g root -G sudo -u 1000 eduardolucas
RUN echo 'eduardolucas:ruinsnolol' | chpasswd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

