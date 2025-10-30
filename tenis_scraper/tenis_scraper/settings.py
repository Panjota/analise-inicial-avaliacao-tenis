# Scrapy settings for tenis_scraper project

BOT_NAME = "tenis_scraper"

SPIDER_MODULES = ["tenis_scraper.spiders"]
NEWSPIDER_MODULE = "tenis_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure delays
DOWNLOAD_DELAY = 2.0
RANDOMIZE_DOWNLOAD_DELAY = True

# Configure concurrent requests
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Configure retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Configure AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# Configure middlewares
DOWNLOADER_MIDDLEWARES = {
    "tenis_scraper.middlewares.RandomUserAgentMiddleware": 400,
    "tenis_scraper.middlewares.AmazonUserAgentMiddleware": 401,  # Para spider da Amazon
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
}

SPIDER_MIDDLEWARES = {
    "tenis_scraper.middlewares.DefaultContextMiddleware": 543,
}

# Configure pipelines
ITEM_PIPELINES = {
    "tenis_scraper.pipelines.CleanAndValidatePipeline": 300,
    "tenis_scraper.pipelines.DuplicatesPipeline": 400,
}

# Configure feeds
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    'data/raw/%(name)s_%(time)s.csv': {
        'format': 'csv',
        'overwrite': True,
    }
}

# Request fingerprinting
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
