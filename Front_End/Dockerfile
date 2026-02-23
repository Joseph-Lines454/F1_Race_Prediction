FROM node:18

WORKDIR /app

COPY Front_End/react_front_end/package*.json ./

RUN npm install

COPY Front_End/react_front_end /.

CMD ["npm","start"]