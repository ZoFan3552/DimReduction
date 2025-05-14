<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>5. UMAP的图构建</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 图构建可视化 -->
            <div class="interaction-container">
                <h3>互动演示：图构建过程</h3>
                <p>通过下面的交互式演示，观察UMAP如何构建图表示数据的局部拓扑结构。</p>

                <div class="controls">
                    <div class="control-item">
                        <span>邻居数量 (n_neighbors):</span>
                        <el-slider v-model="nNeighbors" :min="3" :max="15" :step="1"
                            @change="updateVisualization"></el-slider>
                    </div>
                    <div class="control-item">
                        <span>局部联通性强度 (σ):</span>
                        <el-slider v-model="sigmaFactor" :min="1" :max="10" :step="1"
                            @change="updateVisualization"></el-slider>
                    </div>
                    <div class="control-item">
                        <span>图模式:</span>
                        <el-radio-group v-model="graphMode" @change="updateVisualization">
                            <el-radio label="knn">K近邻图</el-radio>
                            <el-radio label="fuzzy">模糊图</el-radio>
                        </el-radio-group>
                    </div>
                </div>

                <div class="visualization" ref="graphVisualization"></div>

                <div class="explanation-panel">
                    <h4>图构建参数说明</h4>
                    <p>
                        <strong>邻居数量 (n_neighbors):</strong>
                        确定每个点连接的近邻数量。较小的值使图更稀疏，关注局部结构；较大的值使图更密集，捕捉更多全局关系。
                    </p>
                    <p>
                        <strong>局部联通性强度 (σ):</strong>
                        控制模糊图中的连接强度衰减速率。较大的值使连接强度随距离的增加衰减更慢，导致更多点之间有显著的连接。
                    </p>
                    <p>
                        <strong>图模式:</strong>
                        "K近邻图"显示简单的二元连接，每个点连接到其K个最近邻。
                        "模糊图"显示带权重的连接，其中权重（线条粗细）表示连接强度。
                    </p>
                    <p>
                        通过调整这些参数，观察它们如何影响图的结构。这个图是UMAP算法的基础，将直接决定最终降维结果的质量。
                    </p>
                </div>

                <!-- 交互式问题 -->
                <div class="quiz-container" v-if="!quizCompleted">
                    <h4>交互式问题</h4>
                    <p>根据您调整参数的观察，回答以下问题：</p>

                    <div class="question">
                        <p><strong>问题：</strong> 当将邻居数量 (n_neighbors) 从小值增加到大值时，图的结构如何变化？</p>
                        <el-radio-group v-model="userAnswer">
                            <el-radio :label="1">图变得更稀疏，只保留非常强的局部连接</el-radio>
                            <el-radio :label="2">图基本没有变化，因为n_neighbors只影响优化速度</el-radio>
                            <el-radio :label="3">图变得更密集，捕捉更多全局结构信息</el-radio>
                            <el-radio :label="4">图中的连接数量减少，但每个连接的强度增加</el-radio>
                        </el-radio-group>

                        <el-button type="primary" @click="checkAnswer" :disabled="!userAnswer" class="submit-btn">
                            提交答案
                        </el-button>
                    </div>
                </div>

                <!-- 回应部分 -->
                <div v-if="quizCompleted" class="response-container">
                    <el-alert :title="feedbackTitle" :type="isCorrect ? 'success' : 'error'"
                        :description="feedbackDescription" show-icon>
                    </el-alert>

                    <div v-if="isCorrect || retries >= 2" class="next-section">
                        <p>🎉 您已完成UMAP图构建部分！可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>

                    <div v-else class="retry-section">
                        <el-button type="info" @click="resetAnswer">
                            重新回答
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
    name: 'Section5Graph',
    data() {
        return {
            markdownContent: `
  ## UMAP中的图构建
  
  在UMAP算法中，图构建是一个核心步骤，它将原始数据转换为一个表示其拓扑结构的加权图。这个图捕捉了数据点之间的局部和全局关系，为后续的低维嵌入提供了基础。
  
  ### 为什么需要构建图？
  
  UMAP基于数据点在**流形**上的关系来进行降维。但我们无法直接获取这个流形，因此需要从数据点的局部关系来近似推断流形结构。图是表示这种关系的自然方式：
  - 图中的**节点**表示数据点
  - 图中的**边**表示点之间的关系或相似度
  - 边的**权重**表示关系强度
  
  ### 图构建的步骤
  
  UMAP构建图的过程可以分为以下步骤：
  
  #### 1. 计算局部度量
  
  对于每个数据点 $x$，UMAP：
  - 找到它的 $k$ 个最近邻居（其中 $k$ 是参数 \`n_neighbors\`）
  - 计算到第 $k$ 个近邻的距离，记为 $\rho_x$
  - 寻找一个参数 $\\sigma_x$，使得：
  
  $\\sum_{i=1}^{k} \\exp\\left(-\\frac{d(x, y_i) - \\rho_x}{\\sigma_x}\\right) = \\log_2(k)$
  
  这个 $\\sigma_x$ 参数定义了点 $x$ 的**局部度量缩放**，它使得局部连接性在不同密度区域保持一致。
  
  #### 2. 计算高维点之间的相似度
  
  使用上一步中确定的局部度量，UMAP计算点 $x$ 和 $y$ 之间的相似度：
  
  $v_{x|y} = \\exp\\left(-\\frac{\\max(0, d(x,y) - \\rho_x)}{\\sigma_x}\\right)$
  
  注意这个相似度是**非对称的**——从 $x$ 看 $y$ 和从 $y$ 看 $x$ 可能不同，因为它们的局部度量参数 $\\sigma$ 和 $\\rho$ 可能不同。
  
  #### 3. 构建对称的模糊图
  
  为了得到一个对称的相似度度量，UMAP使用一种模糊逻辑组合方式：
  
  $v_{xy} = v_{x|y} + v_{y|x} - v_{x|y} \\cdot v_{y|x}$
  
  这个公式相当于取两个单向相似度的**概率和**（概率论中的"或"操作）。
  
  ### 关键参数
  
  图构建过程中有两个关键参数：
  
  1. **n_neighbors**：决定每个点连接的近邻数量，影响局部与全局结构的平衡：
     - 较小的值（如5-15）：关注非常局部的结构，可能会错过全局模式
     - 较大的值（如30-100）：保留更多全局结构，但可能会模糊局部细节
  
  2. **local_connectivity**：控制最近邻的连接强度，通常默认为1，表示与第一个近邻完全连接。
  
  ### 图构建的特性
  
  UMAP的图构建有以下重要特性：
  
  - **适应不同密度**：通过为每个点确定局部度量，UMAP可以处理不同密度区域的数据
  - **保留局部结构**：近邻点之间有较强的连接
  - **捕捉全局关系**：通过点之间的路径连接，保留整体拓扑结构
  - **模糊表示**：使用连续权重而非二元关系，更准确地表示点之间的相似程度
  
  在下面的互动演示中，您可以调整参数，观察它们如何影响图的构建过程。
        `,
            nNeighbors: 5,
            sigmaFactor: 5,
            graphMode: 'knn',
            points: [],
            simulation: null,
            userAnswer: null,
            quizCompleted: false,
            isCorrect: false,
            retries: 0,
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
        },
        feedbackTitle() {
            return this.isCorrect ? '回答正确！' : '回答不正确';
        },
        feedbackDescription() {
            if (this.isCorrect) {
                return '增加邻居数量确实会使图变得更密集，捕捉更多的全局结构信息。这也是为什么更大的n_neighbors值通常会导致UMAP结果保留更多全局结构的原因。';
            }

            switch (this.userAnswer) {
                case 1:
                    return '与描述相反，增加邻居数量会使图变得更密集，而不是更稀疏。更多的近邻连接意味着更多的边。';
                case 2:
                    return 'n_neighbors参数直接影响图的结构，而不仅仅是优化速度。它决定了每个点连接到多少个其他点。';
                case 4:
                    return '增加n_neighbors会导致连接数量增加，而不是减少。每个点会连接到更多的邻居。';
                default:
                    return '请选择一个选项。';
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(5);
        }

        // 初始化可视化
        this.initializeData();
        this.initializeVisualization();
    },
    methods: {
        initializeData() {
            // 生成示例数据
            this.points = [];

            // 生成两个簇的2D数据
            const generateClusterPoints = (centerX, centerY, count, radius, startIndex) => {
                const clusterPoints = [];
                for (let i = 0; i < count; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const r = Math.random() * radius;
                    const x = centerX + Math.cos(angle) * r;
                    const y = centerY + Math.sin(angle) * r;

                    clusterPoints.push({
                        id: startIndex + i,
                        x: x,
                        y: y,
                        cluster: startIndex === 0 ? 0 : 1
                    });
                }
                return clusterPoints;
            };

            // 生成第一个簇
            const cluster1 = generateClusterPoints(100, 150, 20, 50, 0);

            // 生成第二个簇
            const cluster2 = generateClusterPoints(250, 150, 20, 50, 20);

            this.points = [...cluster1, ...cluster2];

            // 计算点之间的距离矩阵
            this.points.forEach(point => {
                point.distances = {};
                this.points.forEach(other => {
                    if (point !== other) {
                        const dx = point.x - other.x;
                        const dy = point.y - other.y;
                        point.distances[other.id] = Math.sqrt(dx * dx + dy * dy);
                    }
                });
            });
        },

        initializeVisualization() {
            // 创建可视化
            this.updateVisualization();
        },

        updateVisualization() {
            // 更新图可视化
            const width = this.$refs.graphVisualization.clientWidth;
            const height = 400;

            // 清除现有SVG
            d3.select(this.$refs.graphVisualization).selectAll("*").remove();

            const svg = d3.select(this.$refs.graphVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 为每个点找到k个最近邻
            this.points.forEach(point => {
                const neighbors = Object.entries(point.distances)
                    .map(([id, distance]) => ({ id: parseInt(id), distance }))
                    .sort((a, b) => a.distance - b.distance)
                    .slice(0, this.nNeighbors);

                point.neighbors = neighbors;

                // 计算到第k个近邻的距离
                point.rho = neighbors[neighbors.length - 1].distance;

                // 设置局部度量参数，使用sigmaFactor作为缩放
                point.sigma = point.rho * (this.sigmaFactor / 5);
            });

            // 构建边
            const links = [];

            if (this.graphMode === 'knn') {
                // K近邻图 - 简单的二元连接
                this.points.forEach(point => {
                    point.neighbors.forEach(neighbor => {
                        // 确保每条边只添加一次
                        if (point.id < neighbor.id) {
                            links.push({
                                source: point,
                                target: this.points.find(p => p.id === neighbor.id),
                                weight: 1
                            });
                        }
                    });
                });
            } else {
                // 模糊图 - 带权重的连接
                this.points.forEach(point => {
                    this.points.forEach(other => {
                        if (point.id < other.id) {
                            const dist = point.distances[other.id];

                            // 计算定向相似度
                            const vPointToOther = Math.exp(-Math.max(0, dist - point.rho) / point.sigma);
                            const vOtherToPoint = Math.exp(-Math.max(0, dist - other.rho) / other.sigma);

                            // 计算对称相似度
                            const weight = vPointToOther + vOtherToPoint - vPointToOther * vOtherToPoint;

                            // 只添加权重显著的边
                            if (weight > 0.1) {
                                links.push({
                                    source: point,
                                    target: other,
                                    weight: weight
                                });
                            }
                        }
                    });
                });
            }

            // 创建力导向布局
            this.simulation = d3.forceSimulation(this.points)
                .force("link", d3.forceLink(links).id(d => d.id))
                .force("charge", d3.forceManyBody().strength(-30))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("x", d3.forceX(d => d.x).strength(0.1))
                .force("y", d3.forceY(d => d.y).strength(0.1))
                .force("collide", d3.forceCollide(8));

            // 绘制连接线
            const link = svg.append("g")
                .selectAll("line")
                .data(links)
                .enter().append("line")
                .attr("stroke", "#999")
                .attr("stroke-opacity", 0.6)
                .attr("stroke-width", d => this.graphMode === 'fuzzy' ? d.weight * 3 : 1);

            // 绘制节点
            const node = svg.append("g")
                .selectAll("circle")
                .data(this.points)
                .enter().append("circle")
                .attr("r", 6)
                .attr("fill", d => d.cluster === 0 ? "#F56C6C" : "#67C23A")
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5)
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            // 添加悬停提示
            node.append("title")
                .text(d => `ID: ${d.id}\n簇: ${d.cluster === 0 ? "红色" : "绿色"}`);

            // 添加图例
            const legend = svg.append("g")
                .attr("class", "legend")
                .attr("transform", `translate(20, 20)`);

            legend.append("circle")
                .attr("r", 6)
                .attr("cx", 10)
                .attr("cy", 10)
                .attr("fill", "#F56C6C");

            legend.append("text")
                .attr("x", 25)
                .attr("y", 15)
                .text("簇 1");

            legend.append("circle")
                .attr("r", 6)
                .attr("cx", 10)
                .attr("cy", 35)
                .attr("fill", "#67C23A");

            legend.append("text")
                .attr("x", 25)
                .attr("y", 40)
                .text("簇 2");

            if (this.graphMode === 'fuzzy') {
                // 添加边权重图例
                const weightLegend = svg.append("g")
                    .attr("transform", `translate(${width - 150}, 20)`);

                weightLegend.append("text")
                    .attr("x", 0)
                    .attr("y", 15)
                    .text("边权重");

                weightLegend.append("line")
                    .attr("x1", 10)
                    .attr("y1", 35)
                    .attr("x2", 50)
                    .attr("y2", 35)
                    .attr("stroke", "#999")
                    .attr("stroke-width", 1);

                weightLegend.append("text")
                    .attr("x", 60)
                    .attr("y", 40)
                    .text("弱连接");

                weightLegend.append("line")
                    .attr("x1", 10)
                    .attr("y1", 65)
                    .attr("x2", 50)
                    .attr("y2", 65)
                    .attr("stroke", "#999")
                    .attr("stroke-width", 3);

                weightLegend.append("text")
                    .attr("x", 60)
                    .attr("y", 70)
                    .text("强连接");
            }

            this.simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            });

            function dragstarted(event, d) {
                if (!event.active) this.simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }

            function dragended(event, d) {
                if (!event.active) this.simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
        },

        checkAnswer() {
            this.quizCompleted = true;
            this.isCorrect = this.userAnswer === 3; // 选项3是正确答案

            if (this.isCorrect || ++this.retries >= 2) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },

        resetAnswer() {
            this.quizCompleted = false;
            this.userAnswer = null;
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    },
    beforeDestroy() {
        // 停止力导向模拟
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
    background-color: white;
}

.explanation-panel {
    margin: 20px 0;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.quiz-container {
    margin-top: 30px;
    padding: 15px;
    border-top: 1px dashed #dcdfe6;
}

.question {
    margin-top: 15px;
}

.question .el-radio-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 15px 0;
    margin-left: 20px;
}

.submit-btn {
    margin-top: 15px;
}

.response-container {
    margin-top: 20px;
}

.retry-section {
    margin-top: 15px;
    text-align: center;
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

:deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

:deep(th),
:deep(td) {
    border: 1px solid #dcdfe6;
    padding: 8px 12px;
    text-align: left;
}

:deep(th) {
    background-color: #f5f7fa;
}
</style>