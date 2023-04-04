import boto3
import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    url = "https://www.princexml.com/samples/"
    html_content = get_html_content(url)
    links = extract_links(html_content)
    pdf_links = filter_pdf_links(links)
    download_pdf_files(pdf_links)


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
    pdf_links = []
    for link in links:
        if link.endswith(".pdf"):
            pdf_links.append(link)
    return pdf_links


def download_pdf_files(pdf_links):
    s3 = boto3.client("s3")
    bucket_name = "cp-nomination-files"
    existing_files = [obj["Key"] for obj in s3.list_objects(Bucket=bucket_name)["Contents"]]
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