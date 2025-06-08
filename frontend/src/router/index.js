import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/test',
  //   name: 'test',
  //   component: () => import('@/views/testView.vue')
  // },
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
  // {
  //   path: '/main',
  //   name: 'main',
  //   component: () => import('@/views/MainView.vue'),
  //   children: [
  //     // {
  //     //   path: 'BasicTutorTest',
  //     //   name: 'BasicTutorTest',
  //     //   component: () => import('@/components/InteractiveTutorials/BasicTutorialTest/BasicTutorialTest.vue'),
  //     // },

  //     // {
  //     //   path: 'PCA',
  //     //   name: 'PCA',
  //     //   component: () => import('@/views/algorithmTutorialView/PCAtutorialView.vue'),
  //     // },
  //     // {
  //     //   path: 'LDA',
  //     //   name: 'LDA',
  //     //   component: () => import('@/views/algorithmTutorialView/LDAtutorialView.vue'),
  //     // },
  //     // {
  //     //   path: 'Normalization',
  //     //   name: 'Normalization',
  //     //   component: () => import('@/components/articleComponents/NormalizationArticle.vue'),
  //     // },
  //     // {
  //     //   path: 'KLDiv',
  //     //   name: 'KLDiv',
  //     //   component: () => import('@/components/articleComponents/KLdivArticle.vue'),
  //     // },
  //     // {
  //     //   path: 'tSNE',
  //     //   name: 'tSNE',
  //     //   component: () => import('@/components/InteractiveTutorials/tSNEtutorial/TsneTutorial.vue'),
  //     // },
  //     // {
  //     //   path: 'UMAP',
  //     //   name: 'UMAP',
  //     //   component: () => import('@/components/InteractiveTutorials/UMAPtutorial/UMAPtutorial.vue'),
  //     // },
  //     // {
  //     //   path: 'article',
  //     //   name: 'article',
  //     //   component: () => import('@/components/articleComponents/ArticleDisplay.vue'),
  //     // },
  //   ]
  // },
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/LogIn.vue')
  },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = new VueRouter({
  routes
})

export default router
