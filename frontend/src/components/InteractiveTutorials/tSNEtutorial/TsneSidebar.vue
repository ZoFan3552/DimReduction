<template>
    <div class="sidebar-container">
        <h3>教程目录</h3>
        <el-menu :default-active="String(currentLessonIndex)" class="lesson-menu">
            <el-menu-item v-for="(lesson, index) in lessons" :key="lesson.id" :index="String(index)"
                @click="navigateTo(index)" :disabled="index > completedLessonCount">
                <span :class="{
                    'completed': index < completedLessonCount,
                    'current': index === currentLessonIndex,
                    'locked': index > completedLessonCount
                }">
                    {{ lesson.title }}
                    <i v-if="index < completedLessonCount" class="el-icon-check"></i>
                </span>
            </el-menu-item>
        </el-menu>

    </div>
</template>

<script>
export default {
    name: 'TsneSidebar',
    props: {
        lessons: {
            type: Array,
            required: true
        },
        currentLessonIndex: {
            type: Number,
            required: true
        }
    },
    computed: {
        completedLessonCount() {
            return this.currentLessonIndex;
        }
    },
    methods: {
        navigateTo(index) {
            // 只能导航到已完成的课程
            if (index <= this.completedLessonCount) {
                this.$emit('navigate-to', index);
            }
        }
    }
}
</script>

<style scoped>
.sidebar-container {
    background-color: #f5f7fa;
    height: 100%;
    border-right: 1px solid #e6e6e6;
    padding: 10px 0;
}

.lesson-menu {
    border-right: none;
}

.completed {
    color: #67c23a;
}

.current {
    font-weight: bold;
    color: #409eff;
}

.locked {
    color: #909399;
}
</style>