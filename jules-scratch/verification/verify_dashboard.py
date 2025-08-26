from playwright.sync_api import sync_playwright, Page, expect

def run_verification(page: Page):
    """
    Navigates to the dashboard and takes a screenshot.
    """
    # Navigate to the running dev server
    page.goto("http://localhost:3000")

    # Wait for a key element to be visible to ensure the page has loaded
    # Based on the curl output, we expect this text on the page.
    loading_text = page.get_by_text("Sincronizando com o Ecossistema...")
    expect(loading_text).to_be_visible(timeout=10000) # 10 second timeout

    # Take a screenshot for visual verification
    page.screenshot(path="../jules-scratch/verification/dashboard.png")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        run_verification(page)
        browser.close()

if __name__ == "__main__":
    main()
