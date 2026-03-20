import { readonly, reactive } from 'vue'
import request from '../utils/request'

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const sampleProductAnalysis = {
  scatter: [
    { name: '青林数码旗舰店', value: [399, 8324] },
    { name: '新芽办公专营店', value: [1999, 2960] },
    { name: '沐野厨房', value: [699, 9031] },
    { name: '木朴生活馆', value: [1499, 2468] },
    { name: '轻氧运动旗舰店', value: [999, 7820] }
  ],
  priceDistribution: [
    { range: '0-300', count: 4 },
    { range: '300-700', count: 9 },
    { range: '700-1200', count: 7 },
    { range: '1200-2000', count: 6 },
    { range: '2000+', count: 3 }
  ],
  shopDistribution: [
    { shop: '青林数码旗舰店', count: 5 },
    { shop: '新芽办公专营店', count: 4 },
    { shop: '木朴生活馆', count: 3 },
    { shop: '沐野厨房', count: 4 },
    { shop: '其他店铺', count: 5 }
  ]
}

const sampleCommentAnalysis = {
  wordCloud: [
    { name: '包装一般', value: 88 },
    { name: '发热明显', value: 74 },
    { name: '物流偏慢', value: 96 },
    { name: '做工细节', value: 67 },
    { name: '续航普通', value: 79 },
    { name: '说明书简略', value: 58 },
    { name: '色差轻微', value: 49 },
    { name: '配件不足', value: 62 },
    { name: '噪音偏大', value: 83 },
    { name: '客服响应慢', value: 71 },
    { name: '按键手感', value: 45 },
    { name: '边角磨损', value: 39 }
  ],
  tags: [
    { label: '物流速度', count: 126 },
    { label: '价格接受度', count: 108 },
    { label: '材质做工', count: 92 },
    { label: '售后体验', count: 83 },
    { label: '使用噪音', count: 77 },
    { label: '功能稳定性', count: 65 }
  ]
}

const state = reactive({
  products: [],
  crawlKeyword: '',
  crawlStatus: {
    phase: 'idle',
    message: '输入关键词后即可启动真实爬虫任务。',
    progress: 0
  },
  currentProduct: null,
  detailStatus: {
    phase: 'idle',
    message: '尚未加载商品详情。'
  },
  analysisStatus: {
    phase: 'idle',
    message: '尚未选择具体商品，当前分析页展示示例数据。'
  },
  dataSource: 'sample',
  currentAnalysisProductId: null,
  lastUpdated: null,
  productAnalysisData: sampleProductAnalysis,
  commentAnalysisData: sampleCommentAnalysis
})

const parseNumericPrice = (value) => {
  if (typeof value === 'number') {
    return value
  }
  const matched = String(value || '').match(/\d+(\.\d+)?/)
  return matched ? Number(matched[0]) : 0
}

const parseNumericCount = (value) => {
  if (typeof value === 'number') {
    return value
  }
  const raw = String(value || '').trim()
  if (!raw) {
    return 0
  }
  const matched = raw.match(/\d+(\.\d+)?/)
  if (!matched) {
    return 0
  }
  let number = Number(matched[0])
  if (raw.includes('万')) {
    number *= 10000
  }
  return Math.round(number)
}

const mapBackendProduct = (item) => ({
  id: item.product_id,
  productId: item.product_id,
  image: item.image || '',
  name: item.name || '未命名商品',
  price: parseNumericPrice(item.price),
  priceDisplay: item.price_display || `¥ ${parseNumericPrice(item.price).toLocaleString('zh-CN')}`,
  shop: item.shop || '未知店铺',
  commentCount: parseNumericCount(item.comment_count),
  commentCountDisplay: item.comment_count?.toString?.() || '0',
  link: item.link || '',
  category: item.category || '',
  params: item.params || {}
})

const backendDetailLabelMap = {
  product_id: '商品ID',
  name: '商品名称',
  image: '商品图片',
  price_display: '价格展示',
  link: '商品链接',
  shop: '店铺',
  category: '分类',
  comment_count: '评论数'
}

const buildDetailParams = (detailData) => {
  const source = detailData?.detailed_params && Object.keys(detailData.detailed_params).length
    ? detailData.detailed_params
    : detailData

  return Object.entries(source || {}).reduce((result, [key, value]) => {
    if (value === undefined || value === null || value === '') {
      return result
    }

    const label = backendDetailLabelMap[key] || key
    result[label] = value
    return result
  }, {})
}

const sortPriceDistribution = (input) => {
  return Object.entries(input || {}).map(([range, count]) => ({
    range,
    count: Number(count) || 0
  }))
}

const sortShopDistribution = (input) => {
  return Object.entries(input || {})
    .map(([shop, count]) => ({
      shop,
      count: Number(count) || 0
    }))
    .sort((a, b) => b.count - a.count)
}

const normalizeAnalysisResult = (result) => {
  const product = result?.product || {}
  const comments = result?.comments || {}
  const tags = result?.tags || {}

  return {
    product: {
      scatter: (product.scatter_points || []).map((item) => ({
        name: item.shop || '未知店铺',
        value: [Number(item.price) || 0, Number(item.comment) || 0]
      })),
      priceDistribution: sortPriceDistribution(product.price_distribution),
      shopDistribution: sortShopDistribution(product.shop_distribution)
    },
    comment: {
      wordCloud: (comments.negative_wordcloud || []).map((item) => ({
        name: item.name,
        value: Number(item.value) || 0
      })),
      tags: (tags.tags || []).map((item) => ({
        label: item.name,
        count: Number(item.value) || 0
      }))
    }
  }
}

