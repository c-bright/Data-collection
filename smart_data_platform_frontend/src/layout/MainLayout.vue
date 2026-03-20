<template>
  <div class="layout-shell">
    <Sidebar />

    <div class="layout-main">
      <TopBar />

      <main class="layout-content">
        <router-view v-slot="{ Component, route }">
          <Transition name="page-fade" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </Transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
</script>

<style scoped>
.layout-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 268px 1fr;
  background:
    radial-gradient(circle at top left, rgba(77, 201, 168, 0.12), transparent 28%),
    radial-gradient(circle at bottom right, rgba(129, 227, 207, 0.14), transparent 26%),
    var(--app-bg);
}

.layout-main {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.layout-content {
  flex: 1;
  min-height: 0;
  padding: 24px 28px 28px;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.28s ease, transform 0.28s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@media (max-width: 1080px) {
  .layout-shell {
    grid-template-columns: 92px 1fr;
  }

  .layout-content {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .layout-shell {
    grid-template-columns: 1fr;
  }
}
</style>
