FROM node:15
LABEL maintainer="jameelhamdan99@yahoo.com"
COPY package*.json /
RUN npm install gulp-cli -g && npm install
WORKDIR /usr/src/app
COPY . .
RUN npm run build
