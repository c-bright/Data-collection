import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


def warm_up():
    # 1. 路径配置（确保与你的爬虫配置完全一致）
    edge_driver_path = r"E:\test\smart_data_platform_backend\app\crawler\msedgedriver.exe"
    user_data_dir = r"E:\SeleniumProfile"

    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # 2. 关键：移除自动化检测，方便登录
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=options)

    # 3. 屏蔽 webdriver 特征
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        print("正在打开京东，请执行以下操作：")
        print("1. 手动点击登录并完成扫码/验证码登录")
        print("2. 确认地址（左上角）是否正确")
        print("3. 随便搜索一个商品并浏览，确保没有弹出滑块")

        driver.get("https://www.jd.com")

        # 给自己充足的时间进行手动操作
        # 操作完成后，在控制台按 Ctrl+C 或者直接关闭浏览器
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("检测到退出，正在保存环境并关闭浏览器...")
    finally:
        driver.quit()


if __name__ == "__main__":
    warm_up()
