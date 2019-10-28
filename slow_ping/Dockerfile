FROM alpine

ARG PING_HOST
# ARG are only available during build...we must assign then to an ENVironment
ENV HOST_2_PING $PING_HOST

#  SHELL BOMB LIKE:
# CMD while true ; do ping   ${HOST_2_PING} &  done
CMD ping -i 5  ${HOST_2_PING}