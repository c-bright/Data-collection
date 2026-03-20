from multiprocessing import Process

from flask import Blueprint, jsonify, request

from app.crawler.scrapy_spiders.jd_scrapy_demo.run_spider_script import JdCrawler
from app.models.product_model import Product
from app.utils.database.db_manager import DatabaseManager


crawler_bp = Blueprint("product", __name__)
db_manager = DatabaseManager()
CRAWL_TASKS = {}


def _json_response(success, message, status, http_code=200, data=None):
    payload = {
        "success": success,
        "status": status,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    return jsonify(payload), http_code


def _normalize_keyword(raw_keyword):
    return str(raw_keyword or "").strip()


def _normalize_max_page(raw_max_page):
    try:
        value = int(raw_max_page)
    except (TypeError, ValueError):
        return 1
    return max(1, min(value, 10))


def _fetch_products_by_category(session, category):
    products = session.query(Product).filter(Product.category == category).all()
    return [product.to_dict() for product in products]


def _cleanup_finished_task(category):
    process = CRAWL_TASKS.get(category)
    if process and not process.is_alive():
        CRAWL_TASKS.pop(category, None)
    return process


def run_spider_subprocess(keyword, max_page):
    try:
        crawler = JdCrawler(keyword=keyword, max_page=max_page)
        crawler.run()
    except Exception as exc:
        print(f"爬虫进程异常: {exc}")
        raise


@crawler_bp.route("/crawl/start", methods=["POST"])
def start_crawl_task():
    session = None
    try:
        req_data = request.get_json(silent=True) or {}
        category = _normalize_keyword(req_data.get("keyword"))
        max_page = _normalize_max_page(req_data.get("max_page"))

        if not category:
            return _json_response(False, "关键词不能为空。", "error", 400)

        session = db_manager.get_session()
        cached_products = _fetch_products_by_category(session, category)
        if cached_products:
            return _json_response(
                True,
                f"命中关键词 [{category}] 的本地数据。",
                "completed",
                data=cached_products,
            )

        process = _cleanup_finished_task(category)
        if process and process.is_alive():
            return _json_response(
                True,
                f"关键词 [{category}] 的爬取任务正在执行中，请稍候。",
                "crawling",
            )

        process = Process(target=run_spider_subprocess, args=(category, max_page), daemon=True)
        process.start()
        CRAWL_TASKS[category] = process

        return _json_response(
            True,
            f"已启动关键词 [{category}] 的爬取任务，正在后台抓取。",
            "crawling",
        )
    except Exception as exc:
        return _json_response(False, f"启动爬虫失败: {exc}", "error", 500)
    finally:
        if session is not None:
            db_manager.Session.remove()


@crawler_bp.route("/crawl/status", methods=["GET"])
def check_crawl_status():
    session = None
    try:
        category = _normalize_keyword(request.args.get("keyword"))
        if not category:
            return _json_response(False, "缺少 keyword 参数。", "error", 400)

        session = db_manager.get_session()
        process = _cleanup_finished_task(category)

        if process and process.is_alive():
            return _json_response(
                True,
                f"关键词 [{category}] 的爬虫仍在执行中，请稍候。",
                "crawling",
            )

        if process and process.exitcode not in (None, 0):
            return _json_response(False, "爬虫执行失败。", "error", 500)

        products = _fetch_products_by_category(session, category)
        if products:
            return _json_response(
                True,
                f"关键词 [{category}] 的数据已准备完成。",
                "completed",
                data=products,
            )

        return _json_response(False, f"未找到关键词 [{category}] 的抓取结果。", "not_found", 404)
    except Exception as exc:
        return _json_response(False, f"查询爬虫状态失败: {exc}", "error", 500)
    finally:
        if session is not None:
            db_manager.Session.remove()
