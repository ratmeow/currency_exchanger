FROM nginx:alpine

RUN apk update && apk add --no-cache git

RUN git clone https://github.com/zhukovsd/currency-exchange-frontend.git /tmp/currency-exchange-frontend
RUN sed -i 's|http://localhost:8080/currency_exchange_war_exploded|http://localhost:8080|' /tmp/currency-exchange-frontend/js/app.js
RUN cp -r /tmp/currency-exchange-frontend/* /usr/share/nginx/html/

EXPOSE 80
