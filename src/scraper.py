# NOTE FOR VERCEL DEPLOYMENT:
# Running Playwright with a self-hosted Chromium browser directly on Vercel Serverless Functions
# is generally not feasible due to:
# 1. Size Limits: Vercel functions have size limits (e.g., 50MB compressed), while Chromium is much larger (~280MB+).
# 2. Execution Time Limits: Serverless functions have maximum execution times (e.g., 10-60 seconds depending on the plan),
#    which might not be enough for browser startup and scraping tasks.
# 3. Filesystem: Serverless environments often have read-only filesystems, preventing Playwright from downloading browsers.
#
# RECOMMENDED ALTERNATIVE FOR VERCEL:
# Use a remote browser service (e.g., Browserless.io, BrightData Scraping Browser, etc.)
# You can connect to these services using Playwright's `connect_over_cdp` method.
# See the commented-out example below.

import asyncio
import json
import os # Import os to potentially read remote browser URL from env vars
import re
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def scrape_gsmarena(query):
    """
    Scrapes phone details from GSMArena based on a search query using Playwright.

    Args:
        query (str): The search query (e.g., "Xiaomi Redmi 10 2022").

    Returns:
        dict: A dictionary containing phone details, or an error message.
    """
    print(f"Starting scrape for: \"{query}\"")
    browser = None # Initialize browser variable
    try:
        async with async_playwright() as p:

            # --- VERCEL DEPLOYMENT NOTE --- 
            # The following `launch` command will likely FAIL on Vercel due to size/environment limits.
            # It's kept here for local execution or non-serverless environments.
            # browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
            # print("Launched local Chromium instance.")

            # --- EXAMPLE: Connecting to a Remote Browser Service (e.g., Browserless.io) --- 
            # Uncomment and replace with your actual remote browser service WebSocket endpoint.
            # You might get this endpoint from your service provider (e.g., wss://chrome.browserless.io?token=YOUR_API_TOKEN)
            # It's recommended to store the endpoint URL in environment variables.
            # REMOTE_BROWSER_ENDPOINT = os.getenv("REMOTE_BROWSER_ENDPOINT")
            # if not REMOTE_BROWSER_ENDPOINT:
            #     print("Error: REMOTE_BROWSER_ENDPOINT environment variable not set.")
            #     return {"error": "Remote browser endpoint not configured."}
            # print(f"Connecting to remote browser: {REMOTE_BROWSER_ENDPOINT}")
            # browser = await p.chromium.connect_over_cdp(REMOTE_BROWSER_ENDPOINT)
            # print("Connected to remote browser.")
            # --- END EXAMPLE ---

            # --- TEMPORARY ERROR FOR VERCEL --- 
            # Since direct launch fails and remote connection is commented out, return an error.
            # Remove this block if you implement the remote browser connection.
            print("Error: Direct browser launch is not supported in this Vercel environment. Configure a remote browser.")
            return {"error": "Browser launch method not configured for Vercel environment."}
            # --- END TEMPORARY ERROR ---

            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = await context.newPage()

            # --- Search for the phone ---
            search_url = f"https://www.gsmarena.com/res.php3?sSearch={query.replace(' ', '+')}"
            print(f"Navigating to search URL: {search_url}")
            await page.goto(search_url, wait_until='domcontentloaded', timeout=30000) # Increased timeout slightly

            search_results_selector = "div.makers ul li a"
            try:
                await page.wait_for_selector(search_results_selector, timeout=15000)
            except PlaywrightTimeoutError:
                print(f"Search results timeout or no results for query: \"{query}\"")
                return {"error": f"Search results took too long to load or no results found for query: \"{query}\"."}

            first_result_link_element = page.locator(search_results_selector).first
            first_result_title = await first_result_link_element.text_content()
            first_result_link = await first_result_link_element.get_attribute("href")

            if not first_result_link:
                print(f"No phone link found for query: \"{query}\"")
                return {"error": f"No phone found or link extraction failed for query: \"{query}\". Please try a different query."}

            phone_detail_url = first_result_link
            if not phone_detail_url.startswith('http'):
                base_url = 'https://www.gsmarena.com/'
                phone_detail_url = base_url + phone_detail_url.lstrip('/')

            print(f"Found \"{first_result_title.strip()}\". Navigating to details page: {phone_detail_url}")

            # --- Get phone details ---
            await page.goto(phone_detail_url, wait_until='domcontentloaded', timeout=20000) # Increased timeout

            specs_list_selector = "#specs-list"
            try:
                await page.wait_for_selector(specs_list_selector, timeout=10000)
            except PlaywrightTimeoutError:
                print(f"Details page timeout or specs list not found for: \"{first_result_title.strip()}\"")
                return {"error": f"Details page took too long to load or specs list not found for: \"{first_result_title.strip()}\"."}

            phone_details = {}

            phone_name_element = page.locator("h1.specs-phone-name-title")
            if await phone_name_element.count() > 0:
                phone_details["Phone Name"] = (await phone_name_element.text_content()).strip()
            else:
                phone_details["Phone Name"] = first_result_title.strip()

            image_element = page.locator(".specs-photo-main a img")
            if await image_element.count() > 0:
                img_src = await image_element.get_attribute("src")
                if img_src:
                    if not img_src.startswith('http'):
                        base_url = 'https://www.gsmarena.com/'
                        img_src = base_url + img_src.lstrip('/')
                    phone_details["Image URL"] = img_src

            specs_list_container = await page.query_selector(specs_list_selector)
            if specs_list_container:
                tables = await specs_list_container.query_selector_all("table")
                for table in tables:
                    category_element = await table.query_selector("th")
                    if not category_element: continue
                    category = (await category_element.text_content()).strip()
                    if not category: continue

                    phone_details[category] = {}
                    rows = await table.query_selector_all("tr")
                    for tr in rows:
                        key_element = await tr.query_selector("td.ttl")
                        value_element = await tr.query_selector("td.nfo")
                        if key_element and value_element:
                            key = (await key_element.text_content()).strip()
                            value = (await value_element.text_content()).strip()
                            if key and value:
                                phone_details[category][key] = value
                    if not phone_details[category]:
                        del phone_details[category]
            else:
                print(f"Warning: Specs list container ({specs_list_selector}) not found.")

            print(f"Scraping successful for: \"{query}\"")
            return phone_details

    except PlaywrightTimeoutError as e:
        print(f"A Playwright timeout error occurred: {e}")
        return {"error": f"Scraping process timed out. Query: \"{query}\". Error: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e}")
        return {"error": f"Scraping process failed: {e}. Query: \"{query}\""}
    finally:
        if browser and browser.is_connected():
            print("Closing browser connection.")
            await browser.close()

# Removed the main execution block (if __name__ == "__main__")

