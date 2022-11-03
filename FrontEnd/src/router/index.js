import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login.vue'
import Home from '@/components/Home.vue'
import Welcome from '@/components/Welcome.vue'
import Users from '@/components/user/Users.vue'

Vue.use(Router)

 const router = new Router({
    routes: [
      {path: '/', redirect: '/login'},
      {path: '/login', component: Login},
      {
        path: '/home', 
        component: Home, 
        redirect: '/welcome',
        // 嵌套子组件
        children:[
          {path: '/welcome', component: Welcome},
          {path: '/users', component: Users},
      ]},
    ]
})

// 挂载路由导航守卫
/*
  to 将要访问的路径
  from 表示从哪个路径跳转而来
  next 是一个函数，表示放行
      - next()  允许放校
      - next('/login')  强制跳转到指定路由
*/
router.beforeEach((to, from, next)=>{
  if (to.path === "/login"){
      next()
  }else{
      // 获取token
      const tokenStr =  window.sessionStorage.getItem("token");
      if (tokenStr){
          next()
      }else{
          next("/login")
      }

  }

})

export default router