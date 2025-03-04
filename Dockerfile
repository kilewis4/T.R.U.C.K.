FROM ubuntu:18.04  
LABEL maintainer="contact@devopscube.com" 
RUN  apt-get -y update && apt-get -y install nginx
RUN chmod -R 755 /usr/share/nginx/html && chown -R www-data:www-data /usr/share/nginx/html
COPY src/website/default /etc/nginx/sites-available/default
COPY src/website/TruckEntry.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
