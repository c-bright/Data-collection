from playwright.sync_api import sync_playwright
import json


def save_jd_cookies():
    with sync_playwright() as p:
        # 必须开启 headless=False，否则你没法扫码登录
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("正在打开京东登录页，请在弹出窗口中完成扫码登录...")
        page.goto("https://passport.jd.com/new/login.aspx")

        # 等待登录成功的标志性元素（例如首页的“退出”按钮或用户名显示）
        # 这里给 60 秒时间让你操作手机扫码
        try:
            page.wait_for_selector(".nickname", timeout=60000)
            print("登录成功！正在保存 Cookie...")

            # 获取当前上下文的所有 Cookie
            cookies = context.cookies()
            with open("auth.json", "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=4)

            print("Cookie 已成功保存到 auth.json")
        except Exception as e:
            print(f"登录超时或失败: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    save_jd_cookies()