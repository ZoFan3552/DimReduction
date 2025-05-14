<template>
    <div class="experiment-container">
        <!-- 顶部导航 -->
        <el-menu :default-active="activeIndex" class="experiment-nav" mode="horizontal" @select="handleNavChange"
            background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
            <el-menu-item index="tutorial">
                <i class="el-icon-reading"></i> 互动教程
            </el-menu-item>
            <el-menu-item index="flowchart">
                <i class="el-icon-share"></i> 流程图
            </el-menu-item>
            <el-menu-item index="code">
                <i class="el-icon-edit-outline"></i> 代码编辑
            </el-menu-item>
        </el-menu>



        <!-- 内容区域  -->
        <div class="experiment-content">
            <keep-alive>
                <component :is="currentComponent" @step-completed="nextStep"></component>
            </keep-alive>
        </div>


    </div>
</template>

<script>
import TutorialComponent from '@/components/InteractiveTutorials/LDAtutorial/LDAtutorial.vue';
import FlowchartComponent from '@/views/FlowChartView.vue';
import CodeEditorComponent from '@/components/mainComponents/CodeView.vue';

export default {
    name: 'ExperimentNavigation',
    components: {
        TutorialComponent,
        FlowchartComponent,
        CodeEditorComponent
    },
    data() {
        return {
            activeIndex: 'tutorial',
            currentStep: 0,
            steps: [
                { title: '算法介绍', component: 'TutorialComponent' },
                { title: '算法流程', component: 'FlowchartComponent' },
                { title: '代码实现', component: 'CodeEditorComponent' },
            ],
            componentMap: {
                'tutorial': 'TutorialComponent',
                'flowchart': 'FlowchartComponent',
                'code': 'CodeEditorComponent'
            }
        };
    },
    computed: {
        currentComponent() {
            // 根据当前步骤或导航选择返回对应组件
            const stepComponent = this.steps[this.currentStep].component;
            return this.activeIndex === 'auto' ? stepComponent : this.componentMap[this.activeIndex];
        }
    },
    methods: {
        handleNavChange(key) {
            this.activeIndex = key;
            // 可以在这里添加导航变更的逻辑
        },
        nextStep() {
            if (this.currentStep < this.steps.length - 1) {
                this.currentStep++;
                // 如果导航栏设为自动跟随步骤
                if (this.activeIndex === 'auto') {
                    // 更新导航高亮
                    const componentName = this.steps[this.currentStep].component;
                    for (const [key, value] of Object.entries(this.componentMap)) {
                        if (value === componentName) {
                            this.activeIndex = key;
                            break;
                        }
                    }
                }
            }
        },
        prevStep() {
            if (this.currentStep > 0) {
                this.currentStep--;
                // 同上，处理导航高亮
                if (this.activeIndex === 'auto') {
                    const componentName = this.steps[this.currentStep].component;
                    for (const [key, value] of Object.entries(this.componentMap)) {
                        if (value === componentName) {
                            this.activeIndex = key;
                            break;
                        }
                    }
                }
            }
        },
        completeExperiment() {
            // 实验完成逻辑
            this.$message.success('恭喜，您已完成数据降维算法实验！');
        }
    }
};
</script>

<style scoped>
.experiment-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    /* 使用视口高度 */
    overflow: hidden;
    /* 防止整体滚动 */
}

.experiment-nav {
    margin-bottom: 20px;
}

.experiment-steps {
    margin: 20px 0;
    padding: 0 20px;
}

.experiment-content {
    flex: 1;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    /* padding: 20px; */
    padding-left: 20px;
    padding-right: 20px;
    overflow: hidden;
    /* 允许内容区域滚动 */
    background-color: #f9f9f9;
    margin-bottom: 10px;
}

.experiment-controls {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 10px;
    padding: 10px 0;
}
</style>