FROM continuumio/anaconda:latest
RUN conda config --append channels https://conda.anaconda.org/conda-forge
RUN conda install -y simplejson
RUN conda install -y spyre
RUN conda install -y mpld3
RUN conda install -y seaborn
RUN conda install -y keras
COPY TestWebApp /home/TestWebApp
COPY PythonLib /home/PythonLib
ENV PYTHONPATH /home/PythonLib:$PYTHONPATH
CMD python /home/TestWebApp/runserver.py