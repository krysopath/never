FROM alpine:3.7 as builder
ENV BUILD_APKS "python3 py3-pip"
COPY ./requirements.txt /code/requirements.txt
COPY ./docker /code/docker
RUN /code/docker/builder.sh

FROM alpine:3.7
ENV RUN_APKS "su-exec python3"
COPY --from=builder /code /code
RUN /code/docker/prepare-env.sh
COPY ./broker /code/broker
COPY ./run_api.py /code/run_api.py
COPY ./migrate_this.py /code/migrate_this.py
EXPOSE 5000
CMD ["/sbin/su-exec", "never", "/code/docker/runner.sh"]

#ENTRYPOINT ["/sbin/su-exec", "never", "/code/docker/entry.sh"]


