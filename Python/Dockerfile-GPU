FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND noninteractive

#install dependencies
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ninja-build \
    ca-certificates \
    python3-dev  \
    python3-pip  \
    python3-setuptools \
    git \
    g++ \
    wget \
    make \
    libprotobuf-dev  \
    protobuf-compiler \
    libopencv-dev \
    libgoogle-glog-dev \
    libboost-all-dev \
    libhdf5-dev \
    libatlas-base-dev

#install python dependencies
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt

##################Detectron2 installation##################
RUN pip install 'git+https://github.com/facebookresearch/fvcore'
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
ENV FORCE_CUDA="1"
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"
RUN pip install --user -e detectron2_repo
ENV FVCORE_CACHE="/tmp"
WORKDIR /home/appuser/detectron2_repo

##################Openpose installation##################
#replace cmake as old version has CUDA variable bugs
RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.0/cmake-3.16.0-Linux-x86_64.tar.gz && \
tar xzf cmake-3.16.0-Linux-x86_64.tar.gz -C /opt && \
rm cmake-3.16.0-Linux-x86_64.tar.gz
ENV PATH="/opt/cmake-3.16.0-Linux-x86_64/bin:${PATH}"

#get openpose
WORKDIR /openpose
RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git .

#build it
WORKDIR /openpose/build
RUN cmake -DBUILD_PYTHON=ON -DUSE_CUDNN=OFF .. && make -j `nproc`
WORKDIR /openpose

#install openpose python library
RUN cd  /openpose/build/python/openpose && make install

# Copy the Python module to the Python package directory
RUN cd /openpose/build/python/openpose && \
    cp ./pyopenpose.cp* /usr/local/lib/python3.8/dist-packages && \
    cd /usr/local/lib/python3.8/dist-packages && \
    ln -s pyopenpose.cp* pyopenpose && \
    export LD_LIBRARY_PATH=/openpose/build/python/openpose

RUN pip3 install -U flask-cors

# copy local files \
WORKDIR /app
COPY . /app
EXPOSE 5000
CMD python3 main.py