<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="limitations-interactive">
                <h3>PCA局限性探索</h3>
                <p>通过交互式演示，体验PCA在不同数据情境下的局限性。</p>

                <div class="demo-controls">
                    <h4>选择数据场景</h4>
                    <el-radio-group v-model="selectedScenario" @change="updateScenario">
                        <el-radio :label="'nonlinear'">非线性数据</el-radio>
                        <el-radio :label="'outlier'">存在异常值</el-radio>
                        <el-radio :label="'categorical'">分类特征</el-radio>
                        <el-radio :label="'sparse'">稀疏数据</el-radio>
                    </el-radio-group>

                    <div class="scenario-description">
                        <p v-if="selectedScenario === 'nonlinear'">
                            <strong>非线性数据</strong>：当数据呈现非线性关系时，PCA可能无法有效捕捉数据结构。
                        </p>
                        <p v-else-if="selectedScenario === 'outlier'">
                            <strong>存在异常值</strong>：异常值会对PCA结果产生显著影响，导致主成分方向偏移。
                        </p>
                        <p v-else-if="selectedScenario === 'categorical'">
                            <strong>分类特征</strong>：PCA主要针对连续数值特征设计，对分类数据效果较差。
                        </p>
                        <p v-else-if="selectedScenario === 'sparse'">
                            <strong>稀疏数据</strong>：当数据集很稀疏时，PCA可能表现不佳。
                        </p>
                    </div>
                </div>

                <div class="visualization-container">
                    <div class="visualization-wrapper">
                        <h4>原始数据</h4>
                        <div class="visualization" ref="originalDataVis"></div>
                    </div>

                    <div class="visualization-wrapper">
                        <h4>PCA结果</h4>
                        <div class="visualization" ref="pcaResultVis"></div>
                    </div>

                    <div class="visualization-wrapper">
                        <h4>更适合的方法</h4>
                        <div class="visualization" ref="alternativeVis"></div>
                    </div>
                </div>

                <div class="limitations-solutions">
                    <h4>应对PCA局限性的方法</h4>
                    <div class="solutions-container">
                        <div class="solution-card" :class="{ active: selectedSolution === 'kernel' }">
                            <div class="card-content" @click="selectSolution('kernel')">
                                <h5>核PCA (Kernel PCA)</h5>
                                <p>使用核技巧处理非线性数据，通过将数据映射到高维空间使其线性可分。</p>
                            </div>
                        </div>

                        <div class="solution-card" :class="{ active: selectedSolution === 'robust' }">
                            <div class="card-content" @click="selectSolution('robust')">
                                <h5>鲁棒PCA</h5>
                                <p>对异常值不敏感的PCA变体，能够在存在离群点的情况下提供稳定结果。</p>
                            </div>
                        </div>

                        <div class="solution-card" :class="{ active: selectedSolution === 'categorical' }">
                            <div class="card-content" @click="selectSolution('categorical')">
                                <h5>多重对应分析 (MCA)</h5>
                                <p>专为分类数据设计的降维技术，类似于分类变量的PCA。</p>
                            </div>
                        </div>

                        <div class="solution-card" :class="{ active: selectedSolution === 'sparse' }">
                            <div class="card-content" @click="selectSolution('sparse')">
                                <h5>稀疏PCA</h5>
                                <p>在标准PCA基础上加入稀疏约束，更适合处理高维稀疏数据。</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="match-exercise">
                    <h4>匹配练习：PCA局限性与解决方案</h4>
                    <p>请将左侧的PCA局限性与右侧的最佳解决方案匹配起来。</p>

                    <div class="match-container">
                        <div class="match-problems">
                            <div v-for="(problem, index) in problems" :key="`problem-${index}`" class="match-item"
                                :class="{ 'selected': selectedProblem === index }" @click="selectProblem(index)">
                                <span class="match-number">{{ index + 1 }}</span>
                                <span>{{ problem.text }}</span>
                            </div>
                        </div>

                        <div class="match-arrows">
                            <svg ref="arrowsSvg" width="100" height="400"></svg>
                        </div>

                        <div class="match-solutions">
                            <div v-for="(solution, index) in solutions" :key="`solution-${index}`" class="match-item"
                                :class="{ 'selected': selectedSolutionIndex === index }"
                                @click="selectSolutionForMatch(index)">
                                <span class="match-number">{{ String.fromCharCode(65 + index) }}</span>
                                <span>{{ solution.text }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="match-buttons">
                        <el-button type="primary" @click="createMatch"
                            :disabled="selectedProblem === null || selectedSolutionIndex === null">
                            创建匹配
                        </el-button>
                        <el-button type="danger" @click="clearMatch" :disabled="!hasMatches">
                            清除匹配
                        </el-button>
                        <el-button type="success" @click="checkMatches"
                            :disabled="userMatches.length < problems.length">
                            检查答案
                        </el-button>
                    </div>
                </div>
            </div>
        </template>
    </base-segment>
</template>

<script>
import BaseSegment from './BaseSegment.vue';
import * as d3 from 'd3';

export default {
    name: 'PCALimitations',
    components: {
        BaseSegment
    },
    data() {
        return {
            title: '8. PCA的局限性',
            segmentId: 'pca-limitations',
            content: `
  ## PCA的局限性与挑战
  
  尽管PCA是一种功能强大的降维工具，但它并非万能的解决方案。了解其局限性对于正确应用这一技术至关重要。
  
  ### 主要局限性
  
  #### 1. 线性假设
  
  PCA是一种**线性**降维技术，它假设数据可以通过线性变换进行有效表示。然而，现实世界中的许多数据集具有非线性结构，这时PCA可能无法有效捕捉数据的潜在模式。
  
  
  当数据呈现复杂的非线性关系时，可能需要考虑核PCA(Kernel PCA)或流形学习等非线性降维方法。
  
  #### 2. 方差最大化原则的局限
  
  PCA基于最大方差方向提取主成分，但在某些情况下，最大方差方向并不一定是最具信息量或最具区分性的方向。
  
  例如，在分类问题中，类别间差异可能存在于方差较小的方向上，而PCA会优先选择方差较大的方向，可能忽略这些重要信息。
  
  #### 3. 对异常值敏感
  
  由于PCA基于数据方差，异常值会对方差计算产生显著影响，从而影响主成分的方向。一个极端的异常值可能会导致主成分方向发生显著偏移。
  
  #### 4. 特征尺度影响
  
  如果不同特征的尺度（量级）差异很大，PCA会倾向于关注尺度较大的特征。因此，在应用PCA之前通常需要对数据进行标准化处理。
  
  #### 5. 结果解释性挑战
  
  PCA生成的主成分是原始特征的线性组合，这使得主成分的物理或业务含义可能难以解释，尤其是在高维数据中。
  
  #### 6. 对分类特征支持有限
  
  PCA主要设计用于处理连续数值特征，对于分类特征（如性别、颜色等），需要先进行适当的编码转换或使用多重对应分析(MCA)等替代方法。
  
  ### 应对PCA局限性的方法
  
  面对PCA的这些局限性，研究人员开发了许多扩展和替代方法：
  
  1. **非线性降维技术**：
     - 核PCA (Kernel PCA)
     - t-SNE (t-distributed Stochastic Neighbor Embedding)
     - UMAP (Uniform Manifold Approximation and Projection)
     - 自编码器 (Autoencoders)
  
  2. **鲁棒PCA变体**：对异常值不敏感的PCA实现
  
  3. **稀疏PCA**：在标准PCA基础上添加稀疏约束
  
  4. **监督PCA**：将目标变量信息纳入降维过程
  
  在下面的互动环节中，我们将探索一些PCA的局限性场景，并了解如何选择合适的替代方法。
        `,
            // 场景控制
            selectedScenario: 'nonlinear',

            // 可视化状态
            originalData: [],
            pcaResult: [],
            alternativeResult: [],

            // 解决方案选择
            selectedSolution: 'kernel',

            // 匹配练习
            problems: [
                { id: 'nonlinear', text: '数据具有明显的非线性结构' },
                { id: 'outlier', text: '数据中存在显著的异常值' },
                { id: 'categorical', text: '需要处理大量分类特征' },
                { id: 'scale', text: '特征的尺度差异极大' }
            ],
            solutions: [
                { id: 'kernel', text: '核PCA (Kernel PCA)' },
                { id: 'robust', text: '鲁棒PCA (Robust PCA)' },
                { id: 'mca', text: '多重对应分析 (MCA)' },
                { id: 'scaling', text: '标准化预处理' }
            ],
            selectedProblem: null,
            selectedSolutionIndex: null,
            userMatches: [],
            correctMatches: [
                { problem: 0, solution: 0 },  // 非线性 -> 核PCA
                { problem: 1, solution: 1 },  // 异常值 -> 鲁棒PCA
                { problem: 2, solution: 2 },  // 分类特征 -> MCA
                { problem: 3, solution: 3 }   // 尺度差异 -> 标准化
            ],
            matchAttempts: 0
        };
    },
    computed: {
        hasMatches() {
            return this.userMatches.length > 0;
        }
    },
    methods: {
        initVisualizations() {
            // 生成初始数据并创建可视化
            this.generateScenarioData();
            this.createVisualizations();
        },

        generateScenarioData() {
            const numPoints = 100;
            this.originalData = [];
            this.pcaResult = [];
            this.alternativeResult = [];

            switch (this.selectedScenario) {
                case 'nonlinear':
                    // 生成非线性数据（半圆形）
                    for (let i = 0; i < numPoints; i++) {
                        const angle = Math.PI * Math.random();
                        const noise = 0.2 * this.randomNormal();
                        const radius = 5 + noise;

                        const x = radius * Math.cos(angle);
                        const y = radius * Math.sin(angle);

                        this.originalData.push([x, y]);

                        // PCA结果（投影到水平方向，丢失半圆结构）
                        this.pcaResult.push([x, 0]);

                        // 核PCA或其他非线性方法的结果（保留结构）
                        this.alternativeResult.push([angle / Math.PI * 5, radius - 5]);
                    }
                    break;

                case 'outlier':
                    {// 生成带异常值的数据
                        // 主要数据（线性趋势）
                        for (let i = 0; i < numPoints - 5; i++) {
                            const x = 10 * Math.random() - 5;
                            const y = 0.5 * x + 0.3 * this.randomNormal();

                            this.originalData.push([x, y]);
                        }

                        // 添加几个异常值
                        for (let i = 0; i < 5; i++) {
                            const x = 3 * Math.random() - 1.5;
                            const y = -5 - 2 * Math.random();

                            this.originalData.push([x, y]);
                        }

                        // 计算标准PCA（受异常值影响）
                        const stdPCA = this.simplePCA(this.originalData);
                        this.pcaResult = stdPCA.projected;

                        // 模拟鲁棒PCA（不受异常值影响）
                        for (let i = 0; i < numPoints - 5; i++) {
                            const point = this.originalData[i];
                            const projectedX = 0.5 * point[0] + 0.5 * point[1];
                            this.alternativeResult.push([projectedX, 0]);
                        }

                        // 异常值单独处理
                        for (let i = numPoints - 5; i < numPoints; i++) {
                            const point = this.originalData[i];
                            this.alternativeResult.push([point[0], point[1]]);
                        }
                    }
                    break;

                case 'categorical':
                    {// 模拟分类数据
                        const categories = [
                            { x: -3, y: 2, label: 'A' },
                            { x: 0, y: 0, label: 'B' },
                            { x: 3, y: 2, label: 'C' }
                        ];

                        for (let i = 0; i < numPoints; i++) {
                            // 随机选择一个类别
                            const categoryIndex = Math.floor(Math.random() * 3);
                            const category = categories[categoryIndex];

                            // 在类别中心附近生成点
                            const x = category.x + 0.5 * this.randomNormal();
                            const y = category.y + 0.5 * this.randomNormal();

                            this.originalData.push([x, y, category.label]);
                        }

                        // PCA结果（忽略类别信息）
                        const catPCA = this.simplePCA(this.originalData.map(d => [d[0], d[1]]));
                        this.pcaResult = catPCA.projected.map((p, i) => [...p, this.originalData[i][2]]);

                        // MCA或其他分类方法（保留类别区分）
                        this.alternativeResult = this.originalData.map(d => {
                            switch (d[2]) {
                                case 'A': return [-3, 0, d[2]];
                                case 'B': return [0, 0, d[2]];
                                case 'C': return [3, 0, d[2]];
                            }
                        });
                    }
                    break;

                case 'sparse':
                    {// 模拟稀疏数据
                        for (let i = 0; i < numPoints; i++) {
                            const baseX = 10 * Math.random() - 5;

                            // 大多数点的y值为0或接近0
                            const y = Math.random() > 0.8 ?
                                2 * this.randomNormal() :  // 20%的点有非零值
                                0.1 * this.randomNormal();  // 80%的点接近0

                            this.originalData.push([baseX, y]);
                        }

                        // 标准PCA
                        const sparsePCA = this.simplePCA(this.originalData);
                        this.pcaResult = sparsePCA.projected;

                        // 稀疏PCA（更好地保留稀疏性）
                        this.alternativeResult = this.originalData.map(d => {
                            if (Math.abs(d[1]) > 0.5) {
                                // 保留显著非零值
                                return [d[0], d[1]];
                            } else {
                                // 将接近零的值设为精确零
                                return [d[0], 0];
                            }
                        });
                    }
                    break;
            }
        },

        randomNormal() {
            // Box-Muller变换生成标准正态分布随机数
            const u1 = Math.random();
            const u2 = Math.random();

            return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        },

        simplePCA(data) {
            // 简单的PCA实现，用于演示

            // 1. 计算均值
            const meanX = d3.mean(data, d => d[0]);
            const meanY = d3.mean(data, d => d[1]);

            // 2. 中心化数据
            const centered = data.map(d => [d[0] - meanX, d[1] - meanY]);

            // 3. 计算协方差矩阵
            let covXX = 0, covXY = 0, covYY = 0;
            centered.forEach(point => {
                covXX += point[0] * point[0];
                covXY += point[0] * point[1];
                covYY += point[1] * point[1];
            });

            covXX /= centered.length;
            covXY /= centered.length;
            covYY /= centered.length;

            // 4. 计算特征值和特征向量
            const trace = covXX + covYY;
            const det = covXX * covYY - covXY * covXY;

            const lambda1 = (trace + Math.sqrt(trace * trace - 4 * det)) / 2;
            const lambda2 = (trace - Math.sqrt(trace * trace - 4 * det)) / 2;

            // 计算特征向量
            let v1x, v1y, v2x, v2y;

            if (covXY === 0) {
                // 特殊情况：协方差为0
                if (covXX >= covYY) {
                    v1x = 1; v1y = 0;
                    v2x = 0; v2y = 1;
                } else {
                    v1x = 0; v1y = 1;
                    v2x = 1; v2y = 0;
                }
            } else {
                // 一般情况
                v1x = lambda1 - covYY;
                v1y = covXY;

                // 归一化
                const norm1 = Math.sqrt(v1x * v1x + v1y * v1y);
                v1x /= norm1;
                v1y /= norm1;

                // 第二个特征向量（正交）
                v2x = -v1y;
                v2y = v1x;
            }

            // 5. 投影数据到主成分
            const projected = centered.map(point => {
                // 计算在两个主成分上的投影
                const proj1 = point[0] * v1x + point[1] * v1y;
                const proj2 = point[0] * v2x + point[1] * v2y;

                return [proj1, proj2];
            });

            return {
                centered: centered,
                eigenvalues: [lambda1, lambda2],
                eigenvectors: [[v1x, v1y], [v2x, v2y]],
                projected: projected
            };
        },

        createVisualizations() {
            // 创建三个可视化：原始数据、PCA结果和替代方法
            this.createDataVisualization(this.$refs.originalDataVis, this.originalData, '原始数据');
            this.createDataVisualization(this.$refs.pcaResultVis, this.pcaResult, 'PCA结果', true);
            this.createDataVisualization(this.$refs.alternativeVis, this.alternativeResult, '替代方法结果', true);
        },

        createDataVisualization(container, data, title, showAxis = false) {
            // 清除容器
            d3.select(container).selectAll("*").remove();

            // 创建SVG
            const width = 280;
            const height = 220;
            const margin = { top: 20, right: 20, bottom: 30, left: 40 };

            const svg = d3.select(container)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 创建绘图区域
            const g = svg.append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // 计算实际绘图区域
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 确定数据的范围
            let xExtent, yExtent;

            // 对于分类场景，手动设置坐标范围
            if (this.selectedScenario === 'categorical' && data[0] && data[0].length > 2) {
                xExtent = [-5, 5];
                yExtent = [-3, 3];
            } else {
                xExtent = d3.extent(data, d => d[0]);
                yExtent = d3.extent(data, d => d[1]);

                // 为界限增加一些边距
                const xPadding = Math.max(0.1, (xExtent[1] - xExtent[0]) * 0.1);
                const yPadding = Math.max(0.1, (yExtent[1] - yExtent[0]) * 0.1);

                xExtent = [xExtent[0] - xPadding, xExtent[1] + xPadding];
                yExtent = [yExtent[0] - yPadding, yExtent[1] + yPadding];
            }

            // 创建比例尺
            const xScale = d3.scaleLinear()
                .domain(xExtent)
                .range([0, plotWidth]);

            const yScale = d3.scaleLinear()
                .domain(yExtent)
                .range([plotHeight, 0]);

            // 绘制坐标轴（如果需要）
            if (showAxis) {
                g.append("g")
                    .attr("transform", `translate(0, ${plotHeight / 2})`)
                    .call(d3.axisBottom(xScale).ticks(5));

                g.append("g")
                    .attr("transform", `translate(${plotWidth / 2}, 0)`)
                    .call(d3.axisLeft(yScale).ticks(5));

                // 绘制坐标轴标签
                g.append("text")
                    .attr("x", plotWidth)
                    .attr("y", plotHeight / 2 + 15)
                    .style("text-anchor", "end")
                    .style("font-size", "10px")
                    .text("第一主成分");

                g.append("text")
                    .attr("x", plotWidth / 2 - 5)
                    .attr("y", 0)
                    .style("text-anchor", "end")
                    .style("font-size", "10px")
                    .text("第二主成分");
            } else {
                // 只绘制原点参考线
                g.append("line")
                    .attr("x1", 0)
                    .attr("y1", plotHeight / 2)
                    .attr("x2", plotWidth)
                    .attr("y2", plotHeight / 2)
                    .style("stroke", "#ddd")
                    .style("stroke-width", 1);

                g.append("line")
                    .attr("x1", plotWidth / 2)
                    .attr("y1", 0)
                    .attr("x2", plotWidth / 2)
                    .attr("y2", plotHeight)
                    .style("stroke", "#ddd")
                    .style("stroke-width", 1);
            }

            // 绘制数据点
            if (this.selectedScenario === 'categorical' && data[0] && data[0].length > 2) {
                // 分类场景：使用不同颜色
                const colorScale = d3.scaleOrdinal()
                    .domain(['A', 'B', 'C'])
                    .range(['#1f77b4', '#ff7f0e', '#2ca02c']);

                g.selectAll(".data-point")
                    .data(data)
                    .enter()
                    .append("circle")
                    .attr("class", "data-point")
                    .attr("cx", d => xScale(d[0]))
                    .attr("cy", d => yScale(d[1]))
                    .attr("r", 4)
                    .style("fill", d => colorScale(d[2]))
                    .style("opacity", 0.7);

                // 添加图例
                const legend = g.append("g")
                    .attr("transform", `translate(${plotWidth - 50}, 0)`);

                ['A', 'B', 'C'].forEach((category, i) => {
                    legend.append("circle")
                        .attr("cx", 0)
                        .attr("cy", i * 20 + 10)
                        .attr("r", 4)
                        .style("fill", colorScale(category));

                    legend.append("text")
                        .attr("x", 10)
                        .attr("y", i * 20 + 13)
                        .style("font-size", "10px")
                        .text(category);
                });
            } else if (this.selectedScenario === 'outlier') {
                // 异常值场景：区分正常点和异常点
                g.selectAll(".data-point")
                    .data(data)
                    .enter()
                    .append("circle")
                    .attr("class", "data-point")
                    .attr("cx", d => xScale(d[0]))
                    .attr("cy", d => yScale(d[1]))
                    .attr("r", 4)
                    .style("fill", (d, i) => i >= data.length - 5 ? "#e41a1c" : "#377eb8")
                    .style("opacity", 0.7);

                // 添加图例
                if (container === this.$refs.originalDataVis) {
                    const legend = g.append("g")
                        .attr("transform", `translate(${plotWidth - 50}, 0)`);

                    // 正常点
                    legend.append("circle")
                        .attr("cx", 0)
                        .attr("cy", 10)
                        .attr("r", 4)
                        .style("fill", "#377eb8");

                    legend.append("text")
                        .attr("x", 10)
                        .attr("y", 13)
                        .style("font-size", "10px")
                        .text("正常数据");

                    // 异常点
                    legend.append("circle")
                        .attr("cx", 0)
                        .attr("cy", 30)
                        .attr("r", 4)
                        .style("fill", "#e41a1c");

                    legend.append("text")
                        .attr("x", 10)
                        .attr("y", 33)
                        .style("font-size", "10px")
                        .text("异常值");
                }
            } else {
                // 其他场景：普通点
                g.selectAll(".data-point")
                    .data(data)
                    .enter()
                    .append("circle")
                    .attr("class", "data-point")
                    .attr("cx", d => xScale(d[0]))
                    .attr("cy", d => yScale(d[1]))
                    .attr("r", 4)
                    .style("fill", "#69b3a2")
                    .style("opacity", 0.7);
            }

            // 添加特殊可视化元素
            if (this.selectedScenario === 'nonlinear') {
                // 原始数据：显示非线性结构
                if (container === this.$refs.originalDataVis) {
                    // 添加曲线以显示非线性关系
                    const line = d3.line()
                        .x(d => xScale(5 * Math.cos(d)))
                        .y(d => yScale(5 * Math.sin(d)))
                        .curve(d3.curveBasis);

                    const points = Array.from({ length: 50 }, (_, i) => i / 49 * Math.PI);

                    g.append("path")
                        .datum(points)
                        .attr("d", line)
                        .attr("fill", "none")
                        .attr("stroke", "#ff7f0e")
                        .attr("stroke-width", 2)
                        .attr("stroke-dasharray", "5,5");
                }

                // PCA结果：显示投影线
                if (container === this.$refs.pcaResultVis) {
                    // 添加参考线表示主成分方向
                    g.append("line")
                        .attr("x1", 0)
                        .attr("y1", plotHeight / 2)
                        .attr("x2", plotWidth)
                        .attr("y2", plotHeight / 2)
                        .style("stroke", "red")
                        .style("stroke-width", 2)
                        .style("stroke-dasharray", "5,5");
                }
            }

            // 为sparse场景添加特殊标记
            if (this.selectedScenario === 'sparse' && container === this.$refs.alternativeVis) {
                // 标记被设置为精确零的点
                g.selectAll(".zero-marker")
                    .data(data.filter(d => d[1] === 0))
                    .enter()
                    .append("circle")
                    .attr("class", "zero-marker")
                    .attr("cx", d => xScale(d[0]))
                    .attr("cy", d => yScale(d[1]))
                    .attr("r", 6)
                    .style("fill", "none")
                    .style("stroke", "red")
                    .style("stroke-width", 1);
            }

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 10)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .style("font-weight", "bold")
                .text(title);

            // 为替代方法添加说明标签
            if (container === this.$refs.alternativeVis) {
                let methodName;

                switch (this.selectedScenario) {
                    case 'nonlinear': methodName = "核PCA"; break;
                    case 'outlier': methodName = "鲁棒PCA"; break;
                    case 'categorical': methodName = "多重对应分析"; break;
                    case 'sparse': methodName = "稀疏PCA"; break;
                }

                svg.append("text")
                    .attr("x", width / 2)
                    .attr("y", height - 5)
                    .attr("text-anchor", "middle")
                    .style("font-size", "11px")
                    .style("fill", "#1890ff")
                    .text(`(${methodName})`);
            }
        },

        updateScenario() {
            // 更新选择的解决方案以匹配场景
            switch (this.selectedScenario) {
                case 'nonlinear': this.selectedSolution = 'kernel'; break;
                case 'outlier': this.selectedSolution = 'robust'; break;
                case 'categorical': this.selectedSolution = 'categorical'; break;
                case 'sparse': this.selectedSolution = 'sparse'; break;
            }

            // 重新生成数据和可视化
            this.generateScenarioData();
            this.createVisualizations();
        },

        selectSolution(solution) {
            this.selectedSolution = solution;
        },

        // 匹配练习方法
        selectProblem(index) {
            this.selectedProblem = index;
        },

        selectSolutionForMatch(index) {
            this.selectedSolutionIndex = index;
        },

        createMatch() {
            if (this.selectedProblem === null || this.selectedSolutionIndex === null) return;

            // 检查是否已存在该问题的匹配
            const existingMatchIndex = this.userMatches.findIndex(m => m.problem === this.selectedProblem);

            if (existingMatchIndex !== -1) {
                // 更新现有匹配
                this.$set(this.userMatches[existingMatchIndex], 'solution', this.selectedSolutionIndex);
            } else {
                // 创建新匹配
                this.userMatches.push({
                    problem: this.selectedProblem,
                    solution: this.selectedSolutionIndex
                });
            }

            // 绘制连接线
            this.drawMatchArrows();

            // 重置选择
            this.selectedProblem = null;
            this.selectedSolutionIndex = null;
        },

        clearMatch() {
            this.userMatches = [];
            this.drawMatchArrows();
        },

        drawMatchArrows() {
            const svg = d3.select(this.$refs.arrowsSvg);
            svg.selectAll("*").remove();

            const arrowWidth = 100;
            const problemItemHeight = 50; // 每个问题项的高度
            const solutionItemHeight = 50; // 每个解决方案项的高度

            this.userMatches.forEach(match => {
                const startY = match.problem * problemItemHeight + 25;
                const endY = match.solution * solutionItemHeight + 25;

                // 绘制连接线
                svg.append("path")
                    .attr("d", `M0,${startY} C50,${startY} 50,${endY} 100,${endY}`)
                    .attr("fill", "none")
                    .attr("stroke", "#409EFF")
                    .attr("stroke-width", 2);

                // 在线的两端添加小圆点
                svg.append("circle")
                    .attr("cx", 0)
                    .attr("cy", startY)
                    .attr("r", 3)
                    .attr("fill", "#409EFF");

                svg.append("circle")
                    .attr("cx", arrowWidth)
                    .attr("cy", endY)
                    .attr("r", 3)
                    .attr("fill", "#409EFF");
            });
        },

        checkMatches() {
            this.matchAttempts++;

            // 检查用户匹配是否正确
            let correct = true;

            if (this.userMatches.length !== this.correctMatches.length) {
                correct = false;
            } else {
                // 对每个正确匹配，检查用户是否有相应的匹配
                for (const correctMatch of this.correctMatches) {
                    const userMatch = this.userMatches.find(m => m.problem === correctMatch.problem);

                    if (!userMatch || userMatch.solution !== correctMatch.solution) {
                        correct = false;
                        break;
                    }
                }
            }

            if (correct) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "匹配正确！",
                    "您已正确匹配PCA的局限性和相应的解决方案。理解这些局限性和替代方法对于在实际场景中正确应用PCA至关重要。",
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.matchAttempts >= 2) {
                    hint = "提示：考虑每个限制的本质特点，以及哪种方法专门针对这种限制设计。例如，处理非线性数据结构需要哪种变换？";
                }

                this.$refs.baseSegment.showResponse(
                    "匹配不完全正确",
                    `请检查您的匹配并重试。${hint}`,
                    "error"
                );
            }
        },

        onCompleted() {
            // 通知父组件此片段已完成
            this.$emit('completed', this.segmentId);
        }
    },
    mounted() {
        // 初始化可视化
        this.$nextTick(() => {
            this.initVisualizations();
            this.drawMatchArrows();
        });
    },
    beforeDestroy() {
        // 清理D3资源
        const containers = [
            this.$refs.originalDataVis,
            this.$refs.pcaResultVis,
            this.$refs.alternativeVis,
            this.$refs.arrowsSvg
        ];

        containers.forEach(container => {
            if (container) {
                d3.select(container).selectAll("*").remove();
            }
        });
    }
}
</script>

