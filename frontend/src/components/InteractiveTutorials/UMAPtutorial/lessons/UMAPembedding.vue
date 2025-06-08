<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>6. UMAP的低维嵌入</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 低维嵌入过程可视化 -->
            <div class="interaction-container">
                <h3>互动演示：低维嵌入优化过程</h3>
                <p>下面的动画展示了UMAP如何逐步优化低维嵌入来保留数据的拓扑结构。</p>

                <div class="controls">
                    <div class="control-panel">
                        <el-button-group>
                            <el-button :type="animationState === 'playing' ? 'primary' : 'default'"
                                @click="playAnimation" icon="el-icon-video-play">
                                播放
                            </el-button>
                            <el-button :type="animationState === 'paused' ? 'info' : 'default'" @click="pauseAnimation"
                                icon="el-icon-video-pause">
                                暂停
                            </el-button>
                            <el-button @click="resetAnimation" icon="el-icon-refresh-right">
                                重置
                            </el-button>
                        </el-button-group>
                    </div>

                    <div class="progress-container">
                        <span>迭代进度: {{ currentIteration }} / {{ totalIterations }}</span>
                        <el-slider v-model="currentIteration" :min="0" :max="totalIterations" :step="1"
                            @change="setIteration">
                        </el-slider>
                    </div>

                    <div class="parameters">
                        <div class="parameter-item">
                            <span>最小距离 (min_dist):</span>
                            <el-slider v-model="minDist" :min="0" :max="2" :step="0.1"
                                @change="updateParameters"></el-slider>
                        </div>
                        <div class="parameter-item">
                            <span>学习率 (learning_rate):</span>
                            <el-slider v-model="learningRate" :min="1" :max="100" :step="1"
                                @change="updateParameters"></el-slider>
                        </div>
                    </div>
                </div>

                <div class="visualization-container">
                    <!-- <div class="visualization-panel">
                        <h4>原始高维空间关系</h4>
                        <div class="visualization" ref="graphVisualization"></div>
                    </div> -->

                    <div class="visualization-panel">
                        <h4>低维嵌入 (2D投影)</h4>
                        <div class="visualization" ref="embeddingVisualization"></div>
                    </div>
                </div>

                <div class="explanation-panel">
                    <h4>低维嵌入优化说明</h4>
                    <p>
                        UMAP通过最小化一个目标函数来优化低维嵌入。这个目标函数平衡了两个目标：
                    </p>
                    <ol>
                        <li>
                            <strong>吸引力</strong>：在高维空间中相似的点在低维空间中应该靠近。
                            连接强度越高，吸引力越大。
                        </li>
                        <li>
                            <strong>排斥力</strong>：在高维空间中不相似的点在低维空间中应该分开。
                            不相连的点之间存在小的排斥力。
                        </li>
                    </ol>
                    <p>
                        观察上面的动画，您可以看到：
                    </p>
                    <ul>
                        <li>刚开始时，点分布较为混乱</li>
                        <li>随着迭代进行，相似的点（相同颜色）逐渐聚集</li>
                        <li>到后期，不同簇的点明显分开，形成清晰的簇结构</li>
                    </ul>
                    <p>
                        <strong>参数影响</strong>：
                    </p>
                    <ul>
                        <li><strong>min_dist</strong>：控制嵌入中点的紧密程度。较小的值使点聚集更紧密，较大的值使点分布更均匀。</li>
                        <li><strong>learning_rate</strong>：控制每次迭代中点移动的幅度。较大的学习率可以加速收敛，但可能导致不稳定。</li>
                    </ul>
                </div>

                <!-- 交互测验 -->
                <div class="quiz-container" v-if="!quizCompleted">
                    <h4>交互测验</h4>
                    <p>通过调整参数并观察动画，解决下面的问题：</p>

                    <div class="challenge">
                        <p><strong>挑战</strong>：调整<strong>min_dist</strong>参数，尝试找到能够使簇内点足够靠近但仍保持簇间清晰分离的值。</p>

                        <el-radio-group v-model="userAnswer">
                            <el-radio :label="1">我认为较大的min_dist值(>1.0)更好，因为它使簇分布更均匀</el-radio>
                            <el-radio :label="2">我认为中等的min_dist值(0.3-0.8)最好，能平衡簇内聚集和簇间分离</el-radio>
                            <el-radio :label="3">我认为较小的min_dist值( &lt; 0.1)更好，因为它使簇更紧凑 </el-radio>
                        </el-radio-group>

                        <el-button type="primary" @click="checkAnswer" :disabled="!userAnswer" class="submit-btn">
                            提交答案
                        </el-button>
                    </div>
                </div>

                <!-- 回应部分 -->
                <div v-if="quizCompleted" class="response-container">
                    <el-alert :title="feedbackTitle" :type="isCorrect ? 'success' : 'warning'"
                        :description="feedbackDescription" show-icon>
                    </el-alert>

                    <div v-if="isCorrect || retries >= 2" class="next-section">
                        <p>🎉 您已完成UMAP低维嵌入部分！可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>

                    <div v-else class="retry-section">
                        <el-button type="info" @click="resetAnswer">
                            重新尝试
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
    name: 'Section6Embedding',
    data() {
        return {
            markdownContent: `
  ## UMAP的低维嵌入优化
  
  在构建了表示数据拓扑结构的图后，UMAP的下一步是找到数据在低维空间中的表示（通常是2D或3D），使得这种表示尽可能地保留原始高维空间的拓扑结构。这个过程称为**低维嵌入优化**。
  
  ### 优化目标
  
  UMAP的低维嵌入优化基于一个目标函数，它试图使低维空间中的图结构尽可能接近高维空间中的图结构。形式上，这个目标函数是一个交叉熵损失：
  
  $\\sum_{(i, j) \\in E} w_{ij} \\log\\left(\\frac{w_{ij}}{w'_{ij}}\\right) + (1-w_{ij}) \\log\\left(\\frac{1-w_{ij}}{1-w'_{ij}}\\right)$
  
  其中：
  - $w_{ij}$ 是高维空间中点$i$和$j$之间的边权重
  - $w'_{ij}$ 是低维空间中对应点之间的边权重
  - $E$ 是图中所有边的集合
  
  这个目标函数平衡了两个关键目标：
  1. 保持连接点之间的接近性（吸引力）
  2. 保持非连接点之间的分离性（排斥力）
  
  ### 低维空间中的边权重
  
  在低维空间中，点$i$和点$j$之间的边权重计算为：
  
  $w'_{ij} = \\left(1 + a \\cdot d(y_i, y_j)^{2b}\\right)^{-1}$
  
  其中：
  - $d(y_i, y_j)$ 是点在低维空间中的距离
  - $a$ 和 $b$ 是由 \`min_dist\` 参数控制的常数
  - 这个函数是一个平滑的曲线，在距离小于 \`min_dist\` 时接近1，然后随着距离增加而迅速衰减
  
  ### 优化过程
  
  UMAP使用**随机梯度下降（SGD）**来优化低维嵌入。优化过程可以概括为：
  
  1. **初始化**：在低维空间中随机初始化点的位置（或使用PCA等方法获得初始布局）
  2. **迭代优化**：
     - 随机选择一批边
     - 对于每条边，计算基于当前嵌入的梯度
     - 根据梯度更新点的位置
     - 随着迭代进行，逐渐降低学习率
  3. **收敛**：达到最大迭代次数或满足收敛条件时停止
  
  在每次迭代中，梯度计算考虑两种力：
  - **吸引力**：连接的点相互吸引，吸引力与边权重成正比
  - **排斥力**：未连接的点相互排斥，排斥力通常较弱但作用范围更广
  
  ### 关键参数
  
  UMAP低维嵌入优化过程中有几个重要参数：
  
  1. **min_dist**：控制投影中点的紧密程度
     - 较小的值（如0.1）：点聚集更紧密，强调局部结构
     - 较大的值（如0.5-1.0）：点分布更均匀，关注全局布局
  
  2. **n_epochs**：优化迭代的次数
     - 较多的迭代通常会得到更好的结果，但需要更长的计算时间
     - 默认情况下，UMAP会根据数据集大小自动确定适当的迭代次数
  
  3. **learning_rate**：控制每次迭代中点位置更新的步长
     - 较大的学习率可能导致更快收敛，但也可能导致不稳定
     - 较小的学习率更稳定，但可能需要更多迭代才能收敛
  
  在下面的交互演示中，您可以观察UMAP的低维嵌入优化过程，并探索不同参数对结果的影响。
        `,
            animationState: 'paused',
            currentIteration: 0,
            totalIterations: 100,
            minDist: 0.5,
            learningRate: 10,
            pointsHD: [], // 高维空间中的点
            pointsLD: [], // 低维空间中的点 - 每次迭代的快照
            graphLinks: [], // 高维空间中的连接
            animationInterval: null,
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
            return this.isCorrect ? '正确答案！' : '请再考虑一下';
        },
        feedbackDescription() {
            if (this.isCorrect) {
                return '中等的min_dist值确实能够在簇内聚集和簇间分离之间取得良好的平衡。这也是为什么UMAP默认值通常设置在0.1-0.5范围内的原因。';
            }

            switch (this.userAnswer) {
                case 1:
                    return '较大的min_dist值会使所有点分布得更加均匀，可能导致簇内凝聚力不足，使簇结构变得模糊。';
                case 3:
                    return '虽然很小的min_dist值能使簇更紧凑，但可能会导致过度聚集，使不同簇之间的边界模糊，特别是当簇本身很接近时。';
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
            this.isCompleted = completedSections.includes(6);
        }

        // 初始化数据和可视化
        this.initializeData();
        this.initializeVisualizations();
        this.generateEmbeddingSequence();
    },
    methods: {
        initializeData() {
            // 生成三个簇的数据（用于高维空间表示）
            const numClusters = 3;
            const pointsPerCluster = 15;
            this.pointsHD = [];

            const colors = ["#F56C6C", "#409EFF", "#67C23A"];
            const clusterCenters = [
                { x: 100, y: 100 },
                { x: 250, y: 150 },
                { x: 150, y: 250 }
            ];

            // 为每个簇生成点
            for (let c = 0; c < numClusters; c++) {
                const center = clusterCenters[c];

                for (let i = 0; i < pointsPerCluster; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const radius = Math.random() * 40;
                    this.pointsHD.push({
                        id: c * pointsPerCluster + i,
                        x: center.x + Math.cos(angle) * radius,
                        y: center.y + Math.sin(angle) * radius,
                        cluster: c,
                        color: colors[c]
                    });
                }
            }

            // 计算点之间的距离并创建连接
            this.graphLinks = [];

            // 为每个点找到簇内所有其他点的连接
            for (let i = 0; i < this.pointsHD.length; i++) {
                const source = this.pointsHD[i];

                for (let j = i + 1; j < this.pointsHD.length; j++) {
                    const target = this.pointsHD[j];

                    // 计算距离
                    const dx = source.x - target.x;
                    const dy = source.y - target.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    // 添加连接，如果点在同一簇中，连接强度更高
                    if (source.cluster === target.cluster) {
                        this.graphLinks.push({
                            source: source.id,
                            target: target.id,
                            weight: 1.0 / (1.0 + distance / 50),
                            isSameCluster: true
                        });
                    } else {
                        // 不同簇之间也可能有弱连接
                        const weakLinkProb = Math.exp(-distance / 100);
                        if (Math.random() < weakLinkProb * 0.1) {
                            this.graphLinks.push({
                                source: source.id,
                                target: target.id,
                                weight: 0.1 * weakLinkProb,
                                isSameCluster: false
                            });
                        }
                    }
                }
            }
        },

        initializeVisualizations() {
            // 初始化高维空间图可视化
            this.initGraphVisualization();

            // 初始化低维嵌入可视化（初始态）
            this.initEmbeddingVisualization();
        },

        initGraphVisualization() {
            // const width = this.$refs.graphVisualization.clientWidth;
            // const height = 300;

            // // 清除现有SVG
            // d3.select(this.$refs.graphVisualization).selectAll("*").remove();

            // const svg = d3.select(this.$refs.graphVisualization)
            //     .append("svg")
            //     .attr("width", width)
            //     .attr("height", height);

            // // 创建力导向模拟
            // const simulation = d3.forceSimulation(this.pointsHD)
            //     .force("link", d3.forceLink(this.graphLinks)
            //         .id(d => d.id)
            //         .distance(d => 30 + (1 - d.weight) * 100)
            //         .strength(d => d.weight))
            //     .force("charge", d3.forceManyBody().strength(-30))
            //     .force("center", d3.forceCenter(width / 2, height / 2))
            //     .force("x", d3.forceX(d => d.x).strength(0.1))
            //     .force("y", d3.forceY(d => d.y).strength(0.1))
            //     .force("collide", d3.forceCollide(8));

            // // 绘制连接线
            // const link = svg.append("g")
            //     .selectAll("line")
            //     .data(this.graphLinks)
            //     .enter().append("line")
            //     .attr("stroke", d => d.isSameCluster ? "#999" : "#ddd")
            //     .attr("stroke-opacity", d => d.isSameCluster ? 0.6 : 0.3)
            //     .attr("stroke-width", d => d.weight * 3);

            // // 绘制节点
            // const node = svg.append("g")
            //     .selectAll("circle")
            //     .data(this.pointsHD)
            //     .enter().append("circle")
            //     .attr("r", 6)
            //     .attr("fill", d => d.color)
            //     .attr("stroke", "#fff")
            //     .attr("stroke-width", 1.5);

            // // 添加图例
            // const legend = svg.append("g")
            //     .attr("transform", "translate(10, 10)");

            // legend.append("text")
            //     .attr("x", 0)
            //     .attr("y", 15)
            //     .attr("font-size", "12px")
            //     .attr("font-weight", "bold")
            //     .text("高维空间关系图");

            // // 更新力导向模拟
            // simulation.on("tick", () => {
            //     link
            //         .attr("x1", d => d.source.x)
            //         .attr("y1", d => d.source.y)
            //         .attr("x2", d => d.target.x)
            //         .attr("y2", d => d.target.y);

            //     node
            //         .attr("cx", d => d.x)
            //         .attr("cy", d => d.y);
            // });

            // // 将模拟暂停在一个相对稳定的状态
            // for (let i = 0; i < 300; i++) simulation.tick();
            // simulation.stop();
        },

        initEmbeddingVisualization() {
            const width = this.$refs.embeddingVisualization.clientWidth;
            const height = 300;

            // 清除现有SVG
            d3.select(this.$refs.embeddingVisualization).selectAll("*").remove();

            const svg = d3.select(this.$refs.embeddingVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 添加坐标轴
            svg.append("line")
                .attr("x1", 20)
                .attr("y1", height / 2)
                .attr("x2", width - 20)
                .attr("y2", height / 2)
                .attr("stroke", "#ddd")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "3,3");

            svg.append("line")
                .attr("x1", width / 2)
                .attr("y1", 20)
                .attr("x2", width / 2)
                .attr("y2", height - 20)
                .attr("stroke", "#ddd")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "3,3");

            // 添加图例
            const legend = svg.append("g")
                .attr("transform", "translate(10, 10)");

            legend.append("text")
                .attr("x", 0)
                .attr("y", 15)
                .attr("font-size", "12px")
                .attr("font-weight", "bold")
                .text("2D嵌入空间");

            svg.append("text")
                .attr("class", "iteration-label")
                .attr("x", width / 2)
                .attr("y", height - 10)
                .attr("text-anchor", "middle")
                .attr("font-size", "12px")
                .text(`迭代: ${this.currentIteration} / ${this.totalIterations}`);
        },

        generateEmbeddingSequence() {
            // 生成低维嵌入的迭代序列
            this.pointsLD = [];

            // 初始状态 - 随机分布在中心附近
            const initialPoints = this.pointsHD.map(p => ({
                id: p.id,
                x: Math.random() * 100 - 50,  // 中心附近随机位置
                y: Math.random() * 100 - 50,
                cluster: p.cluster,
                color: p.color
            }));

            this.pointsLD.push([...initialPoints]);

            // 定义簇的目标中心
            const targetCenters = [
                { x: -80, y: 0 },    // 簇0目标中心
                { x: 80, y: 0 },     // 簇1目标中心
                { x: 0, y: -80 }      // 簇2目标中心
            ];

            // 生成每次迭代的点位置
            for (let iter = 1; iter <= this.totalIterations; iter++) {
                const prevPoints = this.pointsLD[iter - 1];
                const newPoints = [];

                // 每个点的新位置
                for (let i = 0; i < prevPoints.length; i++) {
                    const point = prevPoints[i];
                    const target = targetCenters[point.cluster];

                    // 计算到目标中心的距离
                    const dx = target.x - point.x;
                    const dy = target.y - point.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    // 添加移动与随机抖动
                    // 移动速度随着迭代减慢
                    const speed = this.learningRate / 10 * (1 - iter / this.totalIterations);
                    const moveX = dist > 0 ? (dx / dist) * speed : 0;
                    const moveY = dist > 0 ? (dy / dist) * speed : 0;

                    // 随机抖动，模拟优化中的随机性
                    const jitter = 5 * (1 - iter / this.totalIterations);
                    const noiseX = (Math.random() - 0.5) * jitter;
                    const noiseY = (Math.random() - 0.5) * jitter;

                    // 应用min_dist参数 - 影响簇的紧密程度
                    const clusterRadius = 30 + 20 * this.minDist;
                    const clusterFactor = Math.min(1, dist / clusterRadius);

                    // 计算新位置
                    newPoints.push({
                        id: point.id,
                        x: point.x + moveX * clusterFactor + noiseX,
                        y: point.y + moveY * clusterFactor + noiseY,
                        cluster: point.cluster,
                        color: point.color
                    });
                }

                this.pointsLD.push(newPoints);
            }

            // 初始状态显示
            this.updateEmbeddingVisualization(this.pointsLD[0]);
        },

        updateEmbeddingVisualization(points) {
            const width = this.$refs.embeddingVisualization.clientWidth;
            const height = 300;
            const svg = d3.select(this.$refs.embeddingVisualization).select("svg");

            // 更新迭代标签
            svg.select(".iteration-label")
                .text(`迭代: ${this.currentIteration} / ${this.totalIterations}`);

            // 缩放数据到可视区域
            const xExtent = d3.extent(points, d => d.x);
            const yExtent = d3.extent(points, d => d.y);

            const xRange = Math.max(1, xExtent[1] - xExtent[0]);
            const yRange = Math.max(1, yExtent[1] - yExtent[0]);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - xRange * 0.1, xExtent[1] + xRange * 0.1])
                .range([50, width - 50]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - yRange * 0.1, yExtent[1] + yRange * 0.1])
                .range([height - 50, 50]);

            // 更新或创建点
            const circles = svg.selectAll("circle").data(points, d => d.id);

            circles.enter()
                .append("circle")
                .attr("r", 6)
                .attr("fill", d => d.color)
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5)
                .merge(circles)
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y));

            circles.exit().remove();
        },

        playAnimation() {
            if (this.animationState === 'playing') return;

            this.animationState = 'playing';
            this.animationInterval = setInterval(() => {
                if (this.currentIteration < this.totalIterations) {
                    this.currentIteration++;
                    this.updateEmbeddingVisualization(this.pointsLD[this.currentIteration]);
                } else {
                    this.pauseAnimation();
                }
            }, 100);
        },

        pauseAnimation() {
            if (this.animationState === 'paused') return;

            this.animationState = 'paused';
            if (this.animationInterval) {
                clearInterval(this.animationInterval);
                this.animationInterval = null;
            }
        },

        resetAnimation() {
            this.pauseAnimation();
            this.currentIteration = 0;
            this.updateEmbeddingVisualization(this.pointsLD[0]);
        },

        setIteration(value) {
            this.pauseAnimation();
            this.currentIteration = value;
            this.updateEmbeddingVisualization(this.pointsLD[value]);
        },

        updateParameters() {
            this.pauseAnimation();
            this.generateEmbeddingSequence();
            this.resetAnimation();
        },

        checkAnswer() {
            this.quizCompleted = true;
            this.isCorrect = this.userAnswer === 2; // 选项2是正确答案

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
        // 清除任何运行中的动画
        if (this.animationInterval) {
            clearInterval(this.animationInterval);
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
    margin-bottom: 20px;
}

.control-panel {
    margin-bottom: 15px;
    display: flex;
    justify-content: center;
}

.progress-container {
    margin: 15px 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.parameters {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px dashed #dcdfe6;
}

.parameter-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.parameter-item span {
    width: 170px;
    margin-right: 15px;
}

.visualization-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 20px 0;
}

.visualization-panel {
    flex: 1;
    min-width: 300px;
}

.visualization-panel h4 {
    text-align: center;
    margin-bottom: 10px;
}

.visualization {
    width: 100%;
    height: 300px;
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

.challenge {
    margin-top: 15px;
}

.challenge .el-radio-group {
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

:deep(ol),
:deep(ul) {
    padding-left: 20px;
    line-height: 1.6;
}
</style>