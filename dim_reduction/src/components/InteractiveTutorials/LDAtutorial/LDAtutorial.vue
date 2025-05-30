<!-- LdaTutorial.vue - 主容器组件 -->
<template>
    <div class="lda-tutorial">
        <SideNavigation :sections="sections" :activeSection="activeSection" @navigate="scrollToSection" />

        <div ref="contentContainer" class="content-container">
            <h1 class="main-title">LDA线性判别分析降维算法教程</h1>

            <div ref="tutorialContent" class="tutorial-content">
                <!-- 动态加载所有教学组件 -->
                <component v-for="(section, index) in sections" :key="section.id" :is="section.component"
                    :ref="'section-' + section.id" @complete="markSectionComplete(section.id)"
                    @save-answer="saveUserAnswer(section.id, $event)" :userAnswers="userAnswers[section.id] || ''"
                    :class="{ 'section-complete': completedSections.includes(section.id) }" :sectionIndex="index + 1"
                    :totalSections="sections.length" />
            </div>

            <el-backtop target=".content-container"></el-backtop>
        </div>
    </div>
</template>

<script>
import SideNavigation from './SideBar.vue'
import IntroductionToLDA from './lessons/LDAintroduction.vue'
import DimensionalityReductionConcept from './lessons/ReductionConcept.vue'
import LDAMathematicalFoundation from './lessons/LDAmath.vue'
import WithinClassScatterMatrix from './lessons/WithinClassScatterMatrix.vue'
import BetweenClassScatterMatrix from './lessons/BetweenClassScatterMatrix.vue'
import GeneralizedEigenvalueFormulation from './lessons/GeneralizedEigenvalue.vue'
// import LDAvsOtherMethods from './lessons/LDAvsOtherMethods.vue'
import LDAImplementationStepByStep from './lessons/LDAImplementationStep.vue'
// import FisherLinearDiscriminant from './lessons/FisherLinearDiscriminant.vue'
// import EigenvalueDecomposition from './lessons/EigenvalueDecomposition.vue'
import LDAVisualizationExamples from './lessons/LDAVisualizationExamples.vue'
import ApplicationsOfLDA from './lessons/LDAapplication.vue'
// import LDALimitations from './lessons/LDALimitations.vue'
// import AdvancedLDATopics from './lessons/AdvancedLDATopics.vue'
// import FinalQuiz from './lessons/FinalQuiz.vue'
import axios from '@/utils/myAxios';

export default {
    name: 'LdaTutorial',
    components: {
        SideNavigation,
        IntroductionToLDA,
        DimensionalityReductionConcept,
        LDAMathematicalFoundation,
        WithinClassScatterMatrix,
        BetweenClassScatterMatrix,
        GeneralizedEigenvalueFormulation,
        // LDAvsOtherMethods,
        LDAImplementationStepByStep,
        // FisherLinearDiscriminant,
        // EigenvalueDecomposition,
        LDAVisualizationExamples,
        ApplicationsOfLDA,
        // LDALimitations,
        // AdvancedLDATopics,
        // FinalQuiz
    },
    data() {
        return {
            activeSection: 'introduction-to-lda',
            completedSections: [],
            userId: null, // 用户ID将从会话或登录状态获取
            userAnswers: {}, // 存储用户回答
            sections: [
                { id: 'introduction-to-lda', title: '1. LDA介绍', component: 'IntroductionToLDA' },
                { id: 'dimensionality-reduction', title: '2. 降维概念', component: 'DimensionalityReductionConcept' },
                { id: 'lda-mathematical-foundation', title: '3. LDA数学基础', component: 'LDAMathematicalFoundation' },
                { id: 'within-class-scatter', title: '4. 类内散布矩阵', component: 'WithinClassScatterMatrix' },
                { id: 'between-class-scatter', title: '5. 类间散布矩阵', component: 'BetweenClassScatterMatrix' },
                { id: 'eigenvalue-formulation', title: '6. 广义特征值公式', component: 'GeneralizedEigenvalueFormulation' },
                // { id: 'fisher-discriminant', title: '7. Fisher线性判别式', component: 'FisherLinearDiscriminant' },
                // { id: 'eigenvalue-decomposition', title: '8. 特征值分解', component: 'EigenvalueDecomposition' },
                { id: 'lda-implementation', title: '7. LDA实现步骤', component: 'LDAImplementationStepByStep' },
                // { id: 'lda-vs-other-methods', title: '10. LDA对比其他方法', component: 'LDAvsOtherMethods' },
                { id: 'lda-visualization', title: '8. LDA可视化示例', component: 'LDAVisualizationExamples' },
                { id: 'lda-applications', title: '9. LDA应用场景', component: 'ApplicationsOfLDA' },
                // { id: 'lda-limitations', title: '13. LDA局限性', component: 'LDALimitations' },
                // { id: 'advanced-lda', title: '14. 高级LDA主题', component: 'AdvancedLDATopics' },
                // { id: 'final-quiz', title: '15. 总结测验', component: 'FinalQuiz' }
            ]
        }
    },
    mounted() {
        // 获取当前用户ID
        this.getUserId().then(() => {
            // 从后端获取用户进度
            this.loadUserProgress();
        });

        // 监听滚动以更新当前显示的部分
        this.setupScrollObserver();
    },
    methods: {
        // 获取用户ID的方法
        async getUserId() {
            try {

                // const response = await axios.get('/user/current');
                this.userId = localStorage.getItem('userId');
                return this.userId;
            } catch (error) {
                console.error('获取用户ID失败:', error);
                // 如果获取失败，可以使用一个临时ID或提示用户登录
                // this.userId = 'guest-' + Math.random().toString(36).substring(2, 15);
                return null;
            }
        },

        // 加载用户进度
        async loadUserProgress() {
            if (!this.userId) return;

            try {
                const response = await axios.get(`/lda-tutorial/progress/${this.userId}`);
                const progressData = response;
                console.log("LDA教程的进度response", response);

                // 设置已完成的章节
                if (progressData.completedSections && Array.isArray(progressData.completedSections)) {
                    this.completedSections = progressData.completedSections;
                }

                // 设置用户回答
                if (progressData.answers) {
                    this.userAnswers = progressData.answers;
                }

                // 如果有已完成的章节，可以跳转到上次学习的位置
                // if (this.completedSections.length > 0) {
                //     // 找到最后完成的章节的下一个章节
                //     const lastCompletedIndex = this.sections.findIndex(
                //         section => section.id === this.completedSections[this.completedSections.length - 1]
                //     );

                //     if (lastCompletedIndex >= 0 && lastCompletedIndex < this.sections.length - 1) {
                //         // 跳转到下一个未完成的章节
                //         const nextSectionId = this.sections[lastCompletedIndex + 1].id;
                //         this.$nextTick(() => {
                //             this.scrollToSection(nextSectionId);
                //         });
                //     }
                // }
            } catch (error) {
                console.error('加载用户进度失败:', error);
            }
        },

        // 保存用户进度到后端
        async saveUserProgress(sectionId = null, answer = null) {
            if (!this.userId) return;

            try {
                // 构建要发送到后端的数据对象
                const progressData = {
                    userId: this.userId,
                    // completedSections: this.completedSections,
                    // answers: this.userAnswers
                };

                // 如果提供了特定章节和回答，更新那个章节的回答
                if (sectionId && answer !== null) {
                    progressData.sectionId = sectionId;
                    progressData.answer = answer;
                }
                console.log('进度提交', progressData);
                await axios.post('/lda-tutorial/answer', progressData);
                console.log('用户进度保存成功');
            } catch (error) {
                console.error('保存用户进度失败:', error);
            }
        },

        // 保存用户回答
        saveUserAnswer(sectionId, answer) {
            console.log(`保存用户在章节 ${sectionId} 的回答:`, answer);
            this.userAnswers = {
                ...this.userAnswers,
                [sectionId]: answer
            };

            // 保存到后端
            this.saveUserProgress(sectionId, answer);
        },

        scrollToSection(sectionId) {
            console.log("LDA选中章节", sectionId);
            this.activeSection = sectionId;
            const element = this.$refs['section-' + sectionId];
            const contentContainer = this.$refs.contentContainer;

            if (element && element[0] && contentContainer) {
                // 获取目标元素相对于内容容器的位置
                const elementTop = element[0].$el.offsetTop;

                // 使用内容容器的scrollTop属性来滚动，而不是scrollIntoView
                contentContainer.scrollTo({
                    top: elementTop - 20, // 减去一些偏移量，使滚动位置更合适
                    behavior: 'smooth'
                });
            }
        },

        markSectionComplete(sectionId) {
            if (!this.completedSections.includes(sectionId)) {
                this.completedSections.push(sectionId);
                // 保存进度到后端
                // this.saveUserProgress();
            }
        },

        setupScrollObserver() {
            // 使用 Intersection Observer API 检测当前可见的部分
            const options = {
                root: this.$refs.contentContainer, // 使用内容容器作为观察的根元素
                rootMargin: '0px',
                threshold: 0.5
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        // 从组件中提取section id
                        const sectionElement = entry.target;
                        // 查找对应的section id
                        for (const section of this.sections) {
                            const sectionRef = this.$refs['section-' + section.id];
                            if (sectionRef && sectionRef[0] && sectionRef[0].$el === sectionElement) {
                                if (section.id !== this.activeSection) {
                                    this.activeSection = section.id;
                                }
                                break;
                            }
                        }
                    }
                });
            }, options);

            // 为每个部分添加observer
            this.sections.forEach(section => {
                const element = this.$refs['section-' + section.id];
                if (element && element[0]) {
                    observer.observe(element[0].$el);
                }
            });
        }
    }
}
</script>

<style scoped>
/* 修改 content-container 的样式 */
.content-container {
    flex: 1;
    padding: 20px 30px;
    overflow-y: auto;
    /* 启用垂直滚动 */
    height: calc(100vh - 60px);
    /* 减去顶部导航栏的高度 */
    scroll-behavior: smooth;
}

/* 确保 tutorial-content 不撑开父容器 */
.tutorial-content {
    margin: 0 auto;
    overflow: visible;
    /* 允许内容自由扩展 */
}

.lda-tutorial {
    display: flex;
    height: 100%;
    overflow: hidden;
}

.main-title {
    text-align: center;
    margin-bottom: 30px;
    color: #409EFF;
}

.section-complete {
    border-left: 4px solid #67C23A;
}
</style>