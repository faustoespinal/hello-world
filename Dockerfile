FROM tiangolo/uwsgi-nginx-flask:python3.8
#ENV http_proxy http://http-proxy.ha.health.ge.com:88/
#ENV https_proxy http://http-proxy.ha.health.ge.com:88/
RUN pip install requests flask
#ENV http_proxy=
#ENV https_proxy=
COPY ./thinslice /app
