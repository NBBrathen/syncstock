FROM ubuntu:latest
LABEL authors="nbrathen"

ENTRYPOINT ["top", "-b"]