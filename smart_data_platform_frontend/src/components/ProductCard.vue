<template>
  <article class="product-card">
    <div class="image-wrap">
      <img :src="data.image" :alt="data.name" />
    </div>

    <div class="body">
      <h3>{{ data.name }}</h3>
      <p class="price">¥ {{ Number(data.price).toLocaleString('zh-CN') }}</p>
    </div>
  </article>
</template>

<script setup>
defineProps({
  data: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.product-card {
  overflow: hidden;
  border-radius: 22px;
  background: var(--card-bg);
  border: 1px solid rgba(31, 41, 55, 0.06);
  box-shadow: var(--shadow-soft);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.image-wrap {
  aspect-ratio: 1 / 1;
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.12), rgba(144, 247, 236, 0.2));
}

.image-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.body {
  padding: 16px 16px 18px;
}

h3 {
  margin: 0;
  font-size: 1rem;
  line-height: 1.45;
  color: var(--text-strong);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.9em;
}

.price {
  margin: 12px 0 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--accent-strong);
}
</style>
