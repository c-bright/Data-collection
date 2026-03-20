import requests

url = "http://127.0.0.1:5000/api/start-crawl"

data = {
    "keyword": "手机",
    "max_page": 3
}




"""

{
    "data": {
        "CPU型号": "A19 Pro",
        "充电功率": "40W",
        "入网型号": "A3527",
        "前摄主像素": "1800万像素",
        "包装清单": "装有 iOS 26 的 iPhone\nUSB-C 充电线 (1 米)",
        "后摄2-超广角像素": "4800万像素",
        "后摄3-长焦像素": "4800万像素",
        "后摄主像素": "4800万像素",
        "品牌": "Apple",
        "商品编号": "100278221408",
        "国补备案型号": "MG044CH/A",
        "屏幕分辨率": "FHD+",
        "屏幕尺寸": "6.86英寸",
        "屏幕材质": "OLED全面屏",
        "无线充电": "以官网信息为准",
        "机型": "Apple iPhone 17 Pro Max",
        "机身内存": "256GB",
        "机身尺寸": "长163.4mm 宽78mm 厚8.75mm",
        "机身重量": "231g",
        "机身颜色": "星宇橙色",
        "特征特质": "无",
        "系统": "iOS"
    },
    "error_code": null,
    "message": "获取商品属性成功",
    "success": true
    """

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())