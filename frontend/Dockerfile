FROM node:20 AS build-stage
WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM node:20 AS serve-frontend
RUN npm install -g serve
WORKDIR /app
COPY --from=build-stage /app/build ./build
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
