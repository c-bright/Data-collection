<template>
  <section class="chart-card">
    <header class="card-header">
      <div>
        <p v-if="eyebrow" class="eyebrow">{{ eyebrow }}</p>
        <h3>{{ title }}</h3>
        <p v-if="description" class="description">{{ description }}</p>
      </div>

      <SourceBadge :source="source" />
    </header>

    <div class="chart-shell" :style="{ minHeight: `${height}px` }">
      <Transition name="fade">
        <div v-if="loading" class="loading-mask">
          <div class="loader"></div>
          <p>{{ loadingText || '图表数据加载中...' }}</p>
        </div>
      </Transition>

      <div v-show="!loading && hasOption" ref="chartRef" class="chart"></div>

      <div v-if="!loading && !hasOption" class="empty-state">
        <strong>暂无图表数据</strong>
        <span>当前卡片等待示例数据或真实分析结果注入。</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import SourceBadge from './SourceBadge.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  eyebrow: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  source: {
    type: String,
    default: 'sample'
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: ''
  },
  height: {
    type: Number,
    default: 320
  },
  option: {
    type: Object,
    default: null
  }
})

const chartRef = ref(null)
let chartInstance = null
let resizeObserver = null

const hasOption = computed(() => !!props.option)

const renderChart = async () => {
  if (!chartRef.value || !props.option || props.loading) {
    return
  }

  await nextTick()

  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  chartInstance.setOption(
    {
      animationDuration: 700,
      animationEasing: 'cubicOut',
      ...props.option
    },
    true
  )
  chartInstance.resize()
}

const disposeChart = () => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
}

const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  renderChart()

  if (window.ResizeObserver) {
    resizeObserver = new ResizeObserver(handleResize)
    if (chartRef.value) {
      resizeObserver.observe(chartRef.value)
    }
  }

  window.addEventListener('resize', handleResize)
})

watch(
  () => [props.option, props.loading],
  () => {
    if (props.loading) {
      return
    }
    renderChart()
  },
  { deep: true }
)

watch(
  () => props.height,
  () => {
    renderChart()
  }
)

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  window.removeEventListener('resize', handleResize)
  disposeChart()
})
</script>

<style scoped>
.chart-card {
  padding: 22px;
  border-radius: 26px;
  background: var(--card-bg);
  border: 1px solid rgba(31, 41, 55, 0.06);
  box-shadow: var(--shadow-soft);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 6px;
  font-size: 0.76rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent-strong);
}

h3 {
  margin: 0;
  font-size: 1.16rem;
  color: var(--text-strong);
}

.description {
  margin: 8px 0 0;
  color: var(--text-soft);
  line-height: 1.6;
}

.chart-shell {
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
  min-height: inherit;
}

.loading-mask,
.empty-state {
  min-height: inherit;
  border-radius: 20px;
  display: grid;
  place-items: center;
  text-align: center;
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.06), rgba(144, 247, 236, 0.14));
  border: 1px dashed rgba(31, 169, 122, 0.18);
  color: var(--text-soft);
  padding: 24px;
}

.loading-mask {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.loader {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 3px solid rgba(31, 169, 122, 0.22);
  border-top-color: var(--accent-strong);
  animation: spin 0.8s linear infinite;
}

.empty-state strong {
  display: block;
  color: var(--text-strong);
  margin-bottom: 8px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
