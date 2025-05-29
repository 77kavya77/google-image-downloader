# Google Image Downloader

A Python script to download images from Google search results.

## Features
- Search and download images by keyword
- Customizable number of images
- Parallel downloads for faster performance
- Simple command-line interface

## Installation

git clone https://github.com/your-username/google-image-downloader.git
cd google-image-downloader
pip install -r requirements.txt

## Usage
python image_downloader.py "your search query" -n 20 -o my_images -t 10

## Arguments
query          : Search term (required)
-n/--num_images: Number of images (default: 10)
-o/--output    : Output folder (default: "downloaded_images")
-t/--threads   : Download threads (default: 5)
