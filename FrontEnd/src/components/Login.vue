<template>
  <div class="login_container">
      <div class="login_box">
          
        <!-- 头像区域 -->
        <div class="avatar">
            <img src="@/assets/logo.png" alt="">
        </div>

        <!-- 登陆表单区域 -->
        <el-form label-width="0px" class="login_form" :model="loginForm" :rules="loginFormRules" ref="loginFormRef">
            <!-- 用户名 -->
            <el-form-item prop="username">
                <el-input prefix-icon="iconfont icon-icon_user" v-model="loginForm.username"></el-input>
            </el-form-item>

            <!-- 密码 -->
            <el-form-item prop="password">
                <el-input prefix-icon="iconfont icon-3702mima" v-model="loginForm.password"></el-input>
            </el-form-item>

            <!-- 按钮区域 -->
            <el-form-item class="btns">
                <el-button type="primary" @click="login">登录</el-button>
                <el-button type="info" @click="resetLoginForm">重置</el-button>
            </el-form-item>

        </el-form>

      </div>
  </div>
</template>

<script>
    export default {
        data(){
            return {

                // 这是表单对象绑定的数据
                loginForm: {
                    username: "cdc",
                    password: "123456"
                },

                // 表单验证对象
                loginFormRules: {
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                        // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' }
                        // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }    
                    ]
                }
            }
        },

        methods: {
            resetLoginForm(){
                this.$refs.loginFormRef.resetFields()
            },

            login(){
                /*
                axios请求返回的是一个promise对象，异步请求，
                使用 async 定义异步方法，使用 await 等待异步方式执行结束接收结果
                */
                this.$refs.loginFormRef.validate(async (valid)=>{
                    // console.log(valid)
                    if (!valid) return;
                    const result = await this.$http.post("login",this.loginForm);
                    // console.log(result);
                    // 获取后台返回数据中的值
                    const res = result.data
                    if (res.meta.status === 200){
                        // console.log("登录成功");
                        this.$message.success("登陆成功");
                        /*
                        登陆成功的后续操作：
                            1. 将 token 保存到 SessionStorage 中
                            2. 跳转到首页组件
                        */
                       window.sessionStorage.setItem("token", res.data.token)
                       this.$router.push('/home')

                    }else{
                        // console.log("登陆失败");
                        this.$message.error("登陆失败");
                    }

                })

                // 也可以用 then 来等来请求结束再做操作
                // this.$refs.loginFormRef.validate((valid)=>{
                //     if (!valid) return;
                //     this.$http.post("login",this.loginForm).then((result)=>{
                //         console.log(result)
                //     }).catch((error) =>{
                //         console.log(error)
                //     })
                // })
            },
        }

    };
</script>

<style scoped>
    .login_container {
        background-color: #2b4b6b;
        height: 100%;
        width: 100%;

    }

    .login_box {
        width: 450px;
        height: 300px;
        background-color: #fff;
        border-radius: 3px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }

    .avatar {
        height: 130px;
        width: 130px;
        border: 1px solid #eee;
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 0 10px;
        position: absolute;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #fff;
    }

    .avatar > img {
        height: 100%;
        width: 100%;
        border-radius: 50%;
        background-color: #eee;
    }

    .btns {
        display: flex;
        justify-content: flex-end;
    }

    .login_form {
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 10px 30px;
        box-sizing: border-box;
    }

</style>