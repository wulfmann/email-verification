# Email Verification

## Contributing

### Running Locally

You can use the Dockerfile to run both dynamo, and api gateway locally. This is accomplished with [Local Dynamo](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) and [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-start-api.html).

Make sure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed. The docker daemon should be running.

Build:

```bash
docker-compose build
```

Run:

```bash
docker-compose up
```

You should now be able to hit dynamo at `localhost:5000` and the api at `localhost:3000`.
