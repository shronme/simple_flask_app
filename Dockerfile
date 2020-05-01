FROM ronbckbn/cf_base

# # setup all the configfiles
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf


# RUN rm -rf /etc/nginx/sites-* /etc/nginx/snippets /etc/nginx/conf.d/default.conf
# ADD nginx/ /etc/nginx/
# ADD supervisord.conf /etc/supervisor/
# ADD supervisor-app.conf /etc/supervisor/conf.d/
ADD ./uwsgi.ini /etc/uwsgi.ini
RUN mkdir /home/code/

ENV PYTHONPATH=/home/code
ENV UWSGI_INI=/etc/uwsgi.ini
ADD ./* /home/code/
ADD ./requirements.txt /home/code/
RUN pip3 install -r /home/code/requirements.txt

## add (the rest of) our code

WORKDIR /home/code/

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
ADD ./entrypoint.sh /entrypoint.sh
ADD ./start.sh /start.sh
RUN chmod +x /start.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]