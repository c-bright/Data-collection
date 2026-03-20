import os
import time
import random
import json
from playwright.sync_api import sync_playwright
from app.services.analysis_service import ScatterCommentService
try:
    from playwright_stealth import stealth_sync
except ImportError:
    def stealth_sync(page):
        pass


class JDBadReviewScraper:

    def __init__(self, product_id: str, auth_file="auth.json"):
        self.target_url = self.target_url = f"https://item.jd.com/{product_id}.html"
        self.target_dir = r"E:\test\smart_data_platform_backend\app\utils"
        self.auth_file = os.path.join(self.target_dir, auth_file)
        self.extracted_comments = []
        self.extracted_tags = []
        self.product_id = product_id

    def is_login_page(self, page):
        current_url = page.url or ""
        content = page.content()
        return (
            "passport.jd.com" in current_url
            or "login.jd.com" in current_url
            or "登录注册" in content
            or "账号密码登录" in content
            or "手机验证码登录" in content
            or "京东登录注册" in content
        )

    def wait_for_manual_login(self, page, context, timeout_seconds=180):
        print(f"检测到登录页，请在 {timeout_seconds} 秒内完成登录...")
        deadline = time.time() + timeout_seconds

        while time.time() < deadline:
            time.sleep(2)
            try:
                if not self.is_login_page(page):
                    print("检测到登录成功，正在保存新的登录态...")
                    context.storage_state(path=self.auth_file)
                    time.sleep(2)
                    return
            except Exception:
                pass

        raise TimeoutError("manual login timeout")

    def ensure_logged_in(self, page, context, target_url):
        if not self.is_login_page(page):
            return

        self.wait_for_manual_login(page, context)
        page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        if self.is_login_page(page):
            self.wait_for_manual_login(page, context)
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

    def fetch_product_attributes(self):
        print(f"[Mode: Detail] 准备抓取商品: {self.product_id}")
        attributes_data = {}

        with sync_playwright() as p:
            # 1. 启动配置
            browser = p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])

            context_args = {}
            if os.path.exists(self.auth_file):
                context_args["storage_state"] = self.auth_file
                print(">>> 已加载本地 auth.json 登录态")

            context = browser.new_context(**context_args, viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            stealth_sync(page)

            try:
                # 2. 访问页面
                page.goto(self.target_url, wait_until="domcontentloaded", timeout=60000)
                self.ensure_logged_in(page, context, self.target_url)

                # 3. 处理登录/SSO 同步 (sso.jkcsjd.com)
                if "passport.jd.com" in page.url or "sso.jkcsjd.com" in page.url:
                    print("🚨 检测到登录跳转，请在 90 秒内完成操作（或观察同步完成）...")
                    try:
                        # 动态等待回到商品页
                        page.wait_for_url(f"**/{self.product_id}.html", timeout=90000)
                        print("🎉 同步成功，正在保存新 Cookie...")
                        context.storage_state(path=self.auth_file)
                    except:
                        print("❌ 登录或同步超时。")
                        return {}
                time.sleep(5)
                # 4. 精准滚动触发渲染
                # 京东详情页必须看到锚点才会加载规格参数接口
                anchor_selector = "#sx-product-detail"
                print(f">>> 正在定位锚点并执行滚动: {anchor_selector}")

                # 等待锚点挂载
                page.wait_for_selector(anchor_selector, state="attached", timeout=15000)
                # 使用 Playwright 的原生滚动，比 wheel 更可靠
                page.locator(anchor_selector).scroll_into_view_if_needed()

                # 额外补偿滚动，确保容器完全进入视口
                page.mouse.wheel(0, 1000)
                print(">>> 已触发详情区域渲染，等待数据生成...")
                page.wait_for_timeout(3000)

                # 5. 提取规格参数
                # 根据 HTML 结构：#product-attribute 是父容器，.item 是每一行
                item_selector = "#product-attribute .item"
                try:
                    page.wait_for_selector(item_selector, timeout=10000)
                except:
                    print("⚠️ 未能在视口内发现规格参数行，可能是由于未完全加载。")

                all_items = page.locator(item_selector).all()
                for item in all_items:
                    # 嵌套定位：.label 下的 .text，.value 下的 .text
                    label_node = item.locator('.label .text').first
                    value_node = item.locator('.value .text').first

                    if label_node.count() > 0 and value_node.count() > 0:
                        # 清洗 key：去掉中文冒号
                        key = label_node.inner_text().strip().replace("：", "").replace(":", "")
                        # 优先取 title (防止页面显示为“...”)，否则取 text
                        val = value_node.get_attribute("title") or value_node.inner_text().strip()

                        if key:
                            attributes_data[key] = val

                print(f"✅ 成功抓取到 {len(attributes_data)} 项规格参数。")

            except Exception as e:
                print(f"❌ 运行崩溃: {e}")
                page.screenshot(path="final_debug.png")
            finally:
                browser.close()

        return attributes_data


    def execute_crawl(self, scroll_limit=7):

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)

            context = browser.new_context(
                storage_state=self.auth_file,
                viewport={"width": 1280, "height": 900}
            )

            page = context.new_page()

            stealth_sync(page)

            page.goto(self.target_url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            self.ensure_logged_in(page, context, self.target_url)

            # ===== 进入评价页 =====
            comment_entry = page.locator("div.all-btn").first
            for _ in range(8):
                try:
                    if comment_entry.is_visible():
                        comment_entry.scroll_into_view_if_needed()
                        page.wait_for_timeout(500)
                        comment_entry.click()
                        break
                except:
                    pass
                page.mouse.wheel(0, 600)
                page.wait_for_timeout(1000)

            self.ensure_logged_in(page, context, self.target_url)

            page.wait_for_timeout(3000)

            # ===== 提取汇总标签 =====
            page.wait_for_timeout(2000)
            tag_locators = page.locator('div[class*="_tag_rgt"]').all()
            self.extracted_tags = []
            for tag in tag_locators:
                name_el = tag.locator('span[class*="_tag-name"]')
                val_el = tag.locator('span[class*="_tag-comment"]')
                if name_el.count() > 0:
                    self.extracted_tags.append({
                        "name": name_el.inner_text().strip(),
                        "value": val_el.inner_text().strip() if val_el.count() > 0 else "0"
                    })

            # ===== 点击差评 =====
            bad_tag = page.locator('div[class*="_tag_rgt"]').filter(has_text="差评").first
            if not bad_tag.is_visible():
                print("该商品暂无差评")
                self.extracted_tags.append({"name": "result_tag", "value": "没有差评"})
                browser.close()
                return

            print("开启差评模式")
            bad_tag.click()
            page.wait_for_timeout(3000)
            page.wait_for_selector('[data-virtuoso-scroller="true"]')

            # ===== 评论容器 =====
            container = page.locator('[data-virtuoso-scroller="true"]')
            container.scroll_into_view_if_needed()

            seen_comments = set()
            last_count = 0
            no_new_count = 0

            for i in range(scroll_limit):
                try:
                    # 模拟人工滚动
                    container.hover()
                    page.mouse.wheel(0, random.randint(1200, 1600))
                    page.wait_for_timeout(int(random.uniform(1.6, 2.3) * 1000))

                    comments = container.locator("span.jdc-pc-rate-card-main-desc")
                    all_comments = [comments.nth(j).inner_text().strip() for j in range(comments.count())]

                    for text in all_comments:
                        if text and text not in seen_comments:
                            seen_comments.add(text)
                            self.extracted_comments.append(text)

                    # ===== 如果连续两次没有新增评论，提前结束 =====
                    if len(self.extracted_comments) == last_count:
                        no_new_count += 1
                        if no_new_count >= 2:
                            print("连续两次没有新增评论，滚动结束")
                            break
                    else:
                        no_new_count = 0

                    last_count = len(self.extracted_comments)

                except Exception as e:
                    print(f"第{i + 1}次滚动异常: {e}")

            browser.close()


            # ===== 保存 JSON =====
            json_file = os.path.join(self.target_dir, 'datil.json')
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump({
                    "tags": self.extracted_tags,
                    "comments": self.extracted_comments
                }, f, ensure_ascii=False, indent=2)

            print(f"\n共抓取 {len(self.extracted_comments)} 条差评")
            print(f"保存到 JSON: {json_file}")




if __name__ == "__main__":

    SCRAPER = JDBadReviewScraper('100278221408')
    # SCRAPER.fetch_product_attributes()
    SCRAPER.execute_crawl(scroll_limit=7)  # 可以根据需要调整
