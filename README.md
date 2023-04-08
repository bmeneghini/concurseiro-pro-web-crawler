# Concurseiro PRO Web Crawler

Concurseiro PRO Web Crawler is a Python application that scrapes a website for PDF files and uploads them to an S3 bucket. The application is packaged as an AWS Lambda function and can be triggered using an event.

## Getting Started

To run the application, you'll need Python 3.7 or higher and the `boto3`, `beautifulsoup4`, and `requests` packages. You can install them using pip:

   ```bash
   pip install boto3 beautifulsoup4 requests
   ```

You'll also need to set up an S3 bucket and an AWS Lambda function. The S3 bucket should have a unique name and should be located in the same region as the Lambda function. The Lambda function should use the `lambda_handler` method in the `index.py` file as its entry point.

To deploy the application, you can use the provided GitHub Actions workflow, which automatically packages and deploys the Python code as an AWS Lambda function whenever there is a push to the main branch. To use this workflow, you'll need to set up your AWS credentials as GitHub secrets, and also set the ARN of the Lambda layer containing the dependencies and the name of the Lambda function in the `deploy-lambda.yml` file.

## Usage

To use the application, you'll need to trigger the Lambda function using an event. An example event is provided in the `events/hw.json` file. You can modify this event to specify the URL of the website you want to scrape.

When the Lambda function is triggered, it will scrape the website for PDF files, filter out any links that are not PDF files or are not valid URLs, and upload the remaining PDF files to the specified S3 bucket. If a file with the same name already exists in the bucket, the application will skip the download and upload for that file.

## Files

The repository contains the following files:

* `index.py`: The Python file containing the `lambda_handler` function that is executed by the Lambda function.
* `requeriments.txt`: The text file containing all the dependencies versions.
* `deploy-lambda.yml`: The GitHub Actions workflow file that packages and deploys the Python code as an AWS Lambda function.
* `events/hw.json`: An example event that can be used to trigger the Lambda function.
* `README.md`: This README file.

## GitHub Actions Workflow

This repository uses GitHub Actions to automatically deploy the Python code as an AWS Lambda function whenever there is a push to the main branch. The workflow is defined in the .github/workflows/deploy-lambda.yml file.

The workflow has a single job named build which runs on an Ubuntu latest runner. The job consists of two steps:

1. Checkout: The `actions/checkout@master` action is used to check out the code from the repository.

2. Deploy code to Lambda: The `mariamrf/py-lambda-action@v1.0.0` action is used to package and deploy the Python code as an AWS Lambda function. The action takes two parameters: lambda_layer_arn and lambda_function_name, which are set to the ARN of the Lambda layer containing the dependencies and the name of the Lambda function respectively. The action also sets the necessary environment variables for AWS access using the secrets defined in the GitHub repository settings.

Whenever a push is made to the `main` branch, the `build` job is triggered and the Python code is automatically packaged and deployed as an AWS Lambda function.

## License

This project is licensed under the MIT License.