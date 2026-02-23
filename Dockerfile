FROM node:18-alpine

WORKDIR /app

COPY my-react-app/package*.json .

RUN npm install

COPY my-react-app ./

EXPOSE 5173

CMD [ "npm", "run","dev","--","host"]