FROM amazonlinux:2 as database

ENV ZIP_NAME=dynamodb_local_latest.tar.gz

RUN yum install -y \
    tar \
    gzip

# Install Java
RUN amazon-linux-extras enable corretto8
RUN yum install -y java-1.8.0-amazon-corretto

WORKDIR /app

# Download and install Local Dynamo
RUN curl https://s3.us-west-2.amazonaws.com/dynamodb-local/${ZIP_NAME} -o ${ZIP_NAME}
RUN curl https://s3.us-west-2.amazonaws.com/dynamodb-local/${ZIP_NAME}.sha256 -o ${ZIP_NAME}.sha256

RUN mkdir /dynamo
RUN tar -xzf ${ZIP_NAME} -C /dynamo && rm ${ZIP_NAME}

FROM amazonlinux:2 as api

# Install Node
RUN curl -sL https://rpm.nodesource.com/setup_12.x | bash -

RUN yum install -y \
    nodejs \
    python3

WORKDIR /app/infrastructure

# Install SAM cli
RUN python3 --version
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install aws-sam-cli poetry
RUN sam --version

# Install CDK
RUN npm i -g aws-cdk

# Install CDK Dependencies
COPY infrastructure/pyproject.toml pyproject.toml
COPY infrastructure/poetry.lock poetry.lock
RUN poetry install

COPY . /app