<style scoped>
.limitations-interactive {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.demo-controls {
    margin-bottom: 20px;
}

.scenario-description {
    margin-top: 15px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    border-left: 4px solid #409EFF;
}

.visualization-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 30px;
    justify-content: center;
}

.visualization-wrapper {
    text-align: center;
}

.visualization {
    width: 280px;
    height: 220px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    margin-top: 10px;
}

.limitations-solutions {
    margin-bottom: 30px;
}

.solutions-container {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 15px;
}

.solution-card {
    flex: 1;
    min-width: 200px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    padding: 15px;
    background-color: #f5f7fa;
    cursor: pointer;
    transition: all 0.3s;
}

.solution-card:hover {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    transform: translateY(-5px);
}

.solution-card.active {
    border-color: #409EFF;
    background-color: #ecf5ff;
}

.card-content h5 {
    margin-top: 0;
    color: #303133;
}

.match-exercise {
    margin-top: 30px;
    padding: 20px;
    background-color: #ecf5ff;
    border-radius: 4px;
}

.match-container {
    display: flex;
    margin: 20px 0;
}

.match-problems,
.match-solutions {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.match-arrows {
    width: 100px;
    position: relative;
}

.match-item {
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    height: 20px;
}

.match-item.selected {
    border: 2px solid #409EFF;
    background-color: #ecf5ff;
}

.match-number {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 24px;
    height: 24px;
    background-color: #409EFF;
    color: white;
    border-radius: 50%;
    font-weight: bold;
}

.match-buttons {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}
</style>