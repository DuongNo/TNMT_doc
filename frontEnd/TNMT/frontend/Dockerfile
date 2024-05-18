# Fetching the latest node image on apline linux
FROM node:latest AS builder



# Setting up the work directory
WORKDIR /app

# Installing dependencies
COPY ./package.json ./
RUN npm install
ENTRYPOINT ["/entrypoint.sh"]
# Copying all the files in our project
COPY . .

ARG VITE_SERVER_PORT=2666
RUN echo "VITE_SERVER_PORT=$VITE_SERVER_PORT" > .env.production
# Declaring env
ENV NODE_ENV production

# Building our application
RUN npm run build

# Fetching the latest nginx image
FROM nginx

# Copying built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copying our nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf