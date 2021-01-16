FROM python:3.8-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get install -y curl

RUN curl https://www.cprover.org/cbmc/download/cbmc-5-11-linux-64.tgz > cbmc.tar.gz && mkdir /cbmc && tar -xzvf cbmc.tar.gz -C /cbmc

COPY . .


ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"
ENV PATH="${PATH}:/cbmc"

RUN mkdir -p /pwd

WORKDIR /pwd

ENTRYPOINT [ "python", "-m", "counterSharp" ]

# TODO(steuber): Jetzt doch __CPROVER_start???