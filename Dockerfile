FROM ubuntu:16.04
MAINTAINER "Gior Bernal"

RUN apt-get update -y && \
    apt-get install zip -y && \
    apt-get install unzip -y && \
    apt-get install software-properties-common -y && \
	add-apt-repository ppa:deadsnakes/ppa -y && \
	apt-get update -y && \
	apt-get install virtualenv -y && \
	apt-get install python3.8 -y && \
	apt-get install python3.8-tk -y && \
	mv /usr/bin/python3 /usr/bin/python3_bu && \
	ln -s /usr/bin/python3.8 /usr/bin/python3 && \
	ln -s /usr/bin/python3 /usr/bin/python && \
	apt-get install python3-pip -y && \
	ln -s /usr/bin/pip3 /usr/bin/pip && \
	pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install numpy && \
	pip install pandas && \
	pip install matplotlib && \
	pip install seaborn && \
	pip install streamlit && \
	pip install pyshp && \
	pip install shapely && \
	pip install pyproj

RUN ["mkdir", "opt/app"]

COPY utils/ /opt/app/utils/
COPY datasets/ /opt/app/datasets/
COPY main.py /opt/app
COPY docker/entrypoint.sh /

# Streamlit application port
EXPOSE 8501

CMD ["/entrypoint.sh"]
