import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AliExpressTopRankingScraper:
    def __init__(self, proxy=None):
        options = uc.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        # 🔐 Apply proxy if given
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')

        self.driver = uc.Chrome(headless=False, version_main=137, options=options)

    def scroll_and_load(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        for _ in range(12):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

    def scrape_top_ranking(self):
        url = "https://www.aliexpress.com/gcp/top-ranking"
        self.driver.get(url)
        time.sleep(10)
        self.scroll_and_load()

        results = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, "div.top-ranking-item-card")

        print(f"🧠 Found {len(cards)} product cards")

        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "div.top-ranking-item-card-title").text
                price = card.find_element(By.CSS_SELECTOR, "div.top-ranking-item-card-price").text
                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

                results.append({
                    "Product Name": title.strip(),
                    "Price": price.strip(),
                    "Product URL": link.strip(),
                    "Source": "Top Ranking"
                })
            except Exception:
                continue

        return results

    def quit(self):
        self.driver.quit()

if __name__ == "__main__":
    # 🌍 Add your proxy here if you have one (HTTP format)
    # Examples:
    # proxy = "http://username:password@123.123.123.123:8000"
    # proxy = "http://123.123.123.123:8000"
    proxy = None  # or replace with real proxy string

    scraper = AliExpressTopRankingScraper(proxy=proxy)
    print("🔍 Scraping AliExpress Top Ranking...")
    products = scraper.scrape_top_ranking()
    scraper.quit()

    df = pd.DataFrame(products)
    df.to_excel("aliexpress_top_products.xlsx", index=False)
    print(f"✅ Saved {len(df)} products to aliexpress_top_products.xlsx")
    print(df.head())
