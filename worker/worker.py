import redis
import json
import re
from playwright.sync_api import sync_playwright
import logging
import boto3
from botocore.exceptions import ClientError
import os
from playwright_stealth import Stealth
import requests

def take_screenshot(url, screenshot_name, full_size):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        Stealth().apply_stealth_sync(context)
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        page.screenshot(path=screenshot_name, full_page=full_size)
        browser.close()

def get_minio_s3_client():
    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url="http://minio:9000",
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
            config=boto3.session.Config(signature_version='s3v4'),
            verify=False
        )
        print("Successfully connected to Minio server.")
        return s3_client
    except ClientError as e:
        logging.error(f"Error connecting to Minio: {e}")
        raise

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = get_minio_s3_client()
    try:
        s3_client.head_bucket(Bucket=bucket)
    except ClientError:
        s3_client.create_bucket(Bucket=bucket)
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def finished(url):
    print(f"Screenshot done in : {url}")

def send_url(data_json):
    screenshot_id = None
    try:
        data = json.loads(data_json)
        url = data['url']
        screenshot_id = data['id']
        full_size = data['full_size']
        screenshot_name = f"screenshot_{screenshot_id}.png"

        print("url : ", url)
        take_screenshot(url, screenshot_name, full_size)
        upload_file(screenshot_name, "screenshots")

        requests.post(f"http://nginx/api/screenshots/{screenshot_id}/update_screenshot", {
            'status': 'done',
            'file_path': f"screenshot_{screenshot_id}.png"
        })
        finished(url)

    except Exception as e:
        print(f"l'erreur est : {e}")
        if screenshot_id:
            response = requests.post(f"http://nginx/api/screenshots/{screenshot_id}/update_screenshot", {
                'status': 'failed',
                'file_path': ''
            })

# Connexion Redis
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

# Abonnement au channel
pubsub = r.pubsub()
pubsub.subscribe('screenshot_queue')

print("En attente d'url sur 'screenshot_queue'...")

# listen() est bloquant, pas de polling
for url in pubsub.listen():
    
    # Skip le message de confirmation d'abonnement
    if url['type'] != 'message':
        continue

    print("Url reçu !")
    print(url)
    send_url(url['data'])