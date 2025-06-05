<template>

    <div class="login-register">
        <!-- <div>
            <router-link to="/mainSelect">登录</router-link>
        </div> -->
        <!-- <el-alert v-if="errorMsg" :title="errorMsg" type="error" show-icon></el-alert> -->
        <div class="contain">
            <div class="big-box" :class="{ active: isLogin }">
                <div class="big-contain" key="bigContainLogin" v-if="isLogin">
                    <div class="btitle">账户登录</div>
                    <div class="bform">
                        <input type="text" placeholder="学号" v-model="form.studentId">
                        <span class="errTips" v-if="emailError">* 邮箱填写错误 *</span>
                        <input type="password" placeholder="密码" v-model="form.password">
                        <span class="errTips" v-if="emailError">* 密码填写错误 *</span>
                    </div>
                    <button class="bbutton" @click="login">登录</button>
                </div>
                <div class="big-contain" key="bigContainRegister" v-else>
                    <div class="btitle">创建账户</div>
                    <div class="bform">
                        <!-- <input type="text" placeholder="用户名" v-model="form.username"> -->
                        <span class="errTips" v-if="existed">* 用户名已经存在！ *</span>
                        <input type="text" placeholder="学号" v-model="form.studentId">
                        <input type="password" placeholder="密码" v-model="form.password">
                    </div>
                    <button class="bbutton" @click="register">注册</button>
                </div>
            </div>
            <div class="small-box" :class="{ active: isLogin }">
                <div class="small-contain" key="smallContainRegister" v-if="isLogin">
                    <div class="stitle">你好，朋友!</div>
                    <p class="scontent">让我们开始数据降维算法可视化教学实验</p>
                    <!-- <button class="sbutton" @click="changeType">注册</button> -->
                </div>
                <div class="small-contain" key="smallContainLogin" v-else>
                    <div class="stitle">欢迎回来!</div>
                    <p class="scontent">与我们保持联系，请登录你的账户</p>
                    <button class="sbutton" @click="changeType">登录</button>
                </div>
            </div>
            <!-- <el-alert v-if="errorMsg" :title="errorMsg" type="error" show-icon></el-alert> -->
        </div>


    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'login-register',
    data() {
        return {
            isLogin: true,
            errorMsg: '',
            emailError: false,
            passwordError: false,
            existed: false,
            form: {
                studentId: '',
                password: '',
                // username: '',
                // useremail: '',
                // userpwd: ''
            },
        }
    },
    methods: {
        changeType() {
            this.isLogin = !this.isLogin
            // this.form.username = ''
            // this.form.useremail = ''
            // this.form.userpwd = ''
            this.form.studentId = ''
            this.form.password = ''
        },
        login() {
            // this.$router.push('/mainSelect') // 替换为你的跳转页
            const self = this;
            if (self.form.studentId != "" && self.form.password != "") {
                axios.post('http://116.198.200.118:8080/api/student/login', this.form)
                    .then(res => {
                        console.log("登录信息", res);
                        if (res.data.code === 200) {
                            this.$message.success('登录成功')
                            // 清空全部 localStorage
                            // localStorage.clear();
                            localStorage.setItem('userId', this.form.studentId)
                            this.$router.push('/mainSelect') // 替换为你的跳转页
                        } else {
                            // this.errorMsg = res.data.msg
                            alert(res.data.msg);
                        }
                    })
                    .catch(() => {
                        // this.errorMsg = '服务器错误，请稍后重试'
                        alert('服务器错误，请稍后重试');
                    })
            } else {
                alert("填写不能为空！");
            }
        },
        register() {
            const self = this;
            if (self.form.username != "" && self.form.studentId != "" && self.form.password != "") {
                console.log("点击注册")
            } else {
                alert("填写不能为空！");
            }
        }
    }
}
</script>

<style scoped="scoped">
html,
body {
    overflow: hidden;
    height: 90%;
    margin: 0;
    padding: 0;
}

.login-register {
    width: 100vw;
    height: 100vh;
    box-sizing: border-box;
    background-image: url("@/assets/login_background.png");
}

.contain {
    max-width: 800px;
    /* 添加最大高度限制 */
    /* 允许容器内部滚动 */
    width: 60%;
    height: 60%;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    border-radius: 20px;
    box-shadow: 0 0 3px #f0f0f0,
        0 0 6px #f0f0f0;
}

.big-box {
    width: 70%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 30%;
    transform: translateX(0%);
    transition: all 1s;
}

.big-contain {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.btitle {
    font-size: 1.5em;
    font-weight: bold;
    color: rgb(57, 167, 176);
}

.bform {
    width: 100%;
    height: 40%;
    padding: 2em 0;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
}

.bform .errTips {
    display: block;
    width: 50%;
    text-align: left;
    color: red;
    font-size: 0.7em;
    margin-left: 1em;
}

.bform input {
    width: 50%;
    height: 30px;
    border: none;
    outline: none;
    border-radius: 10px;
    padding-left: 2em;
    background-color: #f0f0f0;
}

.bbutton {
    width: 20%;
    height: 40px;
    border-radius: 24px;
    border: none;
    outline: none;
    background-color: rgb(57, 167, 176);
    color: #fff;
    font-size: 0.9em;
    cursor: pointer;
}

.small-box {
    width: 30%;
    height: 100%;
    background: linear-gradient(135deg, rgb(57, 167, 176), rgb(56, 183, 145));
    position: absolute;
    top: 0;
    left: 0;
    transform: translateX(0%);
    transition: all 1s;
    border-top-left-radius: inherit;
    border-bottom-left-radius: inherit;
}

.small-contain {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.stitle {
    font-size: 1.5em;
    font-weight: bold;
    color: #fff;
}

.scontent {
    font-size: 0.8em;
    color: #fff;
    text-align: center;
    padding: 2em 4em;
    line-height: 1.7em;
}

.sbutton {
    width: 60%;
    height: 40px;
    border-radius: 24px;
    border: 1px solid #fff;
    outline: none;
    background-color: transparent;
    color: #fff;
    font-size: 0.9em;
    cursor: pointer;
}

.big-box.active {
    left: 0;
    transition: all 0.5s;
}

.small-box.active {
    left: 100%;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
    border-top-right-radius: inherit;
    border-bottom-right-radius: inherit;
    transform: translateX(-100%);
    transition: all 1s;
}
</style>