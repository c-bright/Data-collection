<template>
  <div class="param-table">
    <div v-for="(value, key) in params" :key="key" class="param-row">
      <span class="key">{{ key }}</span>
      <span class="value">{{ value }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  params: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style scoped>
.param-table {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.param-row {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 14px;
  align-items: start;
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(31, 169, 122, 0.05);
  border: 1px solid rgba(31, 169, 122, 0.08);
}

.key {
  color: var(--text-soft);
  font-weight: 600;
}

.value {
  color: var(--text-strong);
  line-height: 1.6;
}

@media (max-width: 640px) {
  .param-row {
    grid-template-columns: 1fr;
  }
}
</style>
