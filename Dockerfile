FROM node:20

WORKDIR /blog

COPY package.json /blog

RUN npm install \
    && npm install -g hexo-cli \
    && npm install hexo-deployer-git --save

EXPOSE 4000
