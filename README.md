# Smart Data Platform

一个基于 **Vue 3**、**Flask**、**Scrapy / Playwright** 和 **MySQL** 的电商数据分析演示项目，包含商品抓取、评论分析与可视化展示完整流程。

## 功能特性

- 用户登录与注册
- 基于关键词的商品抓取
- 商品详情与规格参数获取
- 差评与标签抓取
- 商品分析看板
- 评论词云与标签可视化

## 技术栈

- 前端：Vue 3、Vite、Vue Router、Axios、ECharts
- 后端：Flask、SQLAlchemy、PyMySQL、Scrapy、Selenium、Playwright
- 数据库：MySQL

## 项目结构

```text
E:\test
├─ smart_data_platform_frontend/   # Vue 3 + Vite 前端
└─ smart_data_platform_backend/    # Flask + 爬虫 + 分析后端
```

## 核心流程

1. 登录系统
2. 输入关键词发起抓取任务
3. 后端抓取商品列表并写入 MySQL
4. 进入商品详情页
5. 抓取规格参数、评论和标签
6. 生成图表所需分析数据
7. 在前端展示商品分析与评论分析结果

## 接口概览

```http
POST /api/register
POST /api/login
POST /api/crawl/start
GET  /api/crawl/status?keyword=xxx
GET  /api/analysis/detail/<product_id>
GET  /api/analysis/full/<product_id>
POST /api/analysis/run
```

## 快速开始

### 1. 配置 MySQL

编辑：

```text
smart_data_platform_backend/app/utils/database/config.ini
```

### 2. 启动后端

```bash
cd smart_data_platform_backend
pip install -r requirements.txt
python main.py
```


### 3. 启动前端

```bash
cd smart_data_platform_frontend
npm install
npm run dev
```


## 说明

当前仓库主要用于学习、演示与交流使用。
