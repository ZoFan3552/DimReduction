<template>
    <div class="lesson-container">
        <!-- Markdown展示部分 -->
        <div class="content-section">
            <el-card class="markdown-content">
                <div v-html="renderedMarkdown"></div>
            </el-card>
        </div>

        <!-- 互动部分：PCA vs. t-SNE交互对比 -->
        <div v-if="!isCompleted" class="interactive-section">
            <el-card>
                <h3>PCA 与 t-SNE 的可视化比较</h3>
                <p>下面是同一个数据集分别用PCA和t-SNE降维的效果。拖动滑块来混合两种可视化效果，观察它们的区别。</p>

                <div class="visualization-container">
                    <div ref="visualizationContainer" class="d3-visualization"></div>
                    <el-slider v-model="visualizationBlendValue" :min="0" :max="100"
                        :format-tooltip="formatTooltip"></el-slider>
                </div>

                <div class="question-section">
                    <p>观察后，你认为t-SNE比PCA更擅长做什么？</p>
                    <el-radio-group v-model="userAnswer">
                        <el-radio label="global">保留全局结构（如整体方差方向）</el-radio>
                        <el-radio label="linear">发现线性关系</el-radio>
                        <el-radio label="clusters">揭示数据的聚类结构</el-radio>
                        <el-radio label="computation">降低计算复杂度</el-radio>
                    </el-radio-group>
                    <div class="action-buttons">
                        <el-button type="primary" @click="checkAnswer">提交答案</el-button>
                    </div>
                </div>
            </el-card>
        </div>

        <!-- 回应部分 -->
        <div v-if="showResponse" class="response-section">
            <el-card :class="{ 'correct-answer': isCorrect, 'wrong-answer': !isCorrect }">
                <div v-if="isCorrect">
                    <h3><i class="el-icon-success"></i> 回答正确!</h3>
                    <p>是的，t-SNE特别擅长揭示数据中的<strong>聚类结构</strong>。</p>
                    <p>通过我们的可视化对比，你可以看到：</p>
                    <ul>
                        <li>PCA是线性降维方法，它尝试保留数据中的全局结构（最大方差方向）</li>
                        <li>t-SNE则关注局部结构，能更好地展示数据点的聚类关系</li>
                        <li>当数据有明显的非线性聚类时，t-SNE通常能提供更有洞察力的可视化</li>
                    </ul>
                    <el-button type="success" @click="proceedToNext">继续学习</el-button>
                </div>
                <div v-else>
                    <h3><i class="el-icon-error"></i> 请再试一次</h3>
                    <p>查看可视化结果，注意两种方法的主要区别是什么？哪一种方法更好地展示了数据的聚类结构？</p>
                    <el-button @click="resetAnswer">重新选择</el-button>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
import { marked } from 'marked';
import * as d3 from 'd3';
import 'katex/dist/katex.min.css';


// 示例数据
const pcaData = [
    // 10个模拟PCA降维后的点
    { x: 10, y: 50, group: 1 }, { x: 15, y: 45, group: 1 }, { x: 20, y: 55, group: 1 },
    { x: 60, y: 30, group: 2 }, { x: 65, y: 25, group: 2 }, { x: 70, y: 35, group: 2 },
    { x: 30, y: 80, group: 3 }, { x: 35, y: 75, group: 3 }, { x: 40, y: 85, group: 3 },
    { x: 80, y: 10, group: 4 }
];

const tsneData = [
    // 同样10个点，但t-SNE降维后的位置 - 更明显地聚类
    { x: 10, y: 10, group: 1 }, { x: 15, y: 15, group: 1 }, { x: 12, y: 12, group: 1 },
    { x: 80, y: 10, group: 2 }, { x: 85, y: 15, group: 2 }, { x: 82, y: 12, group: 2 },
    { x: 10, y: 80, group: 3 }, { x: 15, y: 85, group: 3 }, { x: 12, y: 82, group: 3 },
    { x: 80, y: 80, group: 4 }
];

