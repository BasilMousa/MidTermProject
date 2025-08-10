FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    libapache2-mod-wsgi-py3 \
    && pip install flask \
    && a2enmod wsgi \
    && apt-get clean

COPY apache.conf /etc/apache2/sites-available/000-default.conf

COPY . /var/www/flask_app

WORKDIR /var/www/flask_app

# Ensure templates directory exists and has correct permissions
RUN mkdir -p /var/www/flask_app/templates \
    && chown -R www-data:www-data /var/www/flask_app \
    && chmod -R 755 /var/www/flask_app \
    && ls -l /var/www/flask_app/templates || echo "Templates directory not found"

CMD ["apache2ctl", "-D", "FOREGROUND"]