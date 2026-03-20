<template>
  <div class="page-shell">
    <section class="page-card head-card">
      <div>
        <h2>商品分析总览</h2>
        <p>
          进入商品详情页后会触发分析任务，当前页面会自动从示例数据切换到真实商品分析数据。
        </p>
      </div>

      <div class="head-meta">
        <SourceBadge :source="state.dataSource" />
        <span class="time-tag">{{ state.lastUpdated || '尚未生成真实分析结果' }}</span>
      </div>
    </section>

    <div class="chart-grid">
      <ChartCard
        title="价格与评论数散点图"
        eyebrow="Scatter Plot"
        description="X 轴为价格，Y 轴为评论数，不同店铺使用不同颜色区分。"
        :source="state.dataSource"
        :loading="isLoading"
        loading-text="正在切换商品分析数据..."
        :height="380"
        :option="scatterOption"
      />

      <ChartCard
        title="价格分布柱状图"
        eyebrow="Price Distribution"
        description="展示不同价格区间内的商品数量分布。"
        :source="state.dataSource"
        :loading="isLoading"
        loading-text="正在刷新价格区间统计..."
        :option="priceOption"
      />

      <ChartCard
        title="店铺分布图"
        eyebrow="Shop Distribution"
        description="观察商品样本主要集中在哪些店铺。"
        :source="state.dataSource"
        :loading="isLoading"
        loading-text="正在统计店铺分布..."
        :option="shopOption"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ChartCard from '../components/ChartCard.vue'
import SourceBadge from '../components/SourceBadge.vue'
import { useAppStore } from '../store'

const { state } = useAppStore()

const isLoading = computed(() => state.dataSource === 'loading')

const chartColors = ['#1fa97a', '#39c4a5', '#67d7bf', '#84aef5', '#f7b955']

const scatterOption = computed(() => ({
  color: chartColors,
  grid: {
    left: 50,
    right: 24,
    top: 30,
    bottom: 40
  },
  tooltip: {
    trigger: 'item',
    formatter: (params) => {
      const [price, comments] = params.value
      return `${params.seriesName}<br/>价格：¥ ${price}<br/>评论数：${comments}`
    }
  },
  xAxis: {
    type: 'value',
    name: '价格',
    axisLine: { lineStyle: { color: '#9fb3ab' } },
    splitLine: { lineStyle: { color: 'rgba(31, 41, 55, 0.06)' } }
  },
  yAxis: {
    type: 'value',
    name: '评论数',
    axisLine: { lineStyle: { color: '#9fb3ab' } },
    splitLine: { lineStyle: { color: 'rgba(31, 41, 55, 0.06)' } }
  },
  series: state.productAnalysisData.scatter.map((item, index) => ({
    name: item.name,
    type: 'scatter',
    symbolSize: 20 + index * 2,
    itemStyle: { color: chartColors[index % chartColors.length] },
    data: [item.value]
  }))
}))

const priceOption = computed(() => ({
  color: ['#35c5a4'],
  tooltip: {
    trigger: 'axis'
  },
  grid: {
    left: 40,
    right: 20,
    top: 20,
    bottom: 40
  },
  xAxis: {
    type: 'category',
    data: state.productAnalysisData.priceDistribution.map((item) => item.range),
    axisTick: { show: false },
    axisLine: { lineStyle: { color: '#9fb3ab' } }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: 'rgba(31, 41, 55, 0.06)' } }
  },
  series: [
    {
      type: 'bar',
      barWidth: 34,
      borderRadius: [12, 12, 0, 0],
      data: state.productAnalysisData.priceDistribution.map((item) => item.count)
    }
  ]
}))

const shopOption = computed(() => ({
  color: ['#1fa97a', '#39c4a5', '#67d7bf', '#84aef5', '#f7b955'],
  tooltip: {
    trigger: 'item'
  },
  legend: {
    bottom: 0,
    icon: 'circle'
  },
  series: [
    {
      type: 'pie',
      radius: ['42%', '70%'],
      center: ['50%', '46%'],
      itemStyle: {
        borderRadius: 12,
        borderColor: '#fff',
        borderWidth: 3
      },
      label: {
        formatter: '{b}\n{d}%'
      },
      data: state.productAnalysisData.shopDistribution.map((item) => ({
        name: item.shop,
        value: item.count
      }))
    }
  ]
}))
</script>

<style scoped>
.head-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.head-card h2 {
  margin: 0 0 10px;
}

.head-card p {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.7;
}

.head-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.time-tag {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(31, 169, 122, 0.08);
  color: var(--text-soft);
  font-size: 0.84rem;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.chart-grid > :first-child {
  grid-column: 1 / -1;
}

@media (max-width: 960px) {
  .head-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .chart-grid {
    grid-template-columns: 1fr;
  }

  .chart-grid > :first-child {
    grid-column: auto;
  }
}
</style>
