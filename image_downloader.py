import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import argparse
import time

class GoogleImageDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def search_images(self, query, num_images=10):
        """Search for images on Google and return image URLs"""
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
        
        try:
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching search results: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        images = []
        
        # Find all image elements
        img_elements = soup.find_all('img')
        
        for img in img_elements:
            if 'data-src' in img.attrs:
                images.append(img['data-src'])
            elif 'src' in img.attrs:
                images.append(img['src'])
                
            if len(images) >= num_images:
                break

        return images[:num_images]

    def download_image(self, url, folder_path, filename_prefix="img"):
        """Download a single image and save it to the specified folder"""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        try:
            # Generate a unique filename
            timestamp = int(time.time() * 1000)
            filename = f"{filename_prefix}_{timestamp}.jpg"
            filepath = os.path.join(folder_path, filename)
            
            # Download and save the image
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', self.headers['User-Agent'])]
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(url, filepath)
            print(f"Downloaded: {filename}")
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False

    def download_images(self, query, num_images=10, folder_name="downloaded_images", max_workers=5):
        """Download multiple images for a search query"""
        print(f"Searching for '{query}' images...")
        image_urls = self.search_images(query, num_images)
        
        if not image_urls:
            print("No images found.")
            return
        
        print(f"Found {len(image_urls)} images. Downloading...")
        
        # Create folder if it doesn't exist
        folder_path = os.path.join(os.getcwd(), folder_name, query.replace(' ', '_'))
        
        # Download images using thread pool for better performance
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i, url in enumerate(image_urls):
                executor.submit(self.download_image, url, folder_path, f"{query.replace(' ', '_')}_{i}")
        
        print(f"Download completed. Images saved in: {folder_path}")

def main():
    parser = argparse.ArgumentParser(description='Google Image Downloader')
    parser.add_argument('query', type=str, help='Search query for images')
    parser.add_argument('-n', '--num_images', type=int, default=10, 
                        help='Number of images to download (default: 10)')
    parser.add_argument('-o', '--output', type=str, default="downloaded_images",
                        help='Output folder name (default: downloaded_images)')
    parser.add_argument('-t', '--threads', type=int, default=5,
                        help='Number of threads to use for downloading (default: 5)')
    
    args = parser.parse_args()
    
    downloader = GoogleImageDownloader()
    downloader.download_images(
        args.query, 
        num_images=args.num_images, 
        folder_name=args.output,
        max_workers=args.threads
    )

if __name__ == "__main__":
    main()