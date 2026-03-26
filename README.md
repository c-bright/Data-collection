# 📊 智能电商数据分析平台（Smart Data Platform）

一个基于 **Vue 3 + Flask + Scrapy / Playwright + MySQL** 的电商数据分析系统，实现从商品抓取到数据分析再到可视化展示的完整闭环。

---

## ✨ 项目亮点

* 🔐 用户登录 / 注册（前后端联动）
* 🔍 关键词驱动商品抓取（京东）
* 📦 商品详情 + 规格参数采集
* 💬 评论与标签数据抓取与清洗
* 📊 多维度数据分析（价格 / 店铺 / 评论）
* ☁️ 评论词云与标签可视化
* 🔄 前后端完整业务闭环（抓取 → 存储 → 分析 → 展示）

---

## 🏗️ 项目结构

```text
E:\test
├─ smart_data_platform_backend/    # 后端（Flask + 爬虫 + 分析）
└─ smart_data_platform_frontend/   # 前端（Vue 3 + ECharts）
```

---

## ⚙️ 技术栈

### 前端

* Vue 3 + Vite
* Vue Router
* Axios
* ECharts + echarts-wordcloud

### 后端

* Flask + SQLAlchemy
* Scrapy + Selenium + Playwright
* Pandas / 数据分析

### 数据层

* MySQL

---

## 🔄 核心流程

```text
登录系统
  ↓
输入关键词发起抓取
  ↓
爬虫抓取商品并存入数据库
  ↓
进入商品详情页
  ↓
抓取评论与标签
  ↓
生成分析数据
  ↓
前端展示图表（散点图 / 词云 / 柱状图）
```

---

## 🚀 快速启动

### 1️⃣ 启动后端

```bash
cd smart_data_platform_backend
pip install -r requirements.txt
python main.py
```

---

### 2️⃣ 启动前端

```bash
cd smart_data_platform_frontend
npm install
npm run dev
```

---

### 3️⃣ 配置数据库

编辑：

```text
app/utils/database/config.ini
```

---

## 🔌 核心接口

```http
POST /api/login
POST /api/register

POST /api/crawl/start
GET  /api/crawl/status

GET  /api/analysis/full/<product_id>
```

👉 其中 `/api/analysis/full` 为核心聚合接口（详情 + 分析）

---

## ⚠️ 注意事项

* 本项目用于学习 / 演示，不适用于生产环境
* 登录态为简化实现（localStorage）
* 爬虫依赖浏览器环境（Playwright / Selenium）
* 存在本地路径依赖（需调整）

---

## 🛠️ 后续优化方向

* 引入 JWT 鉴权机制
* 消除硬编码路径（改为 `.env`）
* 密码加密存储（hash）
* JSON 中间文件 → 数据库化
* Docker 一键部署
* 增加日志与异常处理

---

## 📌 项目说明

该项目适用于：

* 🎓 毕业设计 / 课程项目
* 📊 数据分析与可视化实践
* 🕷️ 爬虫系统开发学习
* 💼 作品集展示（前后端一体项目）

---
