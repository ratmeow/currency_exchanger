FROM nginx:alpine

RUN apk update && apk add --no-cache git

RUN git clone https://github.com/zhukovsd/currency-exchange-frontend.git /tmp/currency-exchange-frontend
RUN cp -r /tmp/currency-exchange-frontend/* /usr/share/nginx/html/

EXPOSE 80
