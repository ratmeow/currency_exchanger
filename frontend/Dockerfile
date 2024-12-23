FROM nginx:alpine

RUN apk update && apk add --no-cache git

COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN git clone https://github.com/zhukovsd/currency-exchange-frontend.git /tmp/currency-exchange-frontend
RUN sed -i 's|http://localhost:8080/currency_exchange_war_exploded|/api|' /tmp/currency-exchange-frontend/js/app.js
RUN cp -r /tmp/currency-exchange-frontend/* /usr/share/nginx/html/

EXPOSE 80
