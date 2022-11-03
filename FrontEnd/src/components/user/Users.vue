<template>
    <div>
        <!-- 面包屑导航 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>用户列表</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 卡片视图区域 -->
        <el-card>
            <el-row :gutter="20">
                <el-col :span="8">
                      <el-input placeholder="请输入内容" v-model="queryInfo.query" clearable @clear="getUserList">
                        <el-button slot="append" icon="el-icon-search" @click="getUserList"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" @click="addDialogVisible = true">添加用户</el-button>
                </el-col>
            </el-row>

            <!-- 表格区域 -->
            <el-table :data="userList" border stripe>
                <el-table-column type="index"></el-table-column>
                <el-table-column label="姓名" prop="username"></el-table-column>
                <el-table-column label="邮箱" prop="email"></el-table-column>
                <el-table-column label="电话" prop="mobile"></el-table-column>
                <el-table-column label="角色" prop="role_name"></el-table-column>
                <el-table-column label="状态">
                    <!-- 指定一个作用域插槽 通过 scope.row 可以拿到每一行的数据 -->
                    <template slot-scope="scope">
                        <!-- {{ scope.row }} -->
                        <!-- 指定了scope后，table-column的prop会被插槽效果覆盖，因此table-column不需要再指定scope了 -->
                        <el-switch v-model="scope.row.mg_state" ctive-color="#13ce66" inactive-color="#ff4949"  @change="changeUserState(scope.row)">
                        </el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <!-- 编辑按钮 -->
                        <el-button type="primary" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row.id)"></el-button>
                        <!-- 删除按钮 -->
                        <el-button type="danger" icon="el-icon-delete" size="mini"></el-button>
                        <!-- 分配权限 -->
                        <el-tooltip effect="dark" content="权限分配" placement="top" :enterable="false">
                            <el-button type="warning" icon="el-icon-setting" size="mini"></el-button>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页区域 -->
            <el-pagination @size-change="handleSizeChange"  @current-change="handleCurrentChange" :current-page="queryInfo.pagenum"
            :page-sizes="[1, 2, 5, 10]" :page-size="queryInfo.pagesize" layout="total, sizes, prev, pager, next, jumper" :total="total">
            </el-pagination>

            <!-- 新增用户信息弹窗 -->
            <el-dialog title="新增用户" :visible.sync="addDialogVisible" width="50%" @close="addDialogClosed">
                <span>新增用户</span>

                <!-- 主体内容区域 -->
                <el-form :model="addForm" :rules="addFormRules" ref="addFormRef" label-width="80px">
                    <el-form-item label="用户名" prop="username">
                        <el-input v-model="addForm.username"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input v-model="addForm.password"></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱" prop="email">
                        <el-input v-model="addForm.email"></el-input>
                    </el-form-item>
                    <el-form-item label="手机号" prop="mobile">
                        <el-input v-model="addForm.mobile"></el-input>
                    </el-form-item>
                </el-form>

                <!-- 按钮区域 -->
                <span slot="footer" class="dialog-footer">
                    <el-button @click="addDialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="addUser">确 定</el-button>
                </span>
            </el-dialog>

            <!-- 编辑用户信息弹窗 -->
            <el-dialog title="提示" :visible.sync="editDialogVisible" width="30%">
            <span>编辑用户信息</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editDialogVisible = false">确 定</el-button>
            </span>
            </el-dialog>


        </el-card>
    </div>
</template>

<script>
export default {
    data(){
        // 自定义校验邮箱的规则
        // rule--规则  value--要校验的值  callback--回调函数
        var checkEmail = (rule, value, callback) => {
            // 校验邮箱的正则表达式
            const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
            if (regEmail.test(value)){
                // 合法的邮箱，直接调用回调函数，通过验证
                return callback()
            }
            // 非法的邮箱，调用回调函数，抛出异常
            callback(new Error('请输入合法的邮箱')) 
        };

        // 自定义校验手机号的规则
        var checkMobile = (rule, value, callback) => {
            // 校验手机号的正则表达式
            const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/
            if (regMobile.test(value)){
                // 合法的手机号，直接调用回调函数，通过验证
                return callback()
            }
            // 非法的手机号，调用回调函数，抛出异常
            callback(new Error('请输入合法的手机号')) 
        };

        return {
            queryInfo: {
                query: "",
                // 当前页数
                pagenum: 1,
                // 当前每页显示多少数据
                pagesize: 2
            },

            userList: [],
            total: 0,

            // 控制新增弹窗显示或隐藏
            addDialogVisible: false,

            // 用户表单数据
            addForm: {
                username: '',
                password: '',
                email: '',
                mobile: '',
            },

            // 用户表单校验规则
            addFormRules: {
                username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    // 使用自定义的校验规则
                    { validator: checkEmail, trigger: 'blur' }
                ],
                mobile: [
                    { required: true, message: '请输入手机号', trigger: 'blur' },
                    // 使用自定义的校验规则
                    { validator: checkMobile, trigger: 'blur' }
                ],
            },

            // 控制编辑用户信息弹窗的显示与隐藏
            editDialogVisible: false,

            // 编辑用户的信息
            editForm: {}

        }
    },

    created(){
        this.getUserList()
    },

    methods: {
        getUserList(){
            // get 请求携带参数
            this.$http.get("users", {params: this.queryInfo}).then((response) => {
                const res = response.data
                if (res.meta.status !== 200) {
                    this.$message.error("获取用户列表失败")
                }else {
                    this.userList = res.data.users
                    this.total = res.data.total
                }
            })
        },

        // 当 pagesize 改变时触发事件
        handleSizeChange(newSize){
            // console.log(newSize)
            this.queryInfo.pagesize = newSize;
            this.getUserList()
        },

        // 当前页码发生改变时触发事件
        handleCurrentChange(newPage){
            // console.log(newPage)
            this.queryInfo.pagenum = newPage;
            this.getUserList()
        },

        // 监听用户状态改变
        async changeUserState(userinfo){
            const {data: res} = await this.$http.put(`users/${userinfo.id}/state/${userinfo.mg_state}`)
            if (res.meta.status === 200) {
               this.$message.success("更新用户状态成功")
            }else {
                userinfo.mg_state = !userinfo.mg_state
                this.$message.error("更新用户状态失败")
            }
        },

        // 监听用户新增窗口的关闭事件
        addDialogClosed(){
            this.$refs.addFormRef.resetFields()
        },

        // 点击按钮，添加用户
        addUser(){
            this.$refs.addFormRef.validate(valid => {
                if (!valid) return

                // 可以发起添加用户的请求
                this.$http.post('users', this.addForm).then((response) => {
                    const res = response.data;
                    if (res.meta.status !== 201){
                        return this.$message.error("添加用户失败")
                    }

                    this.$message.success("添加用户成功")

                    // 隐藏对话框
                    this.addDialogVisible = false;

                    // 刷新页面数据
                    this.getUserList()
                })
            })
        },

        // 显示编辑用户信息弹窗
        showEditDialog(id){
            this.$http.get('users/' + id).then((response) => {
                const res = response.data;
                if (res.meta.status !==200){
                    return this.$message.error("查询用户信息失败")
                }

                this.editForm = res.data;
            });
            // this.editDialogVisible = true;
            console.log(this.editForm);
        }
    }
}
</script>

<style scoped>
    .el-pagination {
        margin-top: 16px;
    }

</style>