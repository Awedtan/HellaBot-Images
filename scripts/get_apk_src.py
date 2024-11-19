from playwright.sync_api import sync_playwright


def main():
    retries = 5
    for attempt in range(retries):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(args=["--no-sandbox"])
                page = browser.new_page()
                page.goto("https://www.biligame.com/detail/?id=101772",
                          wait_until="networkidle", timeout=90000)
                content = page.content()
                print(content)
                browser.close()
                break
        except Exception as e:
            print(f'Attempt {attempt + 1} failed: {e}')
            if attempt == retries - 1:
                print(f'Failed to download apk after {retries} attempts.')


if __name__ == "__main__":
    main()
