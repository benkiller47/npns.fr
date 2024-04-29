import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_canonical_url(file_path, root_url):
    relative_path = os.path.relpath(file_path, website_dir)
    canonical_url = urljoin(root_url, relative_path)
    canonical_url = os.path.splitext(canonical_url)[0]
    if os.path.isdir(file_path):
        canonical_url += '/'
    return canonical_url

def update_canonical_tag(file_path, root_url):
    canonical_url = get_canonical_url(file_path, root_url)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

    soup = BeautifulSoup(html_content, features="html.parser")

    canonical_tag = soup.find('link', {'rel': 'canonical'})

    if canonical_tag:
        existing_canonical_url = canonical_tag['href']
        if existing_canonical_url == canonical_url:
            print(f"Skipping {file_path}: Canonical URL already correct.")
            return True
        canonical_tag['href'] = canonical_url
        print(f"Updated canonical URL for {file_path}: {existing_canonical_url} -> {canonical_url}")
    else:
        if soup.head:  # Check if the <head> section exists
            new_canonical_tag = soup.new_tag('link', rel='canonical', href=canonical_url)
            soup.head.append(new_canonical_tag)
            print(f"Added canonical URL for {file_path}: {canonical_url}")
        else:
            print(f"Skipping {file_path}: No <head> section found in the HTML.")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        return False

    return True

def crawl_website(website_dir, root_url):
    successful_files = []
    failed_files = []

    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html') or file.endswith('.htm'):
                file_path = os.path.join(root, file)
                result = update_canonical_tag(file_path, root_url)
                if result:
                    successful_files.append(file_path)
                else:
                    failed_files.append(file_path)

    print("\nSummary:")
    print(f"Successful files: {len(successful_files)}")
    print(f"Failed files: {len(failed_files)}")

    if failed_files:
        print("\nFailed files:")
        for file_path in failed_files:
            print(file_path)

# Usage
website_dir = 'C:/Mes Sites Web/telegram'
root_url = 'https://telegramtanude.com/'

if not os.path.isdir(website_dir):
    print(f"Error: {website_dir} is not a valid directory.")
    sys.exit(1)

crawl_website(website_dir, root_url)