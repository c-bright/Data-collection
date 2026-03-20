<template>
  <div class="auth-wrapper">
    <canvas ref="particleCanvas" class="particle-canvas"></canvas>
    <div class="data-background">
      <div class="grid-layer"></div>
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
    </div>

    <div class="auth-card">
      <div class="auth-toggle">
        <div class="toggle-slider" :class="{ 'is-register': !isLogin }"></div>
        <button type="button" :class="['toggle-btn', { active: isLogin }]" @click="switchMode(true)">账号登录</button>
        <button type="button" :class="['toggle-btn', { active: !isLogin }]" @click="switchMode(false)">注册账户</button>
      </div>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="input-label">用户名</label>
          <div class="input-box">
            <input v-model="form.username" type="text" placeholder="输入用户名或 ID" required />
          </div>
        </div>

        <transition name="fade-slide">
          <div v-if="!isLogin" class="form-group">
            <label class="input-label">邮箱</label>
            <div class="input-box">
              <input v-model="form.email" type="email" placeholder="example@domain.com" :required="!isLogin" />
            </div>
          </div>
        </transition>

        <div class="form-group">
          <label class="input-label">密码</label>
          <div class="input-box password-wrapper">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="••••••••" required />
            <span class="eye-icon" @click="showPassword = !showPassword">
              <svg v-if="showPassword" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            </span>
          </div>
        </div>

        <transition name="fade-slide">
          <div v-if="isLogin" class="form-group">
            <div ref="sliderContainer" class="slider-captcha" :class="{ verified: sliderVerified }">
              <div class="slider-track">
                <div class="slider-fill" :style="{ width: sliderPosition + 40 + 'px' }"></div>
                <div class="slider-text">{{ sliderVerified ? '身份验证通过' : '向右滑动进行验证' }}</div>
              </div>
              <div class="slider-thumb" :style="{ transform: `translateX(${sliderPosition}px)` }" @mousedown.prevent="startDrag" @touchstart.prevent="startDrag">
                {{ sliderVerified ? '✔' : '❯' }}
              </div>
            </div>
          </div>
        </transition>

        <button class="submit-btn" type="submit" :disabled="isLogin && !sliderVerified || loading">
          <span v-if="!loading">{{ isLogin ? '确 认 登 录' : '立 即 注 册' }}</span>
          <div v-else class="loader"></div>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import request from '../utils/request'

const router = useRouter()
const isLogin = ref(true)
const showPassword = ref(false)
const loading = ref(false)
const form = reactive({ username: '', password: '', email: '' })

// 粒子背景与滑块相关变量
const particleCanvas = ref(null)
const sliderContainer = ref(null)
const sliderPosition = ref(0)
const sliderVerified = ref(false)
const sliderMax = ref(0)
let isDragging = false
let startX = 0
let animationFrame

// --- 初始化粒子背景 ---
const initParticles = () => {
  const canvas = particleCanvas.value
  const ctx = canvas.getContext('2d')
  let particles = []
  const resize = () => { if (canvas) { canvas.width = window.innerWidth; canvas.height = window.innerHeight } }
  class P {
    constructor() { 
      this.x = Math.random() * canvas.width; 
      this.y = Math.random() * canvas.height; 
      this.vx = (Math.random() - 0.5) * 0.5; 
      this.vy = (Math.random() - 0.5) * 0.5; 
      this.r = Math.random() * 1.5 
    }
    draw() { ctx.beginPath(); ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2); ctx.fillStyle = 'rgba(14, 165, 233, 0.3)'; ctx.fill() }
    update() { 
      this.x += this.vx; this.y += this.vy; 
      if (this.x < 0 || this.x > canvas.width) this.vx *= -1; 
      if (this.y < 0 || this.y > canvas.height) this.vy *= -1 
    }
  }
  for (let i = 0; i < 80; i++) particles.push(new P())
  const animate = () => { 
    if (!ctx) return
    ctx.clearRect(0, 0, canvas.width, canvas.height); 
    particles.forEach(p => { p.update(); p.draw() }); 
    animationFrame = requestAnimationFrame(animate) 
  }
  window.addEventListener('resize', resize); resize(); animate()
}

