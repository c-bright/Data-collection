import { createRouter, createWebHistory } from 'vue-router'

import MainLayout from '../layout/MainLayout.vue'
import Home from '../views/Home.vue'
import Crawl from '../views/Crawl.vue'
import Detail from '../views/Detail.vue'
import AnalysisProduct from '../views/AnalysisProduct.vue'
import AnalysisComment from '../views/AnalysisComment.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      public: true,
      title: '登录注册',
      subtitle: '连接后端真实登录与注册接口'
    }
  },
  {
    path: '/',
    component: MainLayout,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'home',
        component: Home,
        meta: {
          title: '平台首页',
          subtitle: '快速了解系统能力与整体工作流'
        }
      },
      {
        path: 'crawl',
        name: 'crawl',
        component: Crawl,
        meta: {
          title: '商品爬取',
          subtitle: '输入关键词并触发真实商品抓取流程'
        }
      },
      {
        path: 'detail/:id',
        name: 'detail',
        component: Detail,
        meta: {
          title: '商品详情',
          subtitle: '查看商品基础信息并触发分析任务'
        }
      },
      {
        path: 'analysis/product',
        name: 'analysis-product',
        component: AnalysisProduct,
        meta: {
          title: '商品分析',
          subtitle: '对价格、评论量与店铺分布进行可视化分析'
        }
      },
      {
        path: 'analysis/comment',
        name: 'analysis-comment',
        component: AnalysisComment,
        meta: {
          title: '评论分析',
          subtitle: '观察差评热词与用户标签分布'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const isAuthenticated = localStorage.getItem('token') === 'true'

  if (to.meta.requiresAuth && !isAuthenticated) {
    return {
      name: 'login',
      query: {
        redirect: to.fullPath
      }
    }
  }

  if (to.name === 'login' && isAuthenticated) {
    return { name: 'home' }
  }

  return true
})

export default router
