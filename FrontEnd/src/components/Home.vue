<template>
  <el-container class="home_container">
    <!-- 导航头部区域 -->
    <el-header>
      <div>
        <img src="@/assets/logo.png" alt="" />
        <span>电商后台管理系统</span>
      </div>
      <el-button @click="logout" type="info">退出</el-button></el-header>

    <!-- 主题内容区域 -->
    <el-container>
      <!-- 左侧区域 -->
      <el-aside :width="isCollapse ? '63px' : '200px'">
        <!-- 设置菜单折叠 -->
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <!-- 左侧菜单栏区域 -->
        <el-menu background-color="#333744" text-color="#fff" active-text-color="#409EFF" unique-opened :collapse="isCollapse" :collapse-transition="false" router :default-active="activePath">
          <!-- 一级菜单区域 -->
          <el-submenu :index="item.id + ''" v-for="item in menusList" :key="item.id">
            <!-- 菜单模板区域 -->
            <template slot="title">
              <!-- 菜单图标 -->
              <i :class="iconObj[item.id]"></i>
              <!-- 菜单文本 -->
              <span>{{ item.authName }}</span>
            </template>
            <el-menu-item :index="'/' + subItem.path" v-for="subItem in item.children" :key="subItem.id" @click="saveNavState('/' + subItem.path)">
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span>{{ subItem.authName }}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <!-- 占位符，嵌套显示子组件 -->
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      // 左侧菜单栏列表
      menusList: [],
      isCollapse: false,
      activePath: "",
      iconObj: {
        125: "iconfont icon-icon_user",
        103: "iconfont icon-tijikongjian",
        101: "iconfont icon-shangpin",
        102: "iconfont icon-danju",
        145: "iconfont icon-baobiao",
      },
    };
  },

  created() {
    this.getMenusList();
    this.activePath = window.sessionStorage.getItem("activePath")
  },

  methods: {
    logout() {
      // 清楚浏览器缓存
      window.sessionStorage.clear();
      // 强制跳转到登录页面
      this.$router.push("/login");
      this.$message.success("退出登录成功");
    },

    async getMenusList() {
      const { data: res } = await this.$http.get("menus");
      if (res.meta.status === 200) {
        this.menusList = res.data;
      } else {
        this.$message.error(res.meta.msg);
      }
    },

    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    },

    // 保存链接的激活状态
    saveNavState(activePath){
      window.sessionStorage.setItem("activePath", activePath)
      this.activePath = activePath
    }
  },
};
</script>

<style scoped>
.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  color: #eee;
  font-size: 20px;
}

.el-aside {
  background-color: #333744;
}

.el-main {
  background: #eaedf1;
}

.home_container {
  height: 100%;
}

.el-header > div > img {
  height: 50px;
  width: 50px;
  border-radius: 50%;
  border: solid 1px #eee;
}

.el-header > div > span {
  margin-left: 15px;
}

.el-header > div {
  display: flex;
  align-items: center;
}

.iconfont {
  margin-right: 10px;
}

.el-aside > .el-menu {
  border-right: none;
}

.toggle-button {
  background-color: #4a5064;
  line-height: 24px;
  font-size: 10px;
  color: #fff;
  text-align: center;
  cursor: pointer;
  letter-spacing: 0.2em;
}
</style>