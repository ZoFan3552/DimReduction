<template>
  <div id="app">

    <!-- <router-link to="/main"> 主页面 </router-link>
    <router-link to="/test"> test页面 </router-link> -->


    <router-view />
  </div>
</template>

<style>
#app {
  height: 100vh;
}

/* 设置整个滚动条的宽度和高度 */
::-webkit-scrollbar {
  width: 5px;
  /* 适用于垂直滚动条 */
  height: 5px;
  /* 适用于水平滚动条 */
}

/* 滚动条轨道（背景） */
::-webkit-scrollbar-track {
  background: #f5f5f5;
  /* 浅灰色背景 */
  border-radius: 4px;
}

/* 滚动条滑块（拖动的小块） */
::-webkit-scrollbar-thumb {
  background: #d5d4d4;
  /* 默认颜色 */
  border-radius: 4px;
  transition: background 0.3s;
}

/* 悬停时滚动条变色 */
::-webkit-scrollbar-thumb:hover {
  background: #999;
}

/* 滚动条两端的按钮（如果有的话） */
::-webkit-scrollbar-button {
  display: none;
}
</style>
