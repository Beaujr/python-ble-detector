#FROM python@sha256:9c5872d17798c75ac44430686951138f372807dbec4ae9a167af7a6695443649
FROM python@sha256:5ec706ebfeb2e0eef94a9b04cde965de4acc0fad561e6e755abf3da2ccf13d88

RUN apt-get update
RUN apt-get install build-essential bluez bluez-tools python-dev python-pip libglib2.0-dev libboost-python-dev libboost-thread-dev libbluetooth-dev -y

RUN pip3 install pybluez
RUN pip3 install bluepy
RUN echo "ControllerMode = le" >> /etc/bluetooth/main.conf
