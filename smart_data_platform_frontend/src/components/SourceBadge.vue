<template>
  <span class="badge" :class="badgeClass">{{ label }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  source: {
    type: String,
    default: 'sample'
  }
})

const label = computed(() => {
  if (props.source === 'real') {
    return '当前商品数据'
  }
  if (props.source === 'loading') {
    return '分析加载中'
  }
  return '示例数据'
})

const badgeClass = computed(() => {
  return {
    sample: props.source === 'sample',
    loading: props.source === 'loading',
    real: props.source === 'real'
  }
})
</script>

<style scoped>
.sample {
  color: #0f6b52;
  background: rgba(31, 169, 122, 0.12);
}

.loading {
  color: #9a6700;
  background: rgba(255, 214, 102, 0.26);
}

.real {
  color: #1357a6;
  background: rgba(84, 160, 255, 0.16);
}
</style>
