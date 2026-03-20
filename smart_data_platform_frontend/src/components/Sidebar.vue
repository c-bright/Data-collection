<template>
  <aside class="sidebar">
    <div class="sidebar-accent"></div>

    <div class="brand-card">
      <div class="brand-mark">SDP</div>
      <div>
        <div class="brand-title">Smart Data</div>
        <p class="brand-copy">电商分析平台</p>
      </div>
    </div>

    <nav class="nav-list">
      <router-link
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="nav-item"
        active-class="nav-item-active"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-text">
          <strong>{{ item.label }}</strong>
          <small>{{ item.description }}</small>
        </span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <button class="logout-button" type="button" @click="logout">退出登录</button>
      <span class="footer-chip">Bright</span>
      <span class="footer-chip">Natural</span>
      <span class="footer-chip">Insight</span>
    </div>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navItems = [
  { to: '/', label: '首页', description: '平台功能介绍', icon: 'H' },
  { to: '/crawl', label: '商品爬取', description: '关键词任务抓取', icon: 'C' },
  { to: '/analysis/product', label: '商品分析', description: '价格与店铺分布', icon: 'P' },
  { to: '/analysis/comment', label: '评论分析', description: '差评词云与标签', icon: 'R' }
]

const logout = async () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  await router.push('/login')
}
</script>

<style scoped>
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  padding: 22px 18px;
  border-right: 1px solid rgba(31, 41, 55, 0.08);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(14px);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-accent {
  position: absolute;
  inset: 0 auto 0 0;
  width: 6px;
  border-radius: 0 999px 999px 0;
  background: linear-gradient(180deg, #1fa97a, #7de4cf);
}

.brand-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(30, 190, 146, 0.16), rgba(132, 233, 212, 0.18));
  border: 1px solid rgba(31, 169, 122, 0.14);
}

.brand-mark {
  width: 54px;
  height: 54px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  font-weight: 800;
  color: #0d5f48;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.brand-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-strong);
}

.brand-copy {
  margin: 4px 0 0;
  color: var(--text-soft);
  font-size: 0.9rem;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 15px;
  border-radius: 18px;
  color: var(--text-soft);
  transition: transform 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease;
}

.nav-item:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.78);
  box-shadow: var(--shadow-soft);
}

.nav-item-active {
  background: linear-gradient(135deg, rgba(31, 169, 122, 0.14), rgba(125, 228, 207, 0.18));
  color: var(--text-strong);
  box-shadow: var(--shadow-soft);
}

.nav-icon {
  width: 38px;
  height: 38px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  font-weight: 700;
  color: #0f6b52;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(31, 169, 122, 0.12);
}

.nav-text {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.nav-text strong {
  font-size: 0.96rem;
}

.nav-text small {
  color: var(--text-muted);
}

.sidebar-footer {
  margin-top: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.logout-button {
  width: 100%;
  padding: 10px 12px;
  border: 0;
  border-radius: 14px;
  background: rgba(255, 120, 117, 0.14);
  color: #b42318;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.logout-button:hover {
  transform: translateY(-2px);
  background: rgba(255, 120, 117, 0.2);
}

.footer-chip {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  color: #0f6b52;
  background: rgba(31, 169, 122, 0.1);
}

@media (max-width: 1080px) {
  .sidebar {
    padding: 20px 12px;
  }

  .brand-card {
    justify-content: center;
    padding: 12px;
  }

  .brand-card > :last-child,
  .nav-text,
  .sidebar-footer {
    display: none;
  }

  .nav-item {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: relative;
    height: auto;
    padding-bottom: 10px;
    border-right: 0;
    border-bottom: 1px solid rgba(31, 41, 55, 0.08);
  }

  .sidebar-accent {
    width: 100%;
    height: 5px;
    inset: auto 0 0 0;
    border-radius: 999px 999px 0 0;
    background: linear-gradient(90deg, #1fa97a, #7de4cf);
  }

  .nav-list {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .nav-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
