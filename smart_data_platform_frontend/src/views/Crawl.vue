<template>
  <div class="page-shell">
    <section class="page-card">
      <div class="section-title">
        <div>
          <h2>创建爬取任务</h2>
          <p>该页面已接入后端 `/api/crawl/start` 与 `/api/crawl/status`，会真实轮询任务状态。</p>
        </div>
      </div>

      <div class="toolbar">
        <div class="field">
          <label class="field-label" for="keyword">关键词</label>
          <input id="keyword" v-model="keyword" class="input-base" placeholder="例如：笔记本电脑、手机、空气炸锅" />
        </div>

        <div class="field field-small">
          <label class="field-label" for="page">页数</label>
          <input id="page" v-model.number="page" class="input-base" type="number" min="1" max="10" />
        </div>

        <button class="button-primary action-button" type="button" :disabled="isRunning" @click="start">
          {{ isRunning ? '任务运行中...' : '开始爬取' }}
        </button>
      </div>
    </section>

    <StatusPanel
      title="爬取任务状态"
      :status="state.crawlStatus.phase"
      :message="state.crawlStatus.message"
      :progress="state.crawlStatus.progress"
      footer-text="当前状态来自后端真实轮询结果。"
    />

    <section class="page-card">
      <div class="section-title">
        <div>
          <h2>商品列表</h2>
          <p>接口返回的商品列表会在这里分页展示，每页 12 个。</p>
        </div>

        <span class="badge list-badge">共 {{ state.products.length }} 条</span>
      </div>

      <div v-if="visibleProducts.length" class="grid">
        <button
          v-for="item in visibleProducts"
          :key="item.productId"
          class="product-button"
          type="button"
          @click="goDetail(item.productId)"
        >
          <ProductCard :data="item" />
        </button>
      </div>

      <div v-else class="empty-card">
        <strong>暂无商品结果</strong>
        <p>后端任务完成后，商品卡片会自动刷新到这里。</p>
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button class="button-secondary" type="button" :disabled="currentPage === 1" @click="currentPage -= 1">
          上一页
        </button>
        <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
        <button class="button-secondary" type="button" :disabled="currentPage === totalPages" @click="currentPage += 1">
          下一页
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import ProductCard from '../components/ProductCard.vue'
import StatusPanel from '../components/StatusPanel.vue'
import { useAppStore } from '../store'

const router = useRouter()
const { state, startRealCrawl } = useAppStore()

const keyword = ref('笔记本电脑')
const page = ref(2)
const currentPage = ref(1)

const isRunning = computed(() => state.crawlStatus.phase === 'running')
const totalPages = computed(() => Math.max(1, Math.ceil(state.products.length / 12)))
const visibleProducts = computed(() => {
  const startIndex = (currentPage.value - 1) * 12
  return state.products.slice(startIndex, startIndex + 12)
})

watch(
  () => state.products.length,
  () => {
    currentPage.value = 1
  }
)

const start = async () => {
  await startRealCrawl({ keyword: keyword.value, pages: page.value })
}

const goDetail = (id) => {
  router.push(`/detail/${id}`)
}
</script>

<style scoped>
.toolbar {
  display: grid;
  grid-template-columns: 1.2fr 180px 180px;
  gap: 16px;
  align-items: end;
}

.field {
  min-width: 0;
}

.field-small {
  max-width: 180px;
}

.action-button {
  width: 100%;
}

.list-badge {
  color: #0f6b52;
  background: rgba(31, 169, 122, 0.12);
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.product-button {
  padding: 0;
  border: 0;
  background: transparent;
  text-align: left;
}

.empty-card {
  display: grid;
  place-items: center;
  min-height: 220px;
  text-align: center;
  border-radius: 24px;
  background: rgba(31, 169, 122, 0.05);
  border: 1px dashed rgba(31, 169, 122, 0.18);
}

.empty-card strong {
  margin-bottom: 8px;
}

.empty-card p {
  margin: 0;
  color: var(--text-soft);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 22px;
}

@media (max-width: 1080px) {
  .toolbar {
    grid-template-columns: 1fr 160px;
  }

  .action-button {
    grid-column: 1 / -1;
  }

  .grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .toolbar {
    grid-template-columns: 1fr;
  }

  .field-small {
    max-width: none;
  }

  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 520px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .pagination {
    flex-direction: column;
  }
}
</style>
