<template>

    <el-container style="height: 100%;border: 1px solid #eee">
        <!-- 侧边栏导航 -->
        <el-aside>
            <tsne-sidebar :lessons="lessons" :currentLessonIndex="currentLessonIndex" @navigate-to="navigateToLesson" />
        </el-aside>

        <!-- 主内容区域 -->
        <el-main>
            <div class="tutorial-content">
                <h1>t-SNE降维算法互动教程</h1>

                <!-- 已完成的教学片段 -->
                <div v-for="(lesson, index) in completedLessons" :key="'completed-' + index" :id="'lesson-' + index">
                    <component :is="lesson.component" :isCompleted="true" :userAnswers="userResponses[index]" />
                    <el-divider></el-divider>
                </div>

                <!-- 当前正在学习的片段 -->
                <div v-if="currentLesson" :id="'lesson-' + currentLessonIndex">
                    <component :is="currentLesson.component" :isCompleted="false"
                        @lesson-completed="completeCurrentLesson" @user-response="saveUserResponse" />
                </div>

                <!-- 教程完成提示 -->
                <div v-if="isCompleted" class="tutorial-completed">
                    <el-result icon="success" title="恭喜你完成了t-SNE算法的学习！">
                        <template #extra>
                            <el-button type="primary" @click="restartTutorial">重新学习</el-button>
                        </template>
                    </el-result>
                </div>
            </div>

        </el-main>
    </el-container>

</template>

<script>
import TsneSidebar from './TsneSidebar.vue';
import Lesson1Introduction from './lessons/TsneIntroduction.vue';
import Lesson2DimensionalityReduction from './lessons/TsneCompare.vue';
import Lesson3TsneBasics from './lessons/TsneBasic.vue';
import Lesson4TsneMath from './lessons/TsneMath.vue';
import Lesson5TsneParameters from './lessons/TsneParameters.vue';
import Lesson6TsneAdvanced from './lessons/TsneAdvanced.vue';
// import Lesson7TsneApplications from './lessons/TsneApplications.vue';




// 引入更多教学组件...

export default {
    name: 'TsneInteractiveTutorial',
    components: {
        TsneSidebar,
        Lesson1Introduction,
        Lesson2DimensionalityReduction,
        Lesson3TsneBasics,
        Lesson4TsneMath,
        Lesson5TsneParameters,
        Lesson6TsneAdvanced,
        // Lesson7TsneApplications,
        // 注册更多教学组件...
    },
    data() {


        return {

            lessons: [
                { id: 1, title: '1. 介绍', component: 'Lesson1Introduction' },
                { id: 2, title: '2. 什么是降维', component: 'Lesson2DimensionalityReduction' },
                { id: 3, title: '3. t-SNE基础', component: 'Lesson3TsneBasics' },
                { id: 4, title: '4. t-SNE数学原理', component: 'Lesson4TsneMath' },
                { id: 5, title: '5. t-SNE超参数', component: 'Lesson5TsneParameters' },
                { id: 6, title: '6. t-SNE高级应用', component: 'Lesson6TsneAdvanced' },
                // { id: 7, title: '7. t-SNE实际应用', component: 'Lesson7TsneApplications' },
                // 更多教学片段...
            ],
            currentLessonIndex: 0,
            completedLessons: [],
            userResponses: {},
            isCompleted: false
        };
    },
    computed: {
        currentLesson() {
            if (this.currentLessonIndex < this.lessons.length) {
                return this.lessons[this.currentLessonIndex];
            }
            return null;
        }
    },
    methods: {
        completeCurrentLesson() {
            // 将当前片段移到已完成列表
            this.completedLessons.push(this.lessons[this.currentLessonIndex]);

            // 移动到下一个片段
            this.currentLessonIndex++;

            // 检查是否完成所有片段
            if (this.currentLessonIndex >= this.lessons.length) {
                this.isCompleted = true;
            }

            // 滚动到新的当前片段
            this.$nextTick(() => {
                if (!this.isCompleted) {
                    const element = document.getElementById('lesson-' + this.currentLessonIndex);
                    if (element) {
                        element.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            });
        },
        saveUserResponse(response) {
            // 保存用户的回答
            this.$set(this.userResponses, this.currentLessonIndex, response);
        },
        navigateToLesson(index) {
            // 只允许导航到已完成的片段
            if (index < this.completedLessons.length) {
                const element = document.getElementById('lesson-' + index);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                }
            }
        },
        restartTutorial() {
            // 重置教程状态
            this.currentLessonIndex = 0;
            this.completedLessons = [];
            this.userResponses = {};
            this.isCompleted = false;
        }
    }
};
</script>

<style scoped>
.tsne-tutorial-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.tutorial-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.tutorial-completed {
    padding: 40px 0;
    text-align: center;
}
</style>