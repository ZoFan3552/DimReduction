<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>2. UMAP直观理解</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - D3.js可视化 -->
            <div class="interaction-container">
                <h3>互动演示：流形投影</h3>
                <p>试着拖动滑块来调整流形变换的参数，观察高维数据如何被投影到2D平面。</p>

                <div class="controls">
                    <div class="control-item">
                        <span>邻居数量 (n_neighbors):</span>
                        <el-slider v-model="nNeighbors" :min="5" :max="50" :step="5"
                            @change="updateVisualization"></el-slider>
                    </div>
                    <div class="control-item">
                        <span>最小距离 (min_dist):</span>
                        <el-slider v-model="minDist" :min="0" :max="0.9" :step="0.1"
                            @change="updateVisualization"></el-slider>
                    </div>
                </div>

                <div class="visualization" ref="visualization"></div>

                <div class="explanation-panel">
                    <el-collapse v-model="activeExplanation">
                        <el-collapse-item title="当前参数的影响" name="1">
                            <div v-html="currentParameterExplanation"></div>
                        </el-collapse-item>
                    </el-collapse>
                </div>

                <div class="challenge-container" v-if="!challengeCompleted">
                    <h3>挑战</h3>
                    <p>请调整参数，尝试找出可以最清晰地分离出3个聚类的参数组合。</p>
                    <el-button type="primary" @click="checkChallenge">我已找到最佳参数</el-button>
                </div>

                <!-- 回应挑战部分 -->
                <div v-if="challengeCompleted" class="response-container">
                    <el-alert :title="challengeFeedbackTitle" type="success" :description="challengeFeedbackDescription"
                        show-icon>
                    </el-alert>

                    <div class="next-section">
                        <p>🎉 恭喜完成UMAP直观理解部分！您可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { marked } from 'marked';
import * as d3 from 'd3';

// 设置渲染器以支持数学公式
import 'katex/dist/katex.min.css';
// import katex from 'katex';
import katex from 'katex';
// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}


