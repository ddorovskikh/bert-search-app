FROM node:16.15.0

WORKDIR /bert-search-app

ENV PATH /bert-search-app/node_modules/.bin:$PATH

COPY package.json ./

COPY ./ ./

RUN npm i
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
