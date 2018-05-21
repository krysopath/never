FROM alpine:3.7 as builder
ENV BUILD_APKS "python3 py3-pip"
WORKDIR /code
COPY ./anakin /code/anakin
COPY ./dbio /code/dbio
COPY ./never /code/never
COPY ./docker/builder.sh /code/docker/builder.sh
RUN ./docker/builder.sh


FROM alpine:3.7
ENV RUN_APKS "su-exec python3"
COPY --from=builder /code /code
COPY ./docker/runner.sh /code/docker/runner.sh
RUN /code/docker/runner.sh
COPY ./docker/entry.sh /code/docker/entry.sh
COPY ./g.db /code/storage/stash/g.db
CMD ["/sbin/su-exec", "never", "/code/docker/entry.sh"]