export default {
    name: 'Lesson2DimensionalityReduction',
    props: {
        isCompleted: {
            type: Boolean,
            default: false
        },
        userAnswers: {
            type: Array,
            default: null
        }
    },
    data() {
        return {
            markdown: `
  # 降维技术概览
  
  降维是将高维数据转换到低维表示的过程，同时尽可能保留原始数据的重要信息。
  
  ## 常见的降维技术
  
  1. **主成分分析 (PCA)**
     - 线性降维方法
     - 寻找数据方差最大的方向（主成分）
     - 特点：保留全局结构，计算效率高
     - 局限性：只能捕捉线性关系
  
  2. **多维缩放 (MDS)**
     - 试图保留原始空间中点与点之间的距离
     - 可以处理任意距离矩阵
     - 计算成本较高
  
  3. **局部线性嵌入 (LLE)**
     - 非线性降维方法
     - 假设每个数据点可以由其近邻点线性表示
     - 保留局部几何结构
  
  4. **t-SNE**
     - 非线性降维方法
     - 特别注重保留局部结构
     - 特别适合可视化和聚类发现
     - 计算复杂度高
  
  ## 如何选择合适的降维技术？
  
  选择合适的降维技术取决于：
  - 数据的性质（线性/非线性）
  - 任务的目标（可视化/建模）
  - 计算资源的限制
  - 是否需要保留全局或局部结构
  
  下面我们将通过交互式演示对比PCA和t-SNE的效果差异。
  
        `,
            userAnswer: '',
            showResponse: false,
            isCorrect: false,
            visualizationBlendValue: 0, // 默认显示PCA
            svg: null,
            pPoints: null,
            tPoints: null
        };
    },
    computed: {
        renderedMarkdown() {
            return marked(this.markdown);
        }
    },
    watch: {
        visualizationBlendValue() {
            this.updateVisualization();
        }
    },
    mounted() {
        // 如果已经完成，使用保存的答案
        if (this.isCompleted && this.userAnswers) {
            this.userAnswer = this.userAnswers;
            this.showResponse = true;
            this.isCorrect = true;
        }

        this.$nextTick(() => {
            this.initVisualization();
        });
    },
    methods: {
        initVisualization() {
            const width = 500;
            const height = 300;

            // 创建SVG
            this.svg = d3.select(this.$refs.visualizationContainer)
                .append('svg')
                .attr('width', width)
                .attr('height', height);

            // 创建比例尺
            const xScale = d3.scaleLinear()
                .domain([0, 100])
                .range([30, width - 30]);

            const yScale = d3.scaleLinear()
                .domain([0, 100])
                .range([height - 30, 30]);

            // 颜色比例尺
            const colorScale = d3.scaleOrdinal()
                .domain([1, 2, 3, 4])
                .range(['#ff6666', '#66ff66', '#6666ff', '#ffff66']);

            // 添加坐标轴
            this.svg.append('g')
                .attr('transform', `translate(0,${height - 30})`)
                .call(d3.axisBottom(xScale));

            this.svg.append('g')
                .attr('transform', 'translate(30,0)')
                .call(d3.axisLeft(yScale));

            // 添加PCA数据点
            this.pPoints = this.svg.selectAll('.pca-point')
                .data(pcaData)
                .enter()
                .append('circle')
                .attr('class', 'pca-point')
                .attr('cx', d => xScale(d.x))
                .attr('cy', d => yScale(d.y))
                .attr('r', 7)
                .attr('fill', d => colorScale(d.group))
                .attr('opacity', 1);

            // 添加t-SNE数据点（初始设为透明）
            this.tPoints = this.svg.selectAll('.tsne-point')
                .data(tsneData)
                .enter()
                .append('circle')
                .attr('class', 'tsne-point')
                .attr('cx', d => xScale(d.x))
                .attr('cy', d => yScale(d.y))
                .attr('r', 7)
                .attr('fill', d => colorScale(d.group))
                .attr('opacity', 0);

            // 添加图例
            const legend = this.svg.append('g')
                .attr('transform', `translate(${width - 100}, 10)`);

            legend.append('text')
                .attr('x', 0)
                .attr('y', 10)
                .text('数据组:')
                .style('font-size', '12px');

            [1, 2, 3, 4].forEach((group, i) => {
                legend.append('circle')
                    .attr('cx', 10)
                    .attr('cy', 30 + i * 20)
                    .attr('r', 5)
                    .attr('fill', colorScale(group));

                legend.append('text')
                    .attr('x', 20)
                    .attr('y', 35 + i * 20)
                    .text(`组 ${group}`)
                    .style('font-size', '12px');
            });
        },
        updateVisualization() {
            const pcaOpacity = 1 - (this.visualizationBlendValue / 100);
            const tsneOpacity = this.visualizationBlendValue / 100;

            // 更新点的透明度
            this.pPoints.attr('opacity', pcaOpacity);
            this.tPoints.attr('opacity', tsneOpacity);
        },
        formatTooltip(val) {
            if (val === 0) return 'PCA 100%';
            if (val === 100) return 't-SNE 100%';
            return `PCA ${100 - val}% | t-SNE ${val}%`;
        },
        checkAnswer() {
            this.isCorrect = this.userAnswer === 'clusters';
            this.showResponse = true;
        },
        resetAnswer() {
            this.showResponse = false;
            this.userAnswer = '';
        },
        proceedToNext() {
            this.$emit('lesson-completed', true);
            this.$emit('user-response', this.userAnswer);
        }
    }
};
</script>

<style scoped>
.lesson-container {
    margin-bottom: 30px;
}

.content-section,
.interactive-section,
.response-section {
    margin-bottom: 20px;
}

.markdown-content {
    line-height: 1.6;
}

.markdown-content>>>img {
    max-width: 100%;
    display: block;
    margin: 20px auto;
}

.visualization-container {
    width: 100%;
    padding: 10px;
    margin: 20px 0;
}

.d3-visualization {
    border: 1px solid #eaeaea;
    background-color: #f9f9f9;
    margin-bottom: 15px;
}

.question-section {
    margin-top: 20px;
}

.action-buttons {
    margin-top: 20px;
}

.correct-answer {
    background-color: #f0f9eb;
}

.wrong-answer {
    background-color: #fef0f0;
}
</style>
