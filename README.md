# Concurseiro PRO Web Crawler

Concurseiro PRO Web Crawler is a Lambda function that crawls a list of URLs, extracts links to PDF files, downloads the files, and uploads them to an S3 bucket.

## Functionality

* Crawl a list of URLs.
* Extract links to PDF files from the crawled web pages.
* Download PDF files and upload them to an S3 bucket.

## Environment Variables

The following environment variables are required to run the Lambda function:

* `BUCKET_NAME`: The S3 bucket where the downloaded files will be stored.

## Deployment

This repository includes a GitHub Actions workflow for deploying the Lambda function on push to the `main` branch:

```
name: deploy-py-lambda

on:
push:
branches:
- main

jobs:
build:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v2
- name: Deploy code to Lambda
uses: mariamrf/py-lambda-action@v1.0.0
with:
lambda_function_name: 'cp-web-crawler'
env:
AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
AWS_DEFAULT_REGION: ${{ secrets.AWS_REGION }}
```

To configure the deployment, set up the following secrets in your GitHub repository:

* `AWS_ACCESS_KEY_ID`: AWS access key ID
* `AWS_SECRET_ACCESS_KEY`: AWS secret access key
* `AWS_REGION`: AWS region where the Lambda function is deployed

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```


## Usage

To run the script locally, you can execute the following command:

````bash
python index.py
````


There's a run configuration under `.run` folder, you have to set up all the environment variables in order to local debug the code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Note: Make sure to replace `BUCKET_NAME` with your actual S3 bucket name in the README and set up the environment variable in your Lambda function configuration.
