import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/code',
    name: 'code',
    component: () => import('@/components/mainComponents/CodeView.vue')
  },
  {
    path: '/flowChart',
    name: 'flowChart',
    component: () => import('@/views/FlowChartView.vue')
  },
  {
    path: '/mainSelect',
    name: 'mainSelect',
    component: () => import('@/views/MainSelectView.vue')
  },
  {
    path: '/PCA',
    name: 'PCA',
    component: () => import('@/views/algorithmTutorialView/PCAtutorialView.vue'),
  },
  {
    path: '/LDA',
    name: 'LDA',
    component: () => import('@/views/algorithmTutorialView/LDAtutorialView.vue'),
  },
  {
    path: '/tSNE',
    name: 'tSNE',
    component: () => import('@/views/algorithmTutorialView/tSNEtutorialView.vue'),
  },
  {
    path: '/UMAP',
    name: 'UMAP',
    component: () => import('@/views/algorithmTutorialView/UMAPtutorialView.vue'),
  },
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/LogIn.vue')
  },
]

const router = new VueRouter({
  routes
})

export default router
