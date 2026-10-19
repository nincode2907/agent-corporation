FROM node:24.21.0-alpine@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1 AS build
WORKDIR /web
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci
COPY apps/web ./
RUN npm run build

FROM nginx:stable-alpine@sha256:ed84151ed2d47ef93c0939eb9b9754c6990db6092cd2081e11988a47a83d47ea AS runtime
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /web/dist /usr/share/nginx/html
USER 101:101
EXPOSE 15500
CMD ["nginx", "-g", "daemon off;"]
