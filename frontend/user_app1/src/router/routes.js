
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue'), name: 'Index' },
      { path: '/Advanced', component: () => import('pages/AdvancedSettings.vue'), name: 'AdvancedSettings'},
      { path: '/results', component: () => import('pages/ResultsPage.vue'), name: 'Results'},
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
