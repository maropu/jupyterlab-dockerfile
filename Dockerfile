FROM jupyter/datascience-notebook:82d1d0bf0867
MAINTAINER maropu

# Use root for installing JRE
USER root

# Install graphviz for python-graphviz
RUN apt-get dist-upgrade -y && \
    apt-get update -y && \
    apt-get install -y \
      build-essential \
      graphviz

# Install JRE for Spark
RUN apt-get install --no-install-recommends -y openjdk-8-jre-headless ca-certificates-java && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Intall PhantomJS for bokeh
RUN npm install -g phantomjs-prebuilt

# Install additional Python packages
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --no-cache-dir \
      pyspark==2.4.4 \
      koalas==0.17.0 \
      mlflow==1.2.0 \
      pandas-profiling==2.3.0 \
      altair==3.2.0 \
      pydotplus==2.0.2 \
      graphviz==0.13 \
      selenium==3.141.0 \
      yellowbrick==1.0.post1 \
      xgboost==0.82 \
      lightgbm==2.2.3 \
      featuretools==0.10.1 \
      category-encoders==2.0.0 \
      Boruta==0.3 \
      dtreeviz==0.6 \
      bokeh==1.3.4

# Install tensorflow packages
# RUN pip install --no-cache-dir --ignore-installed PyYAML \
#       tensorflow==1.14.0 \
#       tensorflow-data-validation==0.14.1

