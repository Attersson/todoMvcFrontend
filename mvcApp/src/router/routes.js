
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: 'todos', component: () => import('pages/Todos.vue') },
      { path: 'todos/new', component: () => import('pages/TodoEdit.vue') },
      { path: 'todos/:id', component: () => import('pages/TodoEdit.vue') },
      { path: 'about', component: () => import('pages/About.vue') }
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
