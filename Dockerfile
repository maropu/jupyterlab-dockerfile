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
    pyarrow==0.10.0 \
    koalas==0.17.0 \
    mlflow==1.2.0 \
    pandas==0.24.0 \
    pandas-profiling==2.3.0 \
    altair==3.2.0 \
    pydotplus==2.0.2 \
    graphviz==0.13 \
    selenium==3.141.0 \
    yellowbrick==1.0.post1 \
    snorkel==0.9.1 \
    textblob==0.15.3 \
    xgboost==0.82 \
    lightgbm==2.2.3 \
    featuretools==0.10.1 \
    category-encoders==2.0.0 \
    m2cgen==0.4.0 \
    Boruta==0.3 \
    dtreeviz==0.6 \
    bokeh==1.3.4

# Install tensorflow packages
# RUN pip install --no-cache-dir --ignore-installed PyYAML \
#  tensorflow==1.14.0 \
#  tensorflow-data-validation==0.14.1

# Enable the JupyterLab extension manager
RUN mkdir -p /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/extensionmanager-extension
RUN echo '{ "enabled": true }' > \
  /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/extensionmanager-extension/plugin.jupyterlab-settings

# Enable the vim keymap
# RUN mkdir -p /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/codemirror-extension
# RUN echo '{ "keyMap": "vim" }' > \
#   /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/codemirror-extension/commands.jupyterlab-settings

# Add line numbers
RUN mkdir -p /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/notebook-extension
RUN echo '{ "codeCellConfig": { "lineNumbers": true } }' \
  /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/notebook-extension/tracker.jupyterlab-settings

# Install JupyterLab extensions
RUN jupyter labextension install @lckr/jupyterlab_variableinspector
# RUN jupyter labextension install jupyterlab_vim

RUN jupyter labextension install @jupyterlab/git
RUN pip install jupyterlab-git
RUN jupyter serverextension enable --py jupyterlab_git

