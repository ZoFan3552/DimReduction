<!-- SideNavigation.vue - 侧边导航组件 -->
<template>
    <div class="side-navigation">
        <div class="nav-header">
            <h3>教程目录</h3>
            <div class="progress-info">
                <el-progress type="circle" :percentage="completionPercentage" :width="80" :stroke-width="6"
                    :color="progressColors"></el-progress>
                <p class="progress-text">完成: {{ completedCount }}/{{ sections.length }}</p>
            </div>
        </div>

        <el-menu :default-active="activeSection" class="nav-menu" @select="handleSelect">
            <el-menu-item v-for="section in sections" :key="section.id" :index="section.id"
                :class="{ 'is-completed': isCompleted(section.id) }">
                <i class="el-icon-document"></i>
                <span>{{ section.title }}</span>
                <i v-if="isCompleted(section.id)" class="el-icon-check completion-icon"></i>
            </el-menu-item>
        </el-menu>

        <div class="nav-footer">
            <el-button type="primary" size="small" @click="resetProgress" icon="el-icon-refresh-right">
                重置进度
            </el-button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SideNavigation',
    props: {
        sections: {
            type: Array,
            required: true
        },
        activeSection: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            progressColors: [
                { color: '#f56c6c', percentage: 20 },
                { color: '#e6a23c', percentage: 40 },
                { color: '#5cb87a', percentage: 60 },
                { color: '#1989fa', percentage: 80 },
                { color: '#6f7ad3', percentage: 100 }
            ]
        }
    },
    computed: {
        completedCount() {
            return this.sections.filter(section => this.isCompleted(section.id)).length;
        },
        completionPercentage() {
            if (this.sections.length === 0) return 0;
            return Math.round((this.completedCount / this.sections.length) * 100);
        }
    },
    methods: {
        handleSelect(key) {
            this.$emit('navigate', key);
        },
        isCompleted(sectionId) {
            // 从本地存储检查完成状态
            const completedSections = this.getCompletedSections();
            return completedSections.includes(sectionId);
        },
        getCompletedSections() {
            const saved = localStorage.getItem('lda-tutorial-progress');
            if (saved) {
                try {
                    return JSON.parse(saved);
                } catch (e) {
                    console.error('Failed to parse completed sections:', e);
                    return [];
                }
            }
            return [];
        },
        resetProgress() {
            this.$confirm('确定要重置所有学习进度吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                localStorage.removeItem('lda-tutorial-progress');
                this.$message({
                    type: 'success',
                    message: '学习进度已重置'
                });
                // 触发父组件更新
                window.location.reload();
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消重置'
                });
            });
        }
    }
}
</script>

<style scoped>
.side-navigation {
    width: 260px;
    height: 100%;
    background-color: #f5f7fa;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #e6e6e6;
}

.nav-header {
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #ebeef5;
}

.nav-header h3 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #303133;
}

.progress-info {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.progress-text {
    margin-top: 8px;
    font-size: 14px;
    color: #606266;
}

.nav-menu {
    flex: 1;
    overflow-y: auto;
    border-right: none;
}

.nav-menu .el-menu-item.is-completed {
    color: #67C23A;
    position: relative;
}

.completion-icon {
    position: absolute;
    right: 10px;
    color: #67C23A;
}

.nav-footer {
    padding: 15px;
    text-align: center;
    border-top: 1px solid #ebeef5;
}
</style>