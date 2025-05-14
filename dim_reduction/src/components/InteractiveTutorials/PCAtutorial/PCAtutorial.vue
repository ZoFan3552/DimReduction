<template>
    <div class="pca-tutorial-container">
        <!-- 侧边导航栏 -->
        <div class="sidebar">
            <el-menu :default-active="activeSegment" class="segment-menu" @select="scrollToSegment">
                <div class="sidebar-header">
                    <h3>PCA降维算法教程</h3>
                </div>
                <el-menu-item v-for="(segment, index) in segments" :key="index" :index="segment.id">
                    {{ segment.title }}
                </el-menu-item>
            </el-menu>
        </div>

        <!-- 主要内容区域 -->
        <div class="main-content">
            <div class="content-container">
                <!-- 教学片段组件们 -->
                <div v-for="(segment, index) in visibleSegments" :key="segment.id" :id="segment.id"
                    class="segment-container" ref="segmentRefs">
                    <component :is="segment.component"></component>
                    <el-divider v-if="index < visibleSegments.length - 1"></el-divider>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import IntroToPCA from './lessons/PCAintroduction.vue'
import DataVariance from './lessons/PCAvar.vue'
import CovarianceMatrix from './lessons/PCAcov.vue'
import EigenvectorsAndValues from './lessons/PCAeig.vue'
import SelectingPCs from './lessons/PCAselect.vue'
import DimensionalityReduction from './lessons/PCAdimReduction.vue'
import PCAApplications from './lessons/PCAapplication.vue'
import PCALimitations from './lessons/PCAlimitation.vue'
import PracticalExample from './lessons/PCAexample.vue'
// import SummaryAdvanced from '@/components/pca-tutorial/SummaryAdvanced.vue'

export default {
    name: 'PCATutorial',
    components: {
        IntroToPCA,
        DataVariance,
        CovarianceMatrix,
        EigenvectorsAndValues,
        SelectingPCs,
        DimensionalityReduction,
        PCAApplications,
        PCALimitations,
        PracticalExample,
        // SummaryAdvanced
    },
    data() {
        return {
            activeSegment: 'intro-to-pca',
            // 所有可能的教学片段
            segments: [
                { id: 'intro-to-pca', title: '1. PCA简介', component: 'IntroToPCA', completed: false },
                { id: 'data-variance', title: '2. 数据方差', component: 'DataVariance', completed: false },
                { id: 'covariance-matrix', title: '3. 协方差矩阵', component: 'CovarianceMatrix', completed: false },
                { id: 'eigenvectors', title: '4. 特征向量与特征值', component: 'EigenvectorsAndValues', completed: false },
                { id: 'selecting-pcs', title: '5. 选择主成分', component: 'SelectingPCs', completed: false },
                { id: 'dimensionality-reduction', title: '6. 降维过程', component: 'DimensionalityReduction', completed: false },
                { id: 'pca-applications', title: '7. PCA应用', component: 'PCAApplications', completed: false },
                { id: 'pca-limitations', title: '8. PCA局限性', component: 'PCALimitations', completed: false },
                { id: 'practical-example', title: '9. 实际案例', component: 'PracticalExample', completed: false },
                // { id: 'summary-advanced', title: '10. 总结与进阶', component: 'SummaryAdvanced', completed: false }
            ],
            // 当前可见的教学片段（随着用户进度增加）
            progress: 1 // 初始进度：只显示第一个片段
        }
    },
    computed: {
        // 根据当前进度计算可见的教学片段
        visibleSegments() {
            return this.segments.slice(0, this.progress);
        }
    },
    methods: {
        // 用于解锁下一个教学片段
        unlockNextSegment(completedId) {
            // 标记当前片段为已完成
            const index = this.segments.findIndex(segment => segment.id === completedId);
            if (index !== -1) {
                this.$set(this.segments[index], 'completed', true);

                // 如果还有下一个片段，增加进度
                if (index + 1 < this.segments.length) {
                    this.progress = index + 2;

                    // 滚动到新解锁的片段
                    this.$nextTick(() => {
                        const nextSegment = this.segments[index + 1];
                        this.scrollToSegment(nextSegment.id);
                    });
                }
            }
        },

        // 滚动到指定片段
        scrollToSegment(id) {
            this.activeSegment = id;
            const element = document.getElementById(id);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    },
    // 提供一个事件总线给子组件通信
    provide() {
        return {
            unlockNextSegment: this.unlockNextSegment
        }
    }
}
</script>

<style scoped>
.pca-tutorial-container {
    display: flex;
    height: 100%;
    position: relative;
}

.sidebar {
    width: 250px;
    position: sticky;
    top: 0;
    height: 100%;
    max-height: 100%;
    background-color: #f8f9fa;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    overflow-y: auto;
    z-index: 10;
}

.sidebar-header {
    padding: 20px 15px;
    border-bottom: 1px solid #e6e6e6;
    background-color: #409EFF;
    color: white;
}

.segment-menu {
    border-right: none;
}

.main-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    height: 100%;
}

.content-container {
    max-width: 900px;
    margin: 0 auto;
}

.segment-container {
    margin-bottom: 40px;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>