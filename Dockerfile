# install lims microservice

FROM google/python-runtime
MAINTAINER Robin Andeer

ENTRYPOINT ["/env/bin/gunicorn", "-b :8080", "wsgi_gunicorn:app"]
