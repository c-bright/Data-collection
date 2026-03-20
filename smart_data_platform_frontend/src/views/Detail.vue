<template>
  <div class="page-shell">
    <section v-if="product" class="detail-grid">
      <article class="page-card info-card">
        <img class="hero-image" :src="product.image" :alt="product.name" />

        <div class="content-block">
          <p class="label">商品名称</p>
          <h2>{{ product.name }}</h2>
        </div>

        <div class="price-block">
          <span class="label">价格</span>
          <strong>{{ product.priceDisplay || `¥ ${Number(product.price).toLocaleString('zh-CN')}` }}</strong>
        </div>

        <div class="info-list">
          <div class="info-row">
            <span>店铺</span>
            <strong>{{ product.shop }}</strong>
          </div>
          <div class="info-row">
            <span>评论数</span>
            <strong>{{ product.commentCountDisplay || product.commentCount.toLocaleString('zh-CN') }}</strong>
          </div>
          <div class="info-row">
            <span>商品 ID</span>
            <strong>{{ product.productId }}</strong>
          </div>
          <div class="info-row">
            <span>分类</span>
            <strong>{{ product.category || '后端未返回' }}</strong>
          </div>
        </div>

        <a class="button-primary link-button" :href="product.link" target="_blank" rel="noreferrer">
          打开商品链接
        </a>

        <div class="analysis-tip" :class="state.dataSource">
          <strong>{{ sourceTitle }}</strong>
          <p>{{ state.analysisStatus.message }}</p>
        </div>
      </article>

      <article class="page-card params-card">
        <div class="section-title">
          <div>
            <h2>商品详细参数</h2>
            <p>右侧展示的是详情接口触发 `fetch_product_attributes()` 后返回的真实规格参数。</p>
          </div>
        </div>

        <ParamTable :params="product.params" />
      </article>
    </section>

    <section v-else class="page-card missing">
      <strong>{{ state.detailStatus.phase === 'error' ? '商品详情加载失败' : '正在读取商品详情' }}</strong>
      <p>{{ state.detailStatus.message }}</p>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import ParamTable from '../components/ParamTable.vue'
import { useAppStore } from '../store'

const route = useRoute()
const { state, loadProductBundle } = useAppStore()

const product = computed(() => state.currentProduct)

const sourceTitle = computed(() => {
  if (state.dataSource === 'loading') {
    return '正在调用后端分析接口'
  }
  if (state.dataSource === 'real') {
    return '分析页已切换为当前商品真实数据'
  }
  return '当前仍展示示例分析数据'
})

const syncProduct = async (id) => {
  await loadProductBundle(id)
}

onMounted(() => {
  syncProduct(route.params.id)
})

watch(
  () => route.params.id,
  (id) => {
    syncProduct(id)
  }
)
</script>

<style scoped>
.detail-grid {
  display: grid;
  grid-template-columns: minmax(320px, 0.95fr) minmax(0, 1.05fr);
  gap: 22px;
  align-items: stretch;
}

.info-card {
  display: flex;
  flex-direction: column;
  gap: 18px;
  height: 100%;
}

.hero-image {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.12), rgba(144, 247, 236, 0.22));
}

.content-block h2 {
  margin: 8px 0 0;
  line-height: 1.35;
}

.label {
  color: var(--text-soft);
  font-size: 0.9rem;
}

.price-block {
  padding: 18px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.12), rgba(144, 247, 236, 0.2));
}

.price-block strong {
  display: block;
  margin-top: 8px;
  font-size: 2rem;
  color: var(--accent-strong);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(31, 169, 122, 0.05);
  border: 1px solid rgba(31, 169, 122, 0.08);
}

.link-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.analysis-tip {
  padding: 18px;
  border-radius: 22px;
}

.analysis-tip strong {
  display: block;
  margin-bottom: 8px;
}

.analysis-tip p {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.65;
}

.analysis-tip.sample {
  background: rgba(31, 169, 122, 0.08);
}

.analysis-tip.loading {
  background: rgba(255, 214, 102, 0.22);
}

.analysis-tip.real {
  background: rgba(84, 160, 255, 0.14);
}

.params-card {
  height: 100%;
  overflow: auto;
}

.missing {
  min-height: 320px;
  display: grid;
  place-items: center;
  text-align: center;
}

@media (max-width: 960px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .params-card {
    max-height: none;
  }
}
</style>
