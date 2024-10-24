import zipfile  # Import the zipfile module
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
# Set up proxy details
proxy_host = "p.webshare.io:80"
proxy_username = "ljayoggy-JP-rotate"
proxy_password = "kfk2b2al877m"

# Configure the proxy with authentication for Selenium
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version": "22.0.0"
}
"""

background_js = f"""
var config = {{
        mode: "fixed_servers",
        rules: {{
          singleProxy: {{
            scheme: "http",
            host: "{proxy_host.split(':')[0]}",
            port: parseInt({proxy_host.split(':')[1]})
          }},
          bypassList: []
        }}
      }};
chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{proxy_username}",
            password: "{proxy_password}"
        }}
    }};
}}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {{urls: ["<all_urls>"]}},
    ['blocking']
);
"""

# Set up Chrome options
chrome_options = Options()
pluginfile = 'proxy_auth_plugin.zip'

with zipfile.ZipFile(pluginfile, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)

chrome_options.add_extension(pluginfile)

# Create WebDriver instance with proxy settings
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to an IP-checking website to see the proxy in action
    driver.get("http://httpbin.org/ip")
    sleep(5)
    print("Page Source:\n", driver.page_source)
finally:
    driver.quit()