const updateSliderMax = () => { 
  // 只有在登录模式且 DOM 存在时才计算
  if (isLogin.value && sliderContainer.value) {
    sliderMax.value = sliderContainer.value.offsetWidth - 46 
  }
}

// --- 核心重写：提交逻辑 ---
const handleSubmit = async () => {
  // 1. 验证策略：仅在登录模式下强制校验滑块
  if (isLogin.value && !sliderVerified.value) {
    alert('请先完成滑块验证')
    return
  }

  loading.value = true
  try {
    const payload = isLogin.value
      ? {
          username: form.username,
          password: form.password
        }
      : {
          username: form.username,
          password: form.password,
          email: form.email
        }

    const url = isLogin.value ? '/login' : '/register'
    const res = await request.post(url, payload)
    
    // 2. 处理成功响应
    if (res.data.success) {
      if (isLogin.value) {
        // 登录：持久化存储
        localStorage.setItem('token', 'true')
        if (res.data.user) {
          localStorage.setItem('user', JSON.stringify(res.data.user))
        }
        alert(res.data.message || '登录成功')
        await router.push(router.currentRoute.value.query.redirect || '/')
      } else {
        // 注册：引导登录
        alert(res.data.message || '注册成功，请进行登录')
        switchMode(true) // 切换到登录，此时滑块会重新出现
      }
    }
  } catch (e) {
    // 3. 核心修复：捕获后端 409 等错误消息
    if (e.response && e.response.data) {
      // 这里的消息对应后端：如 "该用户名已被占用" 或 "该邮箱已被绑定"
      alert(e.response.data.message || '请求失败，请稍后重试') 
    } else {
      alert('无法连接到服务器，请检查网络')
    }
    
    // 登录失败则重置滑块，注册失败无需重置
    if (isLogin.value) resetSlider()
  } finally {
    loading.value = false
  }
}

// --- 辅助逻辑 ---
const switchMode = (val) => { 
  isLogin.value = val
  resetSlider() 
  showPassword.value = false
  // 清空表单数据
  form.username = ''
  form.password = ''
  form.email = ''
  
  // 切换回登录模式时，给 Vue 渲染滑块组件的时间
  if (val) {
    nextTick(updateSliderMax)
  }
}

const resetSlider = () => { sliderPosition.value = 0; sliderVerified.value = false }
const startDrag = (e) => { 
  if (!isLogin.value || sliderVerified.value) return
  isDragging = true
  startX = (e.touches ? e.touches[0].clientX : e.clientX) - sliderPosition.value
  updateSliderMax() 
}
const onDrag = (e) => { 
  if (!isDragging || sliderVerified.value) return
  let x = (e.touches ? e.touches[0].clientX : e.clientX) - startX
  sliderPosition.value = Math.max(0, Math.min(x, sliderMax.value)) 
}
const stopDrag = () => { 
  if (!isDragging) return
  isDragging = false
  if (sliderPosition.value >= sliderMax.value * 0.96) { 
    sliderPosition.value = sliderMax.value
    sliderVerified.value = true 
  } else { 
    sliderPosition.value = 0 
  } 
}

onMounted(() => { 
  if (localStorage.getItem('token') === 'true') {
    router.replace('/')
    return
  }
  initParticles()
  updateSliderMax()
  window.addEventListener('mousemove', onDrag)
  window.addEventListener('mouseup', stopDrag)
  window.addEventListener('touchmove', onDrag)
  window.addEventListener('touchend', stopDrag)
  window.addEventListener('resize', updateSliderMax) 
})

