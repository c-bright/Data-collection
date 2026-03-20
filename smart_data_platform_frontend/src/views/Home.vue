<template>
  <div class="page-shell">
 

    <section class="page-card">
      <div class="section-title">
        <div>
          <h2>模块总览</h2>
          <p>通过横向滑动浏览系统中的 5 个核心模块。</p>
        </div>

        <div class="actions">
          <button class="button-secondary" type="button" @click="scrollByCard(-1)">上一张</button>
          <button class="button-primary" type="button" @click="scrollByCard(1)">下一张</button>
        </div>
      </div>

      <div ref="carouselRef" class="carousel">
        <article v-for="card in cards" :key="card.title" class="feature-card">
          <div class="icon-badge">{{ card.icon }}</div>
          <h3>{{ card.title }}</h3>
          <p>{{ card.desc }}</p>

          <div class="keyword-list">
            <span v-for="tag in card.tags" :key="tag">{{ tag }}</span>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const carouselRef = ref(null)

const cards = [
  {
    icon: 'SYS',
    title: '系统介绍',
    desc: '介绍平台如何将商品采集、详情查看与分析看板串成完整闭环，帮助用户快速理解前端工作台的功能边界。',
    tags: ['平台概览', '工作流', '引导入口']
  },
  {
    icon: 'CRW',
    title: '商品爬取功能',
    desc: '通过关键词和页数创建爬取任务，页面通过轮询方式展示任务进度，并将结果以 12 个一页的商品卡片形式呈现。',
    tags: ['关键词', '轮询状态', '分页列表']
  },
  {
    icon: 'DTL',
    title: '商品详情功能',
    desc: '详情页聚合商品大图、价格、评论数、店铺信息与规格参数，同时承担触发分析任务的重要角色。',
    tags: ['基础信息', '参数展示', '分析触发']
  },
  {
    icon: 'ANL',
    title: '数据分析能力',
    desc: '平台从商品与评论两条视角提供分析看板，支持散点图、柱状图、饼图与词云的统一卡片化展示。',
    tags: ['商品分析', '评论分析', '图表动画']
  },
  {
    icon: 'TEC',
    title: '技术特点',
    desc: '采用明亮自然的青绿色视觉系统、卡片式布局、页面淡入动效和统一图表容器，为后续接入真实后端预留清晰扩展点。',
    tags: ['Vue 3', 'ECharts', '可扩展']
  }
]

const scrollByCard = (direction) => {
  if (!carouselRef.value) {
    return
  }

  const step = carouselRef.value.clientWidth * 0.72
  carouselRef.value.scrollBy({
    left: step * direction,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1.3fr 0.9fr;
  gap: 22px;
  background:
    linear-gradient(135deg, rgba(31, 169, 122, 0.12), rgba(144, 247, 236, 0.18)),
    var(--card-bg);
}

.hero-copy h2 {
  margin: 0 0 14px;
  font-size: clamp(2rem, 4vw, 2.8rem);
  line-height: 1.15;
}

.hero-copy p:last-child {
  margin: 0;
  line-height: 1.75;
  color: var(--text-soft);
  max-width: 60ch;
}

.hero-eyebrow {
  margin: 0 0 10px;
  font-size: 0.8rem;
  color: var(--accent-strong);
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.hero-orbit {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  align-self: center;
}

.orbit-card {
  min-height: 150px;
  display: grid;
  place-items: center;
  text-align: center;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(31, 169, 122, 0.12);
}

.orbit-card strong {
  display: block;
  font-size: 2rem;
  color: var(--accent-strong);
}

.orbit-card span {
  color: var(--text-soft);
}

.actions {
  display: flex;
  gap: 10px;
}

.carousel {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(280px, 33%);
  gap: 18px;
  overflow-x: auto;
  padding-bottom: 6px;
  scroll-snap-type: x mandatory;
}

.carousel::-webkit-scrollbar {
  height: 8px;
}

.carousel::-webkit-scrollbar-thumb {
  background: rgba(31, 169, 122, 0.24);
  border-radius: 999px;
}

.feature-card {
  scroll-snap-align: start;
  min-height: 280px;
  padding: 24px;
  border-radius: 26px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(245, 253, 250, 0.92));
  border: 1px solid rgba(31, 169, 122, 0.1);
  box-shadow: var(--shadow-soft);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.icon-badge {
  width: 68px;
  height: 68px;
  border-radius: 22px;
  display: grid;
  place-items: center;
  font-weight: 800;
  color: #0d5f48;
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.16), rgba(144, 247, 236, 0.22));
}

.feature-card h3 {
  margin: 20px 0 12px;
  font-size: 1.18rem;
}

.feature-card p {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.7;
}

.keyword-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 18px;
}

.keyword-list span {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(31, 169, 122, 0.1);
  color: #0f6b52;
  font-size: 0.86rem;
}

@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-orbit,
  .carousel {
    grid-auto-columns: minmax(260px, 85%);
  }

  .actions {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .hero-orbit {
    grid-template-columns: 1fr;
  }

  .actions {
    flex-direction: column;
  }
}
</style>
