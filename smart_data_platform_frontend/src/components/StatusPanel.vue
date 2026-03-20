<template>
  <section class="status-panel">
    <div class="status-header">
      <div>
        <p class="status-eyebrow">{{ eyebrow }}</p>
        <h3>{{ title }}</h3>
      </div>
      <span class="badge" :class="statusClass">{{ statusLabel }}</span>
    </div>

    <p class="status-message">{{ message }}</p>

    <div class="progress-track">
      <div class="progress-fill" :style="{ width: `${safeProgress}%` }"></div>
    </div>

    <div class="status-footer">
      <span>轮询进度 {{ safeProgress }}%</span>
      <span>{{ footerText }}</span>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: '任务状态'
  },
  eyebrow: {
    type: String,
    default: '轮询状态'
  },
  status: {
    type: String,
    default: 'idle'
  },
  message: {
    type: String,
    default: ''
  },
  progress: {
    type: Number,
    default: 0
  },
  footerText: {
    type: String,
    default: '轮询机制保持页面状态更新'
  }
})

const safeProgress = computed(() => Math.max(0, Math.min(100, Number(props.progress) || 0)))

const statusLabel = computed(() => {
  if (props.status === 'running') {
    return '运行中'
  }
  if (props.status === 'success') {
    return '已完成'
  }
  if (props.status === 'error') {
    return '失败'
  }
  return '待开始'
})

const statusClass = computed(() => ({
  idle: props.status === 'idle',
  running: props.status === 'running',
  success: props.status === 'success',
  error: props.status === 'error'
}))
</script>

<style scoped>
.status-panel {
  padding: 22px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.08), rgba(144, 247, 236, 0.18));
  border: 1px solid rgba(31, 169, 122, 0.12);
}

.status-header,
.status-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.status-eyebrow {
  margin: 0 0 6px;
  font-size: 0.76rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-strong);
}

h3 {
  margin: 0;
}

.status-message {
  margin: 14px 0;
  color: var(--text-soft);
  line-height: 1.65;
}

.progress-track {
  height: 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.78);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #1fa97a, #7de4cf);
  transition: width 0.36s ease;
}

.status-footer {
  margin-top: 10px;
  color: var(--text-soft);
  font-size: 0.9rem;
}

.idle {
  background: rgba(148, 163, 184, 0.14);
  color: #516171;
}

.running {
  background: rgba(255, 214, 102, 0.26);
  color: #9a6700;
}

.success {
  background: rgba(31, 169, 122, 0.12);
  color: #0f6b52;
}

.error {
  background: rgba(255, 120, 117, 0.18);
  color: #b42318;
}

@media (max-width: 640px) {
  .status-header,
  .status-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
