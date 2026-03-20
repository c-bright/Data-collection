import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JDCrawler:
    def __init__(self):
        edge_driver_path = r"E:\test\smart_data_platform_backend\app\crawler\msedgedriver.exe"
        options = Options()

        # 1. 复用用户数据目录 (保存登录态)
        options.add_argument(r"--user-data-dir=E:\SeleniumProfile")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--window-size=1920,1080")

        # 2. 屏蔽自动化特征
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 注意：这里不再硬编码 UA，由中间件动态注入

        service = Service(edge_driver_path)
        self.driver = webdriver.Edge(service=service, options=options)

        # 3. 核心：使用 CDP 在页面加载前抹除 webdriver 特征
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

    def scroll_to_bottom(self, steps=8):
        """
        模拟真人平滑滚动，触发京东懒加载
        """
        current_position = 0
        for i in range(steps):
            distance = random.randint(400, 800)
            current_position += distance
            self.driver.execute_script(f"window.scrollTo({{top: {current_position}, behavior: 'smooth'}});")

            time.sleep(random.uniform(0.8, 1.5))
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if current_position >= new_height:
                break
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(random.uniform(1, 2))
        print("已完成模拟真人滚动")

    def close(self):
        """
        关闭浏览器
        """
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    jd = JDCrawler()
    jd.search("平板")       # ✅ 调用 search 方法
    # jd.scroll_to_bottom()
    jd.close()