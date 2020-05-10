FROM python:3.8.2
MAINTAINER "Gior Bernal"

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
COPY docker/getSourceData.sh /opt/app

# Streamlit application port
EXPOSE 8501

CMD ["/entrypoint.sh"]
