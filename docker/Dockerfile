FROM ubuntu:18.04

# System packages 
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda
RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
RUN bash Miniconda2-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda2-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

RUN apt-get update && apt-get install -y \
	git \
	build-essential \
	swig \
	g++-5 \
	libglpk-dev \
	libpython-all-dev	

RUN git clone https://github.com/ludwigschmidt/ppoly_density.git /root/ppoly_density
WORKDIR /root/ppoly_density 
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV CVXOPT_BUILD_GLPK=1
RUN pip install cvxopt
RUN make ellipsoid_swig

WORKDIR /root/ppoly_density/experiments

CMD ['bash']