# syntax=docker/dockerfile:1

FROM archlinux:base AS base
RUN pacman-key --init
RUN pacman -Syu --noconfirm

FROM base AS virtualbox
RUN pacman -S --noconfirm virtualbox

from virtualbox AS target
ARG USER="user"
ARG PASS="password"
RUN useradd -m "${USER}"
RUN echo "${USER}:${PASS}" | chpasswd

USER "${USER}"
CMD ["vboxwebsrv"]
