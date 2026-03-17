from playwright.sync_api import Page, expect, sync_playwright

def verify_feature(page: Page):
    # Mock token for getAuthHeaders checks
    page.add_init_script("localStorage.setItem('token', 'mock_token');")

    # Intercept API calls to prevent malformed URL errors (https:///)
    page.route("**/*", lambda route: route.continue_())

    page.goto("http://localhost:5173/generate")
    page.wait_for_timeout(1000)

    # Check that progressbar exists
    progressbar = page.get_by_role("progressbar", name="Generation Progress")
    expect(progressbar).to_be_visible()

    # Check that it has 5 steps
    steps = progressbar.locator("div")
    expect(steps).to_have_count(5)

    # Check first step is active (aria-current="step")
    first_step = steps.first
    expect(first_step).to_have_attribute("aria-current", "step")

    # Take screenshot of the form with the progress bar
    page.screenshot(path="/app/verification.png", full_page=True)
    page.wait_for_timeout(500)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/app/video")
        page = context.new_page()
        try:
            verify_feature(page)
        finally:
            context.close()
            browser.close()
