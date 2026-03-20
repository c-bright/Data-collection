# Scrapy settings for jd_scrapy_demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "jd_scrapy_demo"

SPIDER_MODULES = ["app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.spiders"]
NEWSPIDER_MODULE = "app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.spiders"

LOG_LEVEL = 'ERROR'
# LOG_LEVEL = 'INFO'
# Crawl responsibly by identifying yourself (and your website) on the user-agent


# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs


REDIS_HOST = '192.168.211.132' # 填写虚拟机的 IP
REDIS_PORT = 6379
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/122.0.0.0 Safari/537.36'
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "jd_scrapy_demo.middlewares.JdScrapyDemoSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html

# selenium使用
DOWNLOADER_MIDDLEWARES = {
    'app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.middlewares.RandomUserAgentMiddleware': 400,
    'app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.middlewares.ListSeleniumMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
#
# # SELENIUM CONFIGURATION
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_ARGUMENTS = [
    '--disable-blink-features=AutomationControlled',
    '--window-size=1920,1080'
]

# 禁用 Scrapy 的关闭信号处理器，避开 Windows 的 _handleSignals 报错
INSTALL_SHUTDOWN_HANDLERS = False

# 确保 reactor 设置依然保留（有时需要这一行配合）
# ========================
#   Playwright 核心配置
# ========================

TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.pipelines.JsonPipeline": 300,
    "app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.pipelines.DatabasePipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
FEED_EXPORT_ENCODING = "utf-8"
