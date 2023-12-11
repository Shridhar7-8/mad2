import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from '../views/AdminDashboard.vue'
import createProduct from '../views/createProduct.vue'
import createUser from '../views/createUser.vue'
import deleteProduct from '../views/deleteProduct.vue'
import editProduct from '../views/editProduct.vue'
import editSection from '../views/editSection.vue'
import deleteSection from '../views/deleteSection.vue'
import createSection from '../views/createSection.vue'
import viewSection from '../views/viewSection.vue'
import login from '../views/login.vue'
import summary from '../views/summary.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard
    },
    {
      path: '/register',
      name:'register',
      component: createUser
    },
    {
      path: '/create_section',
      name: 'create_section',
      component: createSection
    },
    {
      path: 'edit_section/:sectionId',
      name: 'edit_section',
      component: editSection
    },
    {
      path: '/delete_section/:sectionId',
      name: 'delete_section',
      component: deleteSection
    },
    {
      path: '/create_product',
      name: 'create_product',
      component: createProduct
    },
    {
      path: '/edit_product/:productId',
      name: 'edit_product',
      component: editProduct
    },
    {
      path: 'delete_product/:productId',
      name: 'delete_product',
      component: deleteProduct
    },
    {
      path: '/view_section/:sectionId',
      name: 'view_section',
      component: viewSection
    },
    {
      path: '/summary',
      name: 'summary',
      component: summary
    }
    
  ]
})

export default router
