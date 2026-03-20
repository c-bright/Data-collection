# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter




class JdScrapyDemoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class JdScrapyDemoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


from .selenium_spiders.login import JDCrawler
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

import time
import random
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest  # 导入忽略请求异常
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ListSeleniumMiddleware:
    def __init__(self):
        # 延迟导入，确保爬虫启动时才初始化驱动
        from app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.selenium_spiders.login import JDCrawler
        self.jd_selenium = JDCrawler()

    @classmethod
    def from_crawler(cls, crawler):
        mw = cls()
        crawler.signals.connect(mw.spider_closed, signal=signals.spider_closed)
        return mw

    def process_request(self, request, spider):
        if not request.meta.get("use_selenium_list"):
            return None

        current_page = request.meta.get('page', 1)
        spider.logger.info(f"[Selenium] 正在处理第 {current_page} 页")

        # 1. 动态同步 UA (确保 Selenium 和 Scrapy 请求一致)
        ua = request.headers.get('User-Agent', b'').decode('utf-8')
        self.jd_selenium.driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua})

        try:
            if current_page == 1:
                # 注入 Cookie
                if "jd.com" not in self.jd_selenium.driver.current_url:
                    self.jd_selenium.driver.get("https://www.jd.com/")
                if request.cookies:
                    for name, value in request.cookies.items():
                        self.jd_selenium.driver.add_cookie({'name': name, 'value': value})

                self.jd_selenium.driver.get(request.url)
                time.sleep(random.uniform(2, 4))
                self.ensure_logged_in(spider, request.url)
            else:
                self.ensure_logged_in(spider, request.url)
                self.navigate_with_pagination(spider, request.url, current_page)

            # 2. 风险检测 (增加手动校验的健壮性)
            if "risk_handler" in self.jd_selenium.driver.current_url:
                spider.logger.error("🛑 触发验证码！请在 60 秒内手动完成...")
                # 增加更频繁的检查
                for i in range(120):  # 最长等 120 次 * 0.5s = 60s
                    time.sleep(0.5)
                    if "risk_handler" not in self.jd_selenium.driver.current_url:
                        spider.logger.info("✅ 验证已通过")
                        break
                else:
                    # 如果 60 秒没过，直接放弃本次请求，防止卡死
                    raise IgnoreRequest("验证码超时未处理")

            # 3. 触发懒加载滚动
            spider.logger.info("触发懒加载滚动...")
            self.jd_selenium.scroll_to_bottom(5)
            time.sleep(1.5)

            content = self.jd_selenium.driver.page_source
            return HtmlResponse(
                url=self.jd_selenium.driver.current_url,
                body=content,
                encoding="utf-8",
                request=request
            )

        except Exception as e:
            spider.logger.error(f"[Selenium] 严重错误: {e}")
            self.jd_selenium.driver.save_screenshot(f"error_page_{current_page}.png")
            raise IgnoreRequest(f"Selenium request failed on page {current_page}: {e}")

    def ensure_logged_in(self, spider, target_url):
        if not self.is_login_page():
            return

        spider.logger.error("检测到已跳转到京东登录页，请在复用浏览器中完成登录。")
        self.wait_for_manual_login(spider, timeout_seconds=180)
        self.jd_selenium.driver.get(target_url)
        time.sleep(random.uniform(2, 4))

        if self.is_login_page():
            spider.logger.error("登录后重新访问目标页时仍处于登录页。")
            self.wait_for_manual_login(spider, timeout_seconds=180)
            self.jd_selenium.driver.get(target_url)
            time.sleep(random.uniform(2, 4))

    def navigate_with_pagination(self, spider, target_url, current_page):
        for attempt in range(2):
            spider.logger.info(f"正在执行第 {current_page} 页的翻页动作，第 {attempt + 1} 次尝试")
            self.scroll_to_pagination_area()
            self.execute_pagination(spider)

            if self.is_login_page():
                spider.logger.error("翻页过程中跳转到登录页，等待登录完成后重新执行本次翻页。")
                self.wait_for_manual_login(spider, timeout_seconds=180)
                self.jd_selenium.driver.get(target_url)
                time.sleep(random.uniform(2, 4))
                continue

            return

        raise IgnoreRequest(f"pagination interrupted by login on page {current_page}")

    def scroll_to_pagination_area(self):
        self.jd_selenium.driver.execute_script(
            """
            const pager =
              document.querySelector('.pn-next') ||
              document.querySelector('a.fp-next') ||
              document.querySelector('[class*="_pagination_next"]') ||
              document.querySelector('.page') ||
              document.querySelector('.p-wrap');

            if (pager) {
              pager.scrollIntoView({behavior: 'auto', block: 'center'});
              window.scrollBy(0, -160);
            } else {
              window.scrollBy(0, window.innerHeight * 0.55);
            }
            """
        )
        time.sleep(random.uniform(0.8, 1.4))

    def is_login_page(self):
        current_url = self.jd_selenium.driver.current_url or ""
        page_source = self.jd_selenium.driver.page_source or ""
        return (
            "passport.jd.com" in current_url
            or "login.jd.com" in current_url
            or "扫码登录" in page_source
            or "账号登录" in page_source
            or "京东账号登录" in page_source
        )

    def wait_for_manual_login(self, spider, timeout_seconds=120):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            time.sleep(2)
            if not self.is_login_page():
                spider.logger.info("检测到登录已完成，继续抓取流程。")
                time.sleep(2)
                return
        raise IgnoreRequest("manual login timeout")

    def execute_pagination(self, spider):
        """稳健翻页逻辑"""
        xpath = (
            '//a[contains(@class,"pn-next") and not(contains(@class,"disabled"))] | '
            '//a[contains(@class,"_pagination_next") and not(contains(@class,"disabled"))] | '
            '//a[@class="fp-next" and not(contains(@class,"disabled"))] | '
            '//a[contains(normalize-space(.), "下一页") and not(contains(@class,"disabled"))]'
        )

        old_url = self.jd_selenium.driver.current_url
        old_source = self.jd_selenium.driver.page_source[:2000]
        last_error = None

        for attempt in range(1, 4):
            try:
                wait = WebDriverWait(self.jd_selenium.driver, 12)
                next_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

                self.jd_selenium.driver.execute_script(
                    """
                    const blockers = Array.from(document.querySelectorAll(
                      '.jdm-tips, .ui-tips, .mod_loading, .search-loading, .mask-layer, .dialog, .popup, .notice, .coupon-pop'
                    ));
                    blockers.forEach(el => {
                      el.style.display = 'none';
                      el.style.pointerEvents = 'none';
                    });
                    """,
                )

                self.jd_selenium.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                    next_btn
                )
                time.sleep(1 + attempt * 0.5)

                classes = next_btn.get_attribute("class") or ""
                if "disabled" in classes:
                    raise IgnoreRequest("pagination button is disabled")

                self.jd_selenium.driver.execute_script("arguments[0].click();", next_btn)

                wait.until(
                    lambda d: d.current_url != old_url or d.page_source[:2000] != old_source
                )
                time.sleep(random.uniform(2.5, 4))
                return

            except (TimeoutException, StaleElementReferenceException, IgnoreRequest) as e:
                last_error = e
                spider.logger.warning(f"翻页第 {attempt} 次尝试失败: {e}")
                time.sleep(1.2)
            except Exception as e:
                last_error = e
                spider.logger.warning(f"翻页第 {attempt} 次尝试异常: {e}")
                time.sleep(1.2)

        spider.logger.error(f"翻页点击动作失败: {last_error}")
        raise IgnoreRequest(f"pagination failed: {last_error}")

    def spider_closed(self, spider):
        self.jd_selenium.driver.quit()

class RandomUserAgentMiddleware:
    DESKTOP_USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.185 Safari/537.36",
    ]

    def __init__(self):
        self._last_ua = self.DESKTOP_USER_AGENTS[0]

    def process_request(self, request, spider):
        self._last_ua = random.choice(self.DESKTOP_USER_AGENTS)
        request.headers['User-Agent'] = self._last_ua



