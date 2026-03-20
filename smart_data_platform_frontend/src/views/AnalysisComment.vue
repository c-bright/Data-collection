<template>
  <div class="page-shell">
    <section class="page-card head-card">
      <div>
        <h2>评论分析总览</h2>
        <p>词云作为视觉中心展示差评高频词，下方标签图用于观察评论关注点的数量分布。</p>
      </div>

      <div class="head-meta">
        <SourceBadge :source="state.dataSource" />
        <span class="time-tag">{{ state.lastUpdated || '当前使用示例评论数据' }}</span>
      </div>
    </section>

    <ChartCard
      title="差评词云"
      eyebrow="Negative Word Cloud"
      description="以更强的视觉重心展示评论中的高频负向表达。"
      :source="state.dataSource"
      :loading="isLoading"
      loading-text="正在更新评论词云..."
      :height="430"
      :option="wordCloudOption"
    />

    <ChartCard
      title="标签柱状图"
      eyebrow="Comment Tags"
      description="对评论中的主要标签进行数量统计，帮助定位用户最关注的话题。"
      :source="state.dataSource"
      :loading="isLoading"
      loading-text="正在整理评论标签..."
      :option="tagOption"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import 'echarts-wordcloud'
import ChartCard from '../components/ChartCard.vue'
import SourceBadge from '../components/SourceBadge.vue'
import { useAppStore } from '../store'

const { state } = useAppStore()

const isLoading = computed(() => state.dataSource === 'loading')

const wordCloudOption = computed(() => ({
  tooltip: {
    show: true
  },
  series: [
    {
      type: 'wordCloud',
      shape: 'circle',
      width: '100%',
      height: '100%',
      gridSize: 8,
      sizeRange: [18, 58],
      rotationRange: [-30, 30],
      textStyle: {
        color: () => {
          const colors = ['#1fa97a', '#39c4a5', '#67d7bf', '#84aef5', '#f7b955']
          return colors[Math.floor(Math.random() * colors.length)]
        }
      },
      emphasis: {
        textStyle: {
          shadowBlur: 18,
          shadowColor: 'rgba(31, 41, 55, 0.18)'
        }
      },
      data: state.commentAnalysisData.wordCloud
    }
  ]
}))

const tagOption = computed(() => ({
  color: ['#1fa97a'],
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
    data: state.commentAnalysisData.tags.map((item) => item.label),
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
      barWidth: 38,
      borderRadius: [12, 12, 0, 0],
      data: state.commentAnalysisData.tags.map((item) => item.count)
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

@media (max-width: 960px) {
  .head-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
