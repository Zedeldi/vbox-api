# syntax=docker/dockerfile:1

ARG PACMAN_ARGS=""

FROM archlinux:base AS base
ARG PACMAN_ARGS
RUN pacman-key --init
RUN pacman -Syu --noconfirm ${PACMAN_ARGS}

FROM base AS virtualbox
ARG PACMAN_ARGS
RUN pacman -S --noconfirm ${PACMAN_ARGS} virtualbox

FROM virtualbox AS target
ARG USER="user"
ARG PASS="password"
RUN useradd -m "${USER}"
RUN echo "${USER}:${PASS}" | chpasswd

USER "${USER}"
CMD ["vboxwebsrv"]
