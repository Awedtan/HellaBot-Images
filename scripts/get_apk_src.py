from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()
        page.goto("https://www.biligame.com/detail/?id=101772", wait_until="networkidle")
        content = page.content()
        print(content)
        browser.close()

if __name__ == "__main__":
    main()
