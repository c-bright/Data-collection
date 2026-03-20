from flask import Blueprint, jsonify, request

from app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.selenium_spiders.datil import JDBadReviewScraper
from app.services.analysis_service import ScatterCommentService
from app.analysis.test_1 import FrontendDataService
from app.utils.database.db_manager import DatabaseManager
from app.services.data_service import JDReviewProcessor


db_manager = DatabaseManager()
analysis_bp = Blueprint("analysis", __name__)


def _json_response(success, message, http_code=200, data=None):
    payload = {
        "success": success,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    return jsonify(payload), http_code


def _normalize_product_id(raw_product_id):
    return str(raw_product_id or "").strip()


def _get_product_or_404(product_id):
    base_info = db_manager.get_formatted_product(product_id)
    if not base_info:
        return None, _json_response(
            False,
            f"数据库中未找到商品 ID 为 {product_id} 的详情数据。",
            404,
        )
    return base_info, None


def _fetch_detailed_params(product_id):
    scraper = JDBadReviewScraper(product_id)
    return scraper.fetch_product_attributes() or {}


def build_analysis_result(product_id):
    print(f"[{product_id}] 开始爬取差评和标签...")
    scraper = JDBadReviewScraper(product_id)
    scraper.execute_crawl()

    print(f"[{product_id}] 开始清洗评论和标签数据...")
    processor = JDReviewProcessor()
    processor.process()

    print(f"[{product_id}] 开始生成散点和评论JSON...")
    service = ScatterCommentService()
    service.save_json()

    print(f"[{product_id}] 开始生成前端可视化JSON...")
    frontend = FrontendDataService()
    return frontend.save_frontend_json()

@analysis_bp.route("/analysis/run", methods=["POST"])
def run_analysis():
    try:
        req_data = request.get_json(silent=True) or {}
        product_id = _normalize_product_id(req_data.get("product_id"))
        if not product_id:
            return _json_response(False, "缺少 product_id。", 400)

        visual_data = build_analysis_result(product_id)

        return _json_response(
            True,
            "全流程分析完成。",
            data={
                "product_id": product_id,
                "status": "completed",
                "result": visual_data,
            },
        )
    except Exception as exc:
        return _json_response(False, f"启动分析失败: {exc}", 500)


@analysis_bp.route("/analysis/full/<product_id>", methods=["GET"])
def get_product_full_data(product_id):
    try:
        product_id = _normalize_product_id(product_id)
        if not product_id:
            return _json_response(False, "缺少 product_id。", 400)

        base_info, error_response = _get_product_or_404(product_id)
        if error_response:
            return error_response

        detailed_params = _fetch_detailed_params(product_id)
        visual_data = build_analysis_result(product_id)

        return _json_response(
            True,
            "详情、详细参数与分析结果获取成功。",
            data={
                "product_id": product_id,
                "detail": {
                    **base_info,
                    "detailed_params": detailed_params,
                },
                "analysis": {
                    "status": "completed",
                    "result": visual_data,
                },
            },
        )
    except Exception as exc:
        return _json_response(False, f"详情与分析获取失败: {exc}", 500)


@analysis_bp.route("/analysis/detail/<product_id>", methods=["GET"])
def get_product_detail(product_id):
    try:
        product_id = _normalize_product_id(product_id)
        if not product_id:
            return _json_response(False, "缺少 product_id。", 400)

        base_info, error_response = _get_product_or_404(product_id)
        if error_response:
            return error_response

        detailed_params = _fetch_detailed_params(product_id)

        detail_data = {
            **base_info,
            "detailed_params": detailed_params,
        }

        return _json_response(True, "商品详情获取成功。", data=detail_data)
    except Exception as exc:
        return _json_response(False, f"服务器查询异常: {exc}", 500)
