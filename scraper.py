import os
import time
from urllib.parse import urljoin
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import List


class ProductImageScraper:
    def __init__(self, base_url: str, categories: List[str], image_dir_1: str, image_dir_2: str, filename: str) -> None:
        self.base_url = base_url
        self.categories = categories
        self.image_dir_1 = image_dir_1
        self.image_dir_2 = image_dir_2
        self.filename = filename
        self.driver = self._initialize_driver()
        self._create_directories()

    @staticmethod
    def _initialize_driver() -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        return driver

    def _create_directories(self) -> None:
        os.makedirs(self.image_dir_1, exist_ok=True)
        os.makedirs(self.image_dir_2, exist_ok=True)

    def get_product_links(self, category: str) -> List[str]:
        try:
            category_url = urljoin(self.base_url, category)
            self.driver.get(category_url)
            product_links = []

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.relative > div > a.group"))
            )

            while len(product_links) < 33:
                links = self.driver.find_elements(By.CSS_SELECTOR, "div.relative > div > a.group")
                for link in links:
                    href = link.get_attribute('href')
                    if href not in product_links:
                        product_links.append(href)
                    if len(product_links) == 33:
                        break
            return product_links
        except Exception as e:
            print(f"Error getting product links for category '{category}': {e}")
            return []

    @staticmethod
    def convert_product_title(product_title: str) -> str:
        return product_title.replace('-', ' ').replace(' ', '_')

    def write_strings_to_file(self, string: str) -> None:
        with open(self.filename, 'a') as file:
            file.write(string + '\n')

    def download_image(self, idx: int, image_urls: List[str], product_title: str, description: str) -> None:
        images_and_description = ""
        for product_id, image_url in enumerate(image_urls):
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                if product_id == 0:
                    image_path = os.path.join(self.image_dir_1, f"0000{idx}_c_{product_title}.jpg")
                    images_and_description += f"0000{idx}_c_{product_title}.jpg"
                else:
                    image_path = os.path.join(self.image_dir_2, f"0000{idx}_i{product_id - 1}_{product_title}.jpg")
                    images_and_description += f" 0000{idx}_i{product_id - 1}_{product_title}.jpg"
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                time.sleep(2)
            except Exception as e:
                print(f"Error downloading image '{image_url}': {e}")
        images_and_description += f", {description}"
        self.write_strings_to_file(images_and_description)

    def scrape_category(self, category: str) -> None:
        product_links = self.get_product_links(category)
        for idx, product_link in enumerate(product_links):
            try:
                self.driver.get(product_link)
                image_urls = []

                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "div.relative > div  > a > div > picture > img"))
                )

                links = self.driver.find_elements(By.CSS_SELECTOR, "div.relative > div  > a > div > picture > img")
                product_title = self.driver.find_element(By.CSS_SELECTOR,
                                                         ".product-page > div:has(header) header h1").text
                converted_title = self.convert_product_title(product_title)
                description = self.driver.find_element(By.CSS_SELECTOR, "div.pr-4 + div").text
                src = links[-1].get_attribute('src')
                image_urls.append(src)
                for link in links[:4]:
                    src = link.get_attribute('src')
                    if src not in image_urls:
                        image_urls.append(src)

                self.download_image(idx, image_urls, converted_title, description)
            except Exception as e:
                print(f"Failed to scrape product '{product_link}': {e}")

    def scrape(self) -> None:
        try:
            for category in self.categories:
                self.scrape_category(category)
        except KeyboardInterrupt:
            print("Scraping interrupted by user.")
        finally:
            self.driver.quit()
            print("Image scraping completed.")


def main() -> None:
    base_url = "https://girlfriend.com/collections/"
    categories = ["leggings", "sports-bras", "tops"]
    image_dir_1 = "cloth_images"
    image_dir_2 = "model_images"
    filename = "images_and_descriptions.txt"

    scraper = ProductImageScraper(base_url, categories, image_dir_1, image_dir_2, filename)
    scraper.scrape()


if __name__ == "__main__":
    main()
