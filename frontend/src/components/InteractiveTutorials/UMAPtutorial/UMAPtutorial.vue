<template>
    <el-container style="height: 100%;border: 1px solid #eee">
        <el-aside width="250px">
            <sidebar :sections="sections" @section-click="scrollToSection" :currentSection="currentSection" />
        </el-aside>
        <el-main ref="mainContent">
            <div class="tutorial-content" ref="tutorialContent">
                <h1 class="tutorial-title">UMAP降维算法交互式教程</h1>

                <!-- 各教学片段组件 -->
                <section1-introduction ref="section1" id="section1" @complete="markSectionComplete(1)"
                    @scrollToSection="scrollToSection(2)" />
                <section2-intuition ref="section2" id="section2" @complete="markSectionComplete(2)"
                    @scrollToSection="scrollToSection(3)" />
                <section3-math-foundation ref="section3" id="section3" @complete="markSectionComplete(3)"
                    @scrollToSection="scrollToSection(4)" />
                <section4-algorithm ref="section4" id="section4" @complete="markSectionComplete(4)"
                    @scrollToSection="scrollToSection(5)" />
                <section5-graph ref="section5" id="section5" @complete="markSectionComplete(5)"
                    @scrollToSection="scrollToSection(6)" />
                <section6-embedding ref="section6" id="section6" @complete="markSectionComplete(6)"
                    @scrollToSection="scrollToSection(7)" />
                <section7-parameters ref="section7" id="section7" @complete="markSectionComplete(7)"
                    @scrollToSection="scrollToSection(8)" />
                <section8-comparison ref="section8" id="section8" @complete="markSectionComplete(8)"
                    @scrollToSection="scrollToSection(9)" />
                <section9-applications ref="section9" id="section9" @complete="markSectionComplete(9)"
                    @scrollToSection="scrollToSection(10)" />
                <section10-implementation ref="section10" id="section10" @complete="markSectionComplete(10)"
                    @scrollToSection="scrollToSection(11)" />
                <section11-case-study ref="section11" id="section11" @complete="markSectionComplete(11)" />
            </div>
        </el-main>
    </el-container>
</template>

<script>
import Sidebar from './SideBar.vue';
import Section1Introduction from './lessons/UMAPintroduction.vue';
import Section2Intuition from './lessons/UMAPintuition.vue';
import Section3MathFoundation from './lessons/UMAPmath.vue';
import Section4Algorithm from './lessons/UMAPalgorithm.vue';
import Section5Graph from './lessons/UMAPgraph.vue';
import Section6Embedding from './lessons/UMAPembedding.vue';
import Section7Parameters from './lessons/UMAPparameters.vue';
import Section8Comparison from './lessons/UMAPcompare.vue';
import Section9Applications from './lessons/UMAPapplication.vue';
import Section10Implementation from './lessons/UMAPimplementation.vue';
import Section11CaseStudy from './lessons/UMAPcaseStudy.vue';

export default {
    name: 'TutorialView',
    components: {
        Sidebar,
        Section1Introduction,
        Section2Intuition,
        Section3MathFoundation,
        Section4Algorithm,
        Section5Graph,
        Section6Embedding,
        Section7Parameters,
        Section8Comparison,
        Section9Applications,
        Section10Implementation,
        Section11CaseStudy
    },
    data() {
        return {
            currentSection: 1,
            completedSections: [],
            sections: [
                { id: 1, title: 'UMAP简介', ref: 'section1' },
                { id: 2, title: 'UMAP直观理解', ref: 'section2' },
                { id: 3, title: '数学基础', ref: 'section3' },
                { id: 4, title: '算法步骤概述', ref: 'section4' },
                { id: 5, title: '图构建', ref: 'section5' },
                { id: 6, title: '低维嵌入', ref: 'section6' },
                { id: 7, title: '参数详解', ref: 'section7' },
                { id: 8, title: '与其他算法比较', ref: 'section8' },
                { id: 9, title: '应用场景', ref: 'section9' },
                { id: 10, title: '实现与优化', ref: 'section10' },
                { id: 11, title: '案例分析', ref: 'section11' }
            ]
        }
    },
    mounted() {
        // 改为监听el-main容器的滚动事件
        const mainContent = this.$refs.mainContent.$el;
        if (mainContent) {
            mainContent.addEventListener('scroll', this.handleScroll);
        }
        // localStorage.removeItem('umap-completed-sections');
        // 检查本地存储中是否有完成记录
        // const storedCompleted = localStorage.getItem('umap-completed-sections');
        // if (storedCompleted) {
        //     this.completedSections = JSON.parse(storedCompleted);
        // }
    },
    beforeDestroy() {
        // 移除el-main容器的滚动事件监听
        const mainContent = this.$refs.mainContent.$el;
        if (mainContent) {
            mainContent.removeEventListener('scroll', this.handleScroll);
        }
    },
    methods: {
        scrollToSection(sectionId) {
            const sectionRef = this.$refs[`section${sectionId}`];
            const mainContent = this.$refs.mainContent.$el;

            if (sectionRef && mainContent) {
                // 获取节点相对位置
                const sectionElement = sectionRef.$el;
                const offsetTop = this.getOffsetTop(sectionElement, mainContent);

                // 使用scrollTo方法在el-main内滚动
                mainContent.scrollTo({
                    top: offsetTop - 20, // 添加一些顶部偏移，使位置更合适
                    behavior: 'smooth'
                });

                this.currentSection = sectionId;
            }
        },

        // 计算元素相对于容器的顶部偏移
        getOffsetTop(element, container) {
            let offsetTop = 0;
            let currentElement = element;

            while (currentElement && currentElement !== container) {
                offsetTop += currentElement.offsetTop;
                currentElement = currentElement.offsetParent;
            }

            return offsetTop;
        },

        handleScroll(event) {
            // 获取滚动容器
            const mainContent = event.target;
            const scrollTop = mainContent.scrollTop;

            // 确定当前在视口中的部分
            const visibleSections = [];

            for (const section of this.sections) {
                const sectionRef = this.$refs[section.ref];
                if (sectionRef) {
                    const sectionElement = sectionRef.$el;
                    const offsetTop = this.getOffsetTop(sectionElement, mainContent);
                    const height = sectionElement.offsetHeight;

                    // 计算与视口顶部的距离
                    const distanceFromTop = offsetTop - scrollTop;

                    visibleSections.push({
                        id: section.id,
                        distanceFromTop: distanceFromTop,
                        // 如果元素部分或全部可见
                        visible: distanceFromTop < mainContent.clientHeight && distanceFromTop + height > 0
                    });
                }
            }

            // 找出可见且最靠近视口顶部的部分
            const visibleTopSections = visibleSections
                .filter(section => section.visible && section.distanceFromTop <= 100)
                .sort((a, b) => b.distanceFromTop - a.distanceFromTop);

            if (visibleTopSections.length > 0) {
                this.currentSection = visibleTopSections[0].id;
            }
        },

        markSectionComplete(sectionId) {
            if (!this.completedSections.includes(sectionId)) {
                this.completedSections.push(sectionId);
                // 保存到本地存储
                // localStorage.setItem('umap-completed-sections', JSON.stringify(this.completedSections));
            }
        }
    }
}
</script>

<style scoped>
.tutorial-container {
    display: flex;
    height: 90%;
    /* min-height: 100vh; */
}

.tutorial-content {
    padding: 20px;
}

.tutorial-title {
    text-align: center;
    margin-bottom: 40px;
    color: #409EFF;
}

/* 确保el-main容器可以滚动 */
.el-main {
    overflow-y: auto;
    height: 100%;
    padding: 20px;
}
</style>