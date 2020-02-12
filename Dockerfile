FROM wordpress:5-php7.2

ENV WORDPRESS_CONFIG_EXTRA "\$_SERVER['HTTPS'] ='on';define( 'WP_HOME', 'https://blog.yong-ju.me' );define( 'WP_SITEURL', 'https://blog.yong-ju.me' );"

COPY ./var/www/html/wp-content/languages /var/www/html/wp-content/languages
COPY ./var/www/html/wp-content/plugins /var/www/html/wp-content/plugins
COPY ./var/www/html/wp-content/themes /var/www/html/wp-content/themes