export default {
    name: 'Section2Intuition',
    data() {
        return {
            markdownContent: `
  ## UMAP的直观理解
  
  UMAP (Uniform Manifold Approximation and Projection) 是一种强大的降维算法，但它的数学原理可能较为复杂。在深入数学细节之前，让我们先通过一些直观的概念和类比来理解UMAP的工作原理。
  
  ### 核心思想：保留数据的拓扑结构
  
  UMAP的核心思想是在降低数据维度的同时，尽可能保留数据的**拓扑结构**。拓扑结构指的是数据点之间的相对关系和连接方式，而不关心具体的距离大小。
  
  想象一个简单的例子：如果原始数据中两个点非常接近，那么在降维后的空间中，这两个点也应该保持接近。同样，如果原始数据中两组点之间有明显的分隔，那么降维后也应该保持这种分隔。
  
  ### 流形假设
  
  UMAP基于一个重要假设：高维数据通常位于低维**流形**(manifold)上。流形可以理解为高维空间中的一个弯曲表面或子空间。
  
  例如，一张2D的纸张弯曲成3D空间中的一个形状（如圆柱或复杂折叠），虽然纸张看起来位于3D空间，但它本质上仍是一个2D对象。类似地，许多高维数据集可能本质上是低维的，只是"嵌入"到了高维空间中。
  
  
  ### UMAP的工作流程直观解释
  
  UMAP主要分为两个阶段：
  
  1. **构建高维空间中的图结构**：
     - 对于每个数据点，找到它的最近邻
     - 构建一个加权图，其中权重反映点之间的相似度
     - 这个图捕捉了数据的局部拓扑结构
  
  2. **优化低维布局**：
     - 在低维空间中初始化点的位置（通常是随机的）
     - 通过力导向布局算法优化这些点的位置
     - 优化目标是让低维图尽可能接近高维图的结构
  
  这个过程可以类比为：想象数据点通过弹簧连接在一起，弹簧的强度表示点之间的相似度。当我们将这个系统从高维"压缩"到低维时，弹簧会施加力使得连接紧密的点保持在一起。
  
  ### 关键参数直观理解
  
  UMAP有两个重要参数：
  
  1. **n_neighbors**（邻居数量）：
     - 控制关注局部还是全局结构
     - 较小的值关注非常局部的结构
     - 较大的值捕捉更全局的模式
  
  2. **min_dist**（最小距离）：
     - 控制点在低维空间中的紧密程度
     - 较小的值使得聚类更紧凑
     - 较大的值使得点分布更均匀
  
  在下面的互动演示中，您可以调整这些参数，观察它们如何影响投影结果。
        `,
            nNeighbors: 15,
            minDist: 0.1,
            activeExplanation: ['1'],
            clusterData: null,
            svg: null,
            simulation: null,
            circles: null,
            challengeCompleted: false,
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
        },
        currentParameterExplanation() {
            let explanation = '';

            // 根据n_neighbors参数值提供解释
            if (this.nNeighbors <= 10) {
                explanation += '<p><strong>邻居数量设置较小</strong>: 当前值为' + this.nNeighbors +
                    '，这会导致UMAP更关注非常局部的结构，可能会出现较多的小簇，但可能会丢失一些全局关系。</p>';
            } else if (this.nNeighbors >= 30) {
                explanation += '<p><strong>邻居数量设置较大</strong>: 当前值为' + this.nNeighbors +
                    '，这会导致UMAP更关注全局结构，点之间的关系会更平滑，但可能会错过一些局部细节。</p>';
            } else {
                explanation += '<p><strong>邻居数量设置适中</strong>: 当前值为' + this.nNeighbors +
                    '，这种设置在保留局部结构和全局模式之间取得了良好的平衡。</p>';
            }

            // 根据min_dist参数值提供解释
            if (this.minDist <= 0.1) {
                explanation += '<p><strong>最小距离设置较小</strong>: 当前值为' + this.minDist +
                    '，这会导致投影中的点分布更紧凑，聚类更加明显，但点可能会过度重叠。</p>';
            } else if (this.minDist >= 0.5) {
                explanation += '<p><strong>最小距离设置较大</strong>: 当前值为' + this.minDist +
                    '，这会使投影中的点分布更加均匀，聚类边界变得模糊，但可以更好地观察点之间的相对位置。</p>';
            } else {
                explanation += '<p><strong>最小距离设置适中</strong>: 当前值为' + this.minDist +
                    '，这种设置在聚类紧凑性和点分布均匀性之间取得了良好的平衡。</p>';
            }

            return explanation;
        },
        challengeFeedbackTitle() {
            return '挑战完成！';
        },
        challengeFeedbackDescription() {
            return `您已成功找到了一组能够清晰分离聚类的参数。对于这个数据集，理想的参数通常是n_neighbors=15-20，min_dist=0.1-0.3之间。UMAP参数的选择通常需要根据具体数据集进行调整和探索。`;
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(2);
        }

        // 初始化可视化
        this.initializeData();
        this.initializeVisualization();
    },
    methods: {
        initializeData() {
            // 生成三个高斯分布的聚类数据用于演示
            const numClusters = 3;
            const pointsPerCluster = 50;
            const data = [];

            // 为每个聚类生成点
            for (let i = 0; i < numClusters; i++) {
                // 随机确定聚类中心 (10维空间)
                const center = Array.from({ length: 10 }, () => Math.random() * 10);

                // 为聚类生成点
                for (let j = 0; j < pointsPerCluster; j++) {
                    // 围绕聚类中心生成点 (添加高斯噪声)
                    const point = center.map(c => c + (Math.random() + Math.random() + Math.random() - 1.5));

                    // 添加点到数据集，包括聚类标签
                    data.push({
                        features: point,
                        cluster: i
                    });
                }
            }

            this.clusterData = data;
        },

        initializeVisualization() {
            // 创建SVG元素
            const width = 500;
            const height = 400;
            const margin = { top: 20, right: 20, bottom: 20, left: 20 };

            // 清除任何现有的可视化
            d3.select(this.$refs.visualization).selectAll("*").remove();

            this.svg = d3.select(this.$refs.visualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            // 使用模拟UMAP的方法进行初始可视化
            this.updateVisualization();
        },

        updateVisualization() {
            if (!this.clusterData || !this.svg) return;

            // 清除现有点
            this.svg.selectAll("*").remove();

            // 模拟UMAP的投影结果
            // 注意：这里简化了UMAP算法，只是一个大致的视觉效果模拟
            const projectedData = this.simulateUMAP(this.clusterData, this.nNeighbors, this.minDist);

            // 定义比例尺
            const xExtent = d3.extent(projectedData, d => d.x);
            const yExtent = d3.extent(projectedData, d => d.y);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - 1, xExtent[1] + 1])
                .range([0, 460]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - 1, yExtent[1] + 1])
                .range([360, 0]);

            // 定义颜色比例尺
            const colorScale = d3.scaleOrdinal()
                .domain([0, 1, 2])
                .range(["#1f77b4", "#ff7f0e", "#2ca02c"]);

            // 绘制点
            this.circles = this.svg.selectAll("circle")
                .data(projectedData)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 5)
                .style("fill", d => colorScale(d.cluster))
                .style("opacity", 0.7)
                .style("stroke", "#fff")
                .style("stroke-width", 0.5);

            // 添加力导向模拟更新点位置
            this.simulation = d3.forceSimulation(projectedData)
                .force("x", d3.forceX(d => xScale(d.x)).strength(0.2))
                .force("y", d3.forceY(d => yScale(d.y)).strength(0.2))
                .force("collide", d3.forceCollide().radius(5).strength(0.1))
                .force("charge", d3.forceManyBody().strength(-10))
                .alpha(0.3)
                .alphaDecay(0.02)
                .on("tick", () => {
                    this.circles
                        .attr("cx", d => Math.max(0, Math.min(460, d.x)))
                        .attr("cy", d => Math.max(0, Math.min(360, d.y)));
                });
        },

        simulateUMAP(data, nNeighbors, minDist) {
            // 注意：这是一个简化的模拟，不是真正的UMAP算法
            // 仅用于教学演示目的

            // 根据参数调整投影结果
            const projectedData = [];

            for (const point of data) {
                // 创建2D投影点
                // 聚类标签影响位置，但添加随机偏移
                const cluster = point.cluster;

                // 基础位置基于聚类，间距受min_dist影响
                let baseX = (cluster - 1) * (2 + 5 * (1 - minDist));
                let baseY = cluster * 1.5;

                // 添加随机扰动，扰动大小受n_neighbors的影响
                // 邻居数多意味着更关注全局结构，所以点更分散
                const scatter = 1 + (nNeighbors / 30);
                const noise = () => (Math.random() * 2 - 1) * scatter;

                // 投影坐标
                const x = baseX + noise();
                const y = baseY + noise();

                projectedData.push({
                    x: x,
                    y: y,
                    cluster: cluster
                });
            }

            return projectedData;
        },

        checkChallenge() {
            // 检查当前参数是否能较好地分离聚类
            // 这里简化为：如果n_neighbors在10-25之间且min_dist在0.1-0.3之间，则视为有效参数
            if (this.nNeighbors >= 10 && this.nNeighbors <= 25 &&
                this.minDist >= 0.1 && this.minDist <= 0.3) {
                this.challengeCompleted = true;
                this.isCompleted = true;
                this.$emit('complete');
            } else {
                // 提供反馈，鼓励继续尝试
                this.$message({
                    message: '这组参数可能不是最优的，请继续调整参数尝试找出更好的分离效果。',
                    type: 'warning'
                });
            }
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    },
    beforeDestroy() {
        // 停止可能仍在运行的模拟
        if (this.simulation) {
            this.simulation.stop();
        }
    }
}
</script>

<style scoped>
.el-slider {
    width: 100%;
}

.section-container {
    margin-bottom: 40px;
}

.section-card {
    margin-bottom: 20px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.markdown-content {
    margin-bottom: 30px;
}

.markdown-content img {
    max-width: 100%;
    margin: 20px 0;
    border-radius: 5px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.controls {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 20px;
}

.control-item {
    display: flex;
    align-items: center;
}

.control-item span {
    width: 170px;
    margin-right: 15px;
}

.visualization {
    width: 100%;
    height: 400px;
    margin: 20px 0;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
}

.explanation-panel {
    margin: 20px 0;
}

.challenge-container {
    margin-top: 30px;
    padding: 15px;
    border: 1px dashed #dcdfe6;
    border-radius: 4px;
}

.response-container {
    margin-top: 20px;
}

.next-section {
    margin-top: 20px;
    text-align: center;
}

/* 全局样式适配 */
:deep(h2) {
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    margin-top: 20px;
}

:deep(blockquote) {
    border-left: 4px solid #409EFF;
    padding-left: 15px;
    color: #606266;
    margin: 20px 0;
}

:deep(p) {
    line-height: 1.6;
}

:deep(strong) {
    color: #409EFF;
}
</style>