FROM wordpress:5-php7.2

COPY ./var/www/html/wp-content/languages /var/www/html/wp-content/languages
COPY ./var/www/html/wp-content/plugins /var/www/html/wp-content/plugins
COPY ./var/www/html/wp-content/themes /var/www/html/wp-content/themes
