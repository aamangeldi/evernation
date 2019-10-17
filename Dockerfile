FROM ubuntu:latest
LABEL maintainer=aamangeldi

ARG CHEESESHOP_USER
ARG CHEESESHOP_PASSWORD
ARG CHEESESHOP_INDEX

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app

RUN echo ${CHEESESHOP_INDEX}
RUN CHEESESHOP_AUTH="${CHEESESHOP_USER:+${CHEESESHOP_USER}:${CHEESESHOP_PASSWORD}@}"; \
  pip install -i https://${CHEESESHOP_AUTH}${CHEESESHOP_INDEX} -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