onBeforeUnmount(() => { 
  cancelAnimationFrame(animationFrame)
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('mouseup', stopDrag)
  window.removeEventListener('touchmove', onDrag)
  window.removeEventListener('touchend', stopDrag)
  window.removeEventListener('resize', updateSliderMax)
})
</script>

<style scoped>
.auth-wrapper { position: fixed; inset: 0; display: flex; align-items: center; justify-content: center; background: #f8fafc; overflow: hidden; font-family: system-ui, sans-serif; }
.particle-canvas { position: absolute; inset: 0; z-index: 1; pointer-events: none; }
.data-background { position: absolute; inset: 0; z-index: 0; }
.grid-layer { position: absolute; inset: 0; background-image: radial-gradient(#cbd5e1 1px, transparent 1px); background-size: 40px 40px; opacity: 0.2; }
.glow-orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.3; }
.orb-1 { width: 600px; height: 600px; background: #bae6fd; top: -200px; left: -100px; }
.orb-2 { width: 500px; height: 500px; background: #f0fdf4; bottom: -100px; right: -50px; }

.auth-card { position: relative; z-index: 10; width: 90%; max-width: 400px; background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.7); border-radius: 24px; padding: 40px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1); }
.auth-toggle { display: flex; position: relative; background: rgba(241, 245, 249, 0.8); padding: 4px; border-radius: 12px; margin-bottom: 32px; }
.toggle-slider { position: absolute; width: calc(50% - 4px); height: calc(100% - 8px); background: #fff; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.toggle-slider.is-register { transform: translateX(100%); }
.toggle-btn { flex: 1; z-index: 1; border: none; background: none; color: #64748b; font-size: 14px; font-weight: 600; cursor: pointer; padding: 10px 0; }
.toggle-btn.active { color: #0f172a; }

.form-group { margin-bottom: 20px; }
.input-label { display: block; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 8px; }
.input-box { position: relative; }
.password-wrapper { display: flex; align-items: center; }
.eye-icon { position: absolute; right: 12px; cursor: pointer; color: #94a3b8; display: flex; }
input { width: 100%; padding: 12px 16px; background: rgba(255,255,255,0.5); border: 1px solid #e2e8f0; border-radius: 12px; font-size: 14px; transition: 0.2s; box-sizing: border-box; }
input:focus { background: #fff; border-color: #3b82f6; outline: none; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); }

.slider-captcha { position: relative; height: 46px; background: rgba(241, 245, 249, 0.6); border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
.slider-text { position: absolute; inset: 0; text-align: center; line-height: 46px; font-size: 13px; color: #94a3b8; pointer-events: none; z-index: 2; }
.slider-fill { position: absolute; height: 100%; background: #3b82f6; opacity: 0.1; }
.slider-thumb { position: absolute; top: 3px; left: 3px; width: 40px; height: 40px; background: #fff; border-radius: 9px; display: flex; align-items: center; justify-content: center; cursor: grab; box-shadow: 0 2px 6px rgba(0,0,0,0.1); z-index: 3; }
.slider-captcha.verified { background: #f0fdf4; border-color: #86efac; }
.slider-captcha.verified .slider-thumb { background: #22c55e; color: #fff; cursor: default; }

.submit-btn { width: 100%; padding: 14px; margin-top: 12px; border: none; border-radius: 12px; background: #0f172a; color: #fff; font-weight: 600; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; }
.submit-btn:hover:not(:disabled) { background: #1e293b; transform: translateY(-1px); }
.submit-btn:disabled { background: #e2e8f0; color: #94a3b8; cursor: not-allowed; }
.loader { width: 18px; height: 18px; border: 2px solid #fff; border-bottom-color: transparent; border-radius: 50%; animation: rot 0.8s linear infinite; }
@keyframes rot { to { transform: rotate(360deg); } }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.3s ease; }
.fade-slide-enter-from, .fade-slide-leave-to { opacity: 0; transform: translateY(-10px); }
</style>
