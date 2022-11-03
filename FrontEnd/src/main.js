// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { Button, Form, FormItem, Input, Message, Container, Header, Aside, Main, Menu, 
  Submenu, MenuItem, Breadcrumb, BreadcrumbItem, Card, Row, Col, Table, TableColumn, 
  Switch, Tooltip, Pagination, Dialog } from 'element-ui'
import axios from 'axios'

/* 导入全局样式 */
import '@/assets/css/global.css'
import '@/assets/fonts/iconfont.css'

// 配置根本请求路径
// axios.defaults.baseURL = "http://127.0.0.1:8000/"
axios.defaults.baseURL = "http://82.157.53.213:8886/api/private/v1/"

// 通过请求拦截器在请求头中添加Token，所有的请求都会先经过这个拦截器
axios.interceptors.request.use((config)=>{
  console.log(config);
  // config为一个请求对象，里面包含了 headers 等各种属性
  config.headers.Authorization = window.sessionStorage.getItem("token")
  // 最后必须返回请求对象
  return config
})

Vue.config.productionTip = false
Vue.prototype.$http = axios

Vue.use(Form)
Vue.use(FormItem)
Vue.use(Button)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Switch)
Vue.use(Tooltip)
Vue.use(Pagination)
Vue.use(Dialog)

// Message配置和其他组件配置不太一样，需要在全局挂载才能使用
Vue.prototype.$message = Message

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
