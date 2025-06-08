<template>
    <div class="sidebar">
        <div class="sidebar-header">
            <h2>UMAP教程目录</h2>
        </div>
        <el-menu :default-active="String(currentSection)" class="section-menu" background-color="#fff" text-color="#000"
            active-text-color="#ffd04b">
            <el-menu-item v-for="section in sections" :key="section.id" :index="String(section.id)"
                @click="$emit('section-click', section.id)">
                <i class="el-icon-document"></i>
                <span>{{ section.id }}. {{ section.title }}</span>
                <el-badge v-if="isCompleted(section.id)" class="section-badge" type="success" value="✓" />
            </el-menu-item>
        </el-menu>
        <div class="sidebar-footer">
            <p>进度: {{ completionPercentage }}%</p>
            <el-progress :percentage="completionPercentage" :color="progressColor">
            </el-progress>
        </div>
    </div>
</template>

<script>
export default {
    // name: 'Sidebar',
    props: {
        sections: {
            type: Array,
            required: true
        },
        currentSection: {
            type: Number,
            required: true
        }
    },
    computed: {
        completionPercentage() {
            const completedSections = this.getCompletedSections().length;
            return Math.round((completedSections / this.sections.length) * 100);
        },
        progressColor() {
            const percentage = this.completionPercentage;
            if (percentage < 30) return '#909399';
            if (percentage < 70) return '#409EFF';
            return '#67C23A';
        }
    },
    methods: {
        isCompleted(sectionId) {
            return this.getCompletedSections().includes(sectionId);
        },
        getCompletedSections() {
            const storedCompleted = localStorage.getItem('umap-completed-sections');
            return storedCompleted ? JSON.parse(storedCompleted) : [];
        }
    }
}
</script>

<style scoped>
.sidebar {
    height: 100%;
    /* position: fixed;
    left: 0;
    top: 0;
    bottom: 0; */
    width: 250px;
    background-color: #c1bcbc;
    color: #fff;
    display: flex;
    flex-direction: column;
    z-index: 10;
}

.sidebar-header {
    padding: 20px 15px;
    text-align: center;
    border-bottom: 1px solid #fff;
}

.sidebar-header h2 {
    font-size: 1.2rem;
    margin: 0;
}

.section-menu {
    flex: 1;
    overflow-y: auto;
}

.section-badge {
    margin-left: 8px;
}

.sidebar-footer {
    padding: 15px;
    border-top: 1px solid #fff;
}

.sidebar-footer p {
    margin: 0 0 10px;
    text-align: center;
    font-size: 0.9rem;
}
</style>