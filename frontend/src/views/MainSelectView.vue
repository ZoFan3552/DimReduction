<template>
  <div class="algorithm-selector">
    <div class="section" v-for="(section, index) in algorithmSections" :key="index">
      <el-card class="box-card">
        <div slot="header" class="card-header">{{ section.title }}</div>
        <div class="button-group">
          <el-button v-for="algo in section.algorithms" :key="algo.name" type="primary" plain round class="algo-button"
            @click="goToAlgorithm(algo.route)">
            {{ algo.name }}
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlgorithmSelector',
  data() {
    return {
      algorithmSections: [
        {
          title: '数据降维算法',
          algorithms: [
            { name: 'PCA', route: '/PCA' },
            { name: 'LDA', route: '/LDA' },
            { name: 't-SNE', route: '/tSNE' },
            { name: 'UMAP', route: '/UMAP' },
            // { name: 'MDS', route: '/main/MDS' },
            // { name: 'BasicTutorTest', route: '/main/BasicTutorTest' },
            { name: '代码编辑', route: '/code' },
            { name: '算法流程图', route: '/flowChart' },

          ]
        },
        // {
        //   title: '图布局算法',
        //   algorithms: [
        //     { name: '布局算法1', route: '/algorithm/layout1' },
        //     { name: '布局算法2', route: '/algorithm/layout2' },
        //     { name: '布局算法3', route: '/algorithm/layout3' }
        //   ]
        // },
        // {
        //   title: '时序算法',
        //   algorithms: [
        //     { name: '时序算法1', route: '/algorithm/time1' },
        //     { name: '时序算法2', route: '/algorithm/time2' },
        //     { name: '时序算法3', route: '/algorithm/time3' }
        //   ]
        // }
      ]
    };
  },
  methods: {
    goToAlgorithm(route) {
      this.$router.push(route).catch(err => {
        // 忽略重复导航错误（错误码 NAVIGATION_DUPLICATED）
        if (err.name !== 'NavigationDuplicated') {
          console.error('导航失败:', err);
        }
      });
    }
  }
};
</script>

<style scoped>
.algorithm-selector {
  height: 100%;
  padding: 30px;
  background-color: #f5f7fa;
  overflow: auto;
}

.section {
  margin-bottom: 30px;
}

.box-card {
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  font-size: 16px;
  font-weight: bold;
  padding: 10px 0;
}

.button-group {
  /* display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 20px 10px; */
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.algo-button {
  /* min-width: 100px;
  height: 40px;
  font-size: 14px; */
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
</style>
