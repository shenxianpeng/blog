FROM node:12

EXPOSE 4000

WORKDIR /blog

COPY package.json /blog

RUN npm install \
    && npm install -g hexo-cli \
    && npm install hexo-deployer-git --save

ENTRYPOINT ["make"]

CMD ["server"]