const setSampleAnalysis = () => {
  state.dataSource = 'sample'
  state.currentAnalysisProductId = null
  state.lastUpdated = null
  state.productAnalysisData = sampleProductAnalysis
  state.commentAnalysisData = sampleCommentAnalysis
  state.analysisStatus = {
    phase: 'idle',
    message: '当前为示例数据，可进入商品详情页触发真实分析。'
  }
}

const pollCrawlStatus = async (keyword) => {
  const progressMarks = [26, 42, 58, 72, 84, 92]
  let index = 0

  while (true) {
    await wait(2200)

    try {
      const response = await request.get('/crawl/status', {
        params: { keyword }
      })
      const payload = response.data || {}
      const status = payload.status

      if (status === 'completed') {
        state.products = (payload.data || []).map(mapBackendProduct)
        state.crawlStatus = {
          phase: 'success',
          message: payload.message || `已获取 ${state.products.length} 条商品数据。`,
          progress: 100
        }
        return
      }

      if (status === 'crawling') {
        state.crawlStatus = {
          phase: 'running',
          message: payload.message || '后端仍在执行爬虫任务，请稍候。',
          progress: progressMarks[Math.min(index, progressMarks.length - 1)]
        }
        index += 1
        continue
      }

      state.crawlStatus = {
        phase: 'error',
        message: payload.message || '爬虫状态未知，请稍后重试。',
        progress: 0
      }
      return
    } catch (error) {
      const message = error.response?.data?.message || '轮询爬虫状态失败，请确认后端服务是否可用。'
      if (error.response?.status === 404) {
        state.crawlStatus = {
          phase: 'error',
          message,
          progress: 0
        }
        return
      }

      state.crawlStatus = {
        phase: 'error',
        message,
        progress: 0
      }
      return
    }
  }
}

const startRealCrawl = async ({ keyword, pages }) => {
  const normalizedKeyword = String(keyword || '').trim()
  if (!normalizedKeyword) {
    state.crawlStatus = {
      phase: 'error',
      message: '关键词不能为空。',
      progress: 0
    }
    return
  }

  state.crawlKeyword = normalizedKeyword
  state.crawlStatus = {
    phase: 'running',
    message: '正在向后端提交爬虫任务...',
    progress: 8
  }

  try {
    const response = await request.post('/crawl/start', {
      keyword: normalizedKeyword,
      max_page: Number(pages) || 1
    })

    const payload = response.data || {}

    if (!payload.success) {
      throw new Error(payload.message || '爬虫任务启动失败。')
    }

    if (payload.status === 'completed') {
      state.products = (payload.data || []).map(mapBackendProduct)
      state.crawlStatus = {
        phase: 'success',
        message: payload.message || `已获取 ${state.products.length} 条商品数据。`,
        progress: 100
      }
      return
    }

    state.crawlStatus = {
      phase: 'running',
      message: payload.message || '爬虫已启动，正在等待后端处理。',
      progress: 16
    }

    await pollCrawlStatus(normalizedKeyword)
  } catch (error) {
    state.crawlStatus = {
      phase: 'error',
      message: error.response?.data?.message || error.message || '爬虫任务调用失败。',
      progress: 0
    }
  }
}

const getProductById = (id) => {
  return state.products.find((item) => item.productId === id || item.id === id) || null
}

const loadProductBundle = async (productId) => {
  state.currentProduct = null
  state.detailStatus = {
    phase: 'running',
    message: '正在获取商品详情、详细参数与评论分析...'
  }
  state.dataSource = 'loading'
  state.analysisStatus = {
    phase: 'running',
    message: `正在按顺序抓取商品 ${productId} 的详细参数与评论分析，请耐心等待。`
  }

  try {
    const response = await request.get(`/analysis/full/${productId}`)
    const payload = response.data || {}

    if (!payload.success || !payload.data?.detail) {
      throw new Error(payload.message || '商品详情与分析数据不存在。')
    }

    const detailData = payload.data.detail
    const backendItem = mapBackendProduct(detailData)
    backendItem.params = buildDetailParams(detailData)

    const normalized = normalizeAnalysisResult(payload.data.analysis?.result)

    state.currentProduct = backendItem
    state.detailStatus = {
      phase: 'success',
      message: payload.message || '商品详情与详细参数加载成功。'
    }
    state.productAnalysisData = normalized.product
    state.commentAnalysisData = normalized.comment
    state.dataSource = 'real'
    state.currentAnalysisProductId = productId
    state.lastUpdated = new Date().toLocaleString('zh-CN')
    state.analysisStatus = {
      phase: 'success',
      message: '已完成详细参数抓取，并继续完成恶评与标签分析。'
    }

    return backendItem
  } catch (error) {
    state.detailStatus = {
      phase: 'error',
      message: error.response?.data?.message || error.message || '商品详情与分析加载失败。'
    }
    state.dataSource = 'sample'
    state.currentAnalysisProductId = null
    state.lastUpdated = null
    state.productAnalysisData = sampleProductAnalysis
    state.commentAnalysisData = sampleCommentAnalysis
    state.analysisStatus = {
      phase: 'error',
      message: error.response?.data?.message || error.message || '统一详情分析接口调用失败，已回退到示例数据。'
    }
    return null
  }
}

export function useAppStore() {
  return {
    state: readonly(state),
    startRealCrawl,
    getProductById,
    loadProductBundle,
    setSampleAnalysis
  }
}
