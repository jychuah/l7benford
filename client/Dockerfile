FROM node:current-alpine3.10
WORKDIR /src
COPY ./benford /src
RUN yarn install
ENTRYPOINT yarn build --target app --dest /build/static