<template>
  <header class="topbar">
    <div class="topbar-accent"></div>

    <div>
      <p class="eyebrow">电商数据分析平台</p>
      <h1>{{ route.meta.title || '智能分析平台' }}</h1>
      <p class="subtitle">{{ route.meta.subtitle || '明亮、自然、具有轻科技感的数据工作台' }}</p>
    </div>

    <div class="topbar-side">
      <div class="highlight-card">
        <span class="highlight-label">当前分析上下文</span>
        <strong>{{ currentProductName }}</strong>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '../store'

const route = useRoute()
const { state } = useAppStore()

const currentProductName = computed(() => {
  return state.currentProduct?.name || '当前为示例数据上下文'
})
</script>

<style scoped>
.topbar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 24px 28px 22px;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(31, 41, 55, 0.06);
}

.topbar-accent {
  position: absolute;
  inset: 0 0 auto 0;
  height: 7px;
  border-radius: 0 0 999px 999px;
  background: linear-gradient(90deg, #1fa97a, #35c5a4, #90f7ec);
}

.eyebrow {
  margin: 0 0 6px;
  font-size: 0.78rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent-strong);
}

h1 {
  margin: 0;
  font-size: 1.7rem;
  color: var(--text-strong);
}

.subtitle {
  margin: 6px 0 0;
  color: var(--text-soft);
}

.topbar-side {
  display: flex;
  align-items: center;
  gap: 12px;
}

.highlight-card {
  min-width: 220px;
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.12), rgba(144, 247, 236, 0.2));
  border: 1px solid rgba(31, 169, 122, 0.14);
}

.highlight-label {
  display: block;
  margin-bottom: 4px;
  font-size: 0.76rem;
  color: var(--text-soft);
}

.highlight-card strong {
  color: var(--text-strong);
  display: block;
  line-height: 1.5;
}

@media (max-width: 900px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .topbar-side {
    width: 100%;
  }

  .highlight-card {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .topbar {
    padding: 20px 20px 18px;
  }

  h1 {
    font-size: 1.4rem;
  }
}
</style>
