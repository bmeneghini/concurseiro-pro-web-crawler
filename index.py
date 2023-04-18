import os
import re
import json
import boto3
import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    urls = ["https://www.princexml.com/samples/", "https://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf"]
    pdf_links = []
    for url in urls:
        html_content = get_html_content(url)
        links = extract_links(html_content)
        pdf_links = filter_pdf_links(links)
        download_pdf_files(pdf_links)
    return {
        "statusCode": 200,
        "body": f"Process completed successfully. Fetched and uploaded {len(pdf_links)} PDF files."
    }

def get_html_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    link_elements = soup.select("a[href]")
    links = []
    for link in link_elements:
        links.append(link.get("href"))
    return links


def filter_pdf_links(links):
    pdf_links = set()
    url_pattern = re.compile(
        r'^(https?://)?'  # scheme (optional)
        r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'  # domain name (required)
        r'(/\S*)?'  # path and query string (optional)
        r'$'
    )
    for link in links:
        if link.endswith(".pdf") and url_pattern.match(link):
            pdf_links.add(link)
    return list(pdf_links)


def download_pdf_files(pdf_links):
    s3 = boto3.client("s3")
    bucket_name = os.environ["BUCKET_NAME"]
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            existing_files = [obj["Key"] for obj in response["Contents"]]
        else:
            existing_files = []
        for link in pdf_links:
            filename = link.split("/")[-1]
            if filename in existing_files:
                print(f"File {filename} already exists in S3, skipping download.")
                continue
            response = requests.get(link)
            response.raise_for_status()
            metadata = {"ContentLength": str(len(response.content))}
            s3.put_object(Bucket=bucket_name, Key=filename, Body=response.content, Metadata=metadata)
            print(f"Downloaded and uploaded file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


class Context:
    def __init__(self, arn: str):
        self.invoked_function_arn = arn


if __name__ == "__main__":
    with open("events/hw.json", 'r') as f:
        event = json.load(f)
        lambda_handler(event, Context("CP-WEB-CRAWLER-PROD"))
