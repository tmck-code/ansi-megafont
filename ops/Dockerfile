FROM python:3.14-slim

RUN apt update \
    && apt upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        fontforge git wget unzip tree \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

ARG UID
ARG GID

RUN addgroup --gid $GID user \
    && adduser --uid $UID user --ingroup user

WORKDIR /fonts
RUN git clone https://github.com/rewtnull/amigafonts.git ./amigafonts \
    && wget --progress=dot:mega https://int10h.org/oldschool-pc-fonts/download/oldschool_pc_font_pack_v2.2_linux.zip \
    && unzip -q -d ./ibm oldschool_pc_font_pack_v2.2_linux.zip

RUN python3 -m pip install laser-prynter
ENV PYTHONPATH=/usr/local/lib/python3.14/site-packages

WORKDIR /app
COPY . /app
