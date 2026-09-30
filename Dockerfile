FROM ubuntu:24.04

ARG RUNNER_VERSION=2.337.0

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    curl \
    git \
    jq \
    ca-certificates \
    sudo \
    tar \
    gzip \
    libicu74 \
    libssl3 \
    libkrb5-3 \
    zlib1g \
    liblttng-ust1t64 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash runner && \
    echo "runner ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/runner && \
    chmod 0440 /etc/sudoers.d/runner

WORKDIR /home/runner/actions-runner

RUN curl -fsSL \
    -o actions-runner.tar.gz \
    "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" && \
    tar xzf actions-runner.tar.gz && \
    rm actions-runner.tar.gz && \
    chown -R runner:runner /home/runner

RUN mkdir -p \
    /home/runner/.cache/uv \
    /home/runner/.cache/ms-playwright && \
    chown -R runner:runner /home/runner/.cache

USER runner

CMD ["bash"]