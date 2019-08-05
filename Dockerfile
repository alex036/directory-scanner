FROM python:3.7-alpine

ADD crontab.txt /crontab.txt
ADD scan.py /scan.py
COPY entry.sh /entry.sh
RUN chmod 755 /scan.py /entry.sh
RUN /usr/bin/crontab /crontab.txt

CMD ["/entry.sh"]
