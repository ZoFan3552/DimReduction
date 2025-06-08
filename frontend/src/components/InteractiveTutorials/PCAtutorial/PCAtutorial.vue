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
                    <el-badge v-if="segment.completed" value="✓" class="segment-completed-badge" type="success" />
                </el-menu-item>
            </el-menu>
        </div>

        <!-- 主要内容区域 -->
        <div class="main-content">
            <div class="content-container">
                <!-- 教学片段组件们 -->
                <div v-for="(segment, index) in visibleSegments" :key="segment.id" :id="segment.id"
                    class="segment-container" ref="segmentRefs">
                    <component :is="segment.component" :saved-answer="segmentAnswers[segment.id]"
                        @answer-submitted="handleAnswerSubmitted($event, segment.id)">
                    </component>
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
import { tutorialProgressService } from './service/PCAservice'

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
        PracticalExample
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
                { id: 'practical-example', title: '9. 实际案例', component: 'PracticalExample', completed: false }
            ],
            // 当前可见的教学片段（随着用户进度增加）
            progress: 1, // 初始进度：只显示第一个片段
            userId: null, // 将从用户认证系统获取
            segmentAnswers: {}, // 存储用户对每个片段的回答
            isLoading: true // 加载状态标志
        }
    },
    computed: {
        // 根据当前进度计算可见的教学片段
        visibleSegments() {
            return this.segments.slice(0, this.progress);
        },
        // 获取已完成的片段ID列表
        completedSegmentIds() {
            return this.segments
                .filter(segment => segment.completed)
                .map(segment => segment.id);
        },
        // 计算已完成的章节数
        completeCount() {
            return this.completedSegmentIds.length;
        }
    },
    created() {
        // 从用户认证系统获取用户ID
        this.userId = localStorage.getItem('userId');

        // 如果有用户ID，则从后端加载进度
        if (this.userId) {
            this.loadUserProgress();
        } else {
            this.isLoading = false;
            this.$message.warning('未检测到用户登录，进度将不会被保存');
        }
    },
    methods: {
        // 加载用户进度
        async loadUserProgress() {
            this.isLoading = true;
            console.log("加载进度");

            try {
                const response = await tutorialProgressService.getProgress(this.userId);
                const userData = response;
                console.log("加载进度回应", response);

                if (userData) {
                    // 恢复进度 - 已完成的章节数加1（因为下一章节已解锁）
                    this.progress = userData.completeCount + 1 || 1;

                    // 恢复完成状态
                    if (userData.completeCount > 0) {
                        // 根据完成数量标记已完成的章节
                        for (let i = 0; i < userData.completeCount; i++) {
                            this.$set(this.segments[i], 'completed', true);
                        }
                    }

                    // 恢复各章节的答案
                    this.segments.forEach(segment => {
                        // 将 segment.id (intro-to-pca) 转换为驼峰式 (introToPca)
                        const camelCaseKey = segment.id.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());

                        // 检查 userData 中是否存在转换后的键
                        if (userData[camelCaseKey]) {
                            this.$set(this.segmentAnswers, segment.id, userData[camelCaseKey]);
                        }
                    });
                    console.log("加载进度时的segmentAnswers", this.segmentAnswers)

                    this.$message.success('已恢复您的学习进度');
                }
            } catch (error) {
                console.error('加载用户进度失败:', error);
                this.$message.error('加载进度失败，将使用默认进度');
            } finally {
                this.isLoading = false;
            }
        },

        // 保存用户进度
        async saveUserProgress() {
            if (!this.userId) {
                this.$message.warning('未登录用户无法保存进度');
                return;
            }

            try {
                // 构建与数据库结构匹配的数据
                const progressData = {
                    userId: this.userId,
                    completeCount: this.completeCount
                };

                // 添加每个章节的答案
                Object.keys(this.segmentAnswers).forEach(segmentId => {
                    progressData[segmentId] = this.segmentAnswers[segmentId];
                });

                await tutorialProgressService.saveProgress(progressData);
                console.log('进度保存成功');
            } catch (error) {
                console.error('保存进度失败:', error);
                this.$message.error('保存进度失败');
            }
        },

        // 处理章节问题的回答
        async handleAnswerSubmitted(answer, segmentId) {
            // 保存该章节的回答
            this.$set(this.segmentAnswers, segmentId, answer);
            console.log("segmentAnswers", this.segmentAnswers);
            console.log("segmentId", segmentId);
            console.log("answer", answer);


            if (this.userId) {
                console.log("用户id", this.userId);
                try {
                    // 更新特定章节的回答
                    await tutorialProgressService.updateSegmentAnswer(
                        this.userId,
                        segmentId,
                        answer
                    );
                    console.log(`章节 ${segmentId} 的回答已保存`);
                } catch (error) {
                    console.error(`保存章节 ${segmentId} 回答失败:`, error);
                    this.$message.error('保存回答失败');
                }
            }
        },

        // 用于解锁下一个教学片段
        async unlockNextSegment(completedId) {
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

                // 保存完成状态到后端
                if (this.userId) {
                    try {
                        await tutorialProgressService.markSegmentComplete(
                            this.userId,
                            completedId
                        );

                        // 完整保存当前进度
                        // await this.saveUserProgress();

                        this.$message.success(`恭喜完成 ${this.segments[index].title}！`);
                    } catch (error) {
                        console.error('更新章节完成状态失败:', error);
                        this.$message.error('更新进度失败');
                    }
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

.segment-completed-badge {
    margin-left: 5px;
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