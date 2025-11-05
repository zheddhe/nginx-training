FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
# inutile, les certificats sont montés depuis le host (ne pas pousser ses clés dans une image docker)
# COPY certs/ /etc/nginx/certs/

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]