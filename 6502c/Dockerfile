FROM alpine:3.7

ARG 6502C_VERSION
ENV BUILD_PACKAGES \
    python3 \
    git musl-dev gcc make

RUN apk update && apk upgrade

RUN echo "===> Adding Compile and Python runtime..."  && \
    apk add --no-cache ${BUILD_PACKAGES} 

RUN echo "===> Upgrading pip" && \
    pip3 install --upgrade pip 

RUN echo "===> Compiling cc65" && git clone -b  V2.18  https://github.com/cc65/cc65.git
RUN cd cc65 && make -j2 >make.log && make install PREFIX=~/.local
RUN cd .. && rm -rf cc65

ENV PATH="$HOME/.local/bin:$PATH"

# ca65 is ghe assebler, sim65 is the sim-ulator

RUN echo "===> Installing python emulator" && \
    pip3 install py65==1.1.0

# TODO: Install related mechanincs
# py65mon -l stomper -g 0
RUN mkdir /app
WORKDIR /app
CMD [ sh ]