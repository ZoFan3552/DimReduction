<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="dim-reduction-interactive">
                <h3>降维过程可视化</h3>
                <p>通过这个交互式演示，您将看到PCA降维的整个过程，从原始数据到降维结果。</p>

                <div class="process-controls">
                    <h4>演示控制</h4>
                    <div class="process-buttons">
                        <el-button type="primary" @click="startDemo" :disabled="isPlaying">开始演示</el-button>
                        <el-button type="info" @click="pauseDemo" :disabled="!isPlaying">暂停</el-button>
                        <el-button type="warning" @click="resetDemo" :disabled="currentStep === 0">重置</el-button>
                    </div>

                    <div class="step-display">
                        <el-steps :active="currentStep" finish-status="success" simple>
                            <el-step v-for="(step, index) in demoSteps" :key="index" :title="step.title"></el-step>
                        </el-steps>
                    </div>
                </div>

                <div class="visualization-container">
                    <div id="pca-process-visualization" ref="processVisualization"></div>
                </div>

                <div class="step-description">
                    <template v-if="currentStep < demoSteps.length">
                        <h4>{{ demoSteps[currentStep].title }}</h4>
                        <p>{{ demoSteps[currentStep].description }}</p>
                    </template>
                    <template v-else>
                        <h4>演示完成</h4>
                        <p>您已完成PCA降维过程的演示。您现在可以尝试解答下面的问题，或重置演示再次观看。</p>
                    </template>
                </div>

                <div v-if="currentStep === demoSteps.length" class="understanding-check">
                    <h4>理解检查</h4>
                    <p>根据演示，请将PCA降维的步骤按正确顺序排列：</p>

                    <div class="sortable-container">
                        <el-card v-for="(item, index) in userSortedSteps" :key="index" class="sort-item">
                            <div class="step-content">
                                <span class="step-number">{{ index + 1 }}</span>
                                <span>{{ item.text }}</span>
                            </div>
                            <div class="step-controls">
                                <el-button type="text" icon="el-icon-arrow-up" @click="moveStep(index, -1)"
                                    :disabled="index === 0">
                                    上移
                                </el-button>
                                <el-button type="text" icon="el-icon-arrow-down" @click="moveStep(index, 1)"
                                    :disabled="index === userSortedSteps.length - 1">
                                    下移
                                </el-button>
                            </div>
                        </el-card>
                    </div>

                    <el-button type="primary" @click="checkStepOrder" class="check-order-button">
                        检查顺序
                    </el-button>
                </div>
            </div>
        </template>
    </base-segment>
</template>

<script>
import BaseSegment from './BaseSegment.vue'
import * as d3 from 'd3'
// import * as math from 'mathjs'

export default {
    name: 'DimensionalityReduction',
    components: {
        BaseSegment
    },
    data() {
        return {
            title: '6. 降维过程',
            segmentId: 'dimensionality-reduction',
            content: `
  ## PCA降维过程详解
  
  在前面的章节中，我们学习了PCA的基本原理和关键概念。现在，让我们系统地走一遍完整的PCA降维过程。
  
  ### PCA降维的计算步骤
  
  PCA降维的完整计算过程包含以下步骤：
  
  #### 1. 数据预处理
  
  PCA对数据的分布很敏感，因此通常需要进行预处理：
  - **中心化**：将每个特征的均值调整为0
  - **标准化**（可选）：将每个特征的方差调整为1
  
  数学表示：对于原始数据矩阵 $X$，中心化后的数据为：
  
  $$X_{centered} = X - \\mu$$
  
  其中 $\\mu$ 是每个特征的均值向量。
  
  #### 2. 计算协方差矩阵
  
  使用中心化后的数据计算协方差矩阵：
  
  $$\\Sigma = \\frac{1}{n} X_{centered}^T X_{centered}$$
  
  其中 $n$ 是样本数量。
  
  #### 3. 计算特征值和特征向量
  
  对协方差矩阵 $\\Sigma$ 进行特征值分解：
  
  $$\\Sigma v_i = \\lambda_i v_i$$
  
  得到特征值 $\\lambda_i$ 和对应的特征向量 $v_i$。
  
  #### 4. 特征值排序
  
  将特征值按从大到小排序，并相应地排列特征向量。
  
  #### 5. 选择主成分
  
  根据某种标准（如累计方差贡献率）选择前 $k$ 个特征向量，构成投影矩阵 $P$。
  
  $$P = [v_1, v_2, ..., v_k]$$
  
  #### 6. 数据投影
  
  将原始数据投影到新的低维空间：
  
  $$Y = X_{centered} \\cdot P$$
  
  其中 $Y$ 是降维后的数据，维度从原来的 $d$ 降为 $k$。
  
  ### 降维结果的特点
  
  通过PCA降维后的数据具有以下特点：
  - 维度减少，便于可视化和后续处理
  - 各维度间相互正交，消除了原始特征间的相关性
  - 第一维包含最大方差，第二维包含次大方差，依此类推
  - 保留了原始数据的主要结构和模式
  
  ### 降维信息损失
  
  需要注意的是，降维不可避免地会导致信息损失。这种损失可以通过解释方差比例来量化：
  
  $$\text{信息保留率} = \\frac{\\sum_{i=1}^{k} \\lambda_i}{\\sum_{i=1}^{d} \\lambda_i}$$
  
  在选择主成分数量时，需要在维度降低和信息保留之间取得平衡。
  
  在下面的交互式演示中，您可以直观地观察PCA降维的全过程。
        `,
            // 演示控制
            isPlaying: false,
            currentStep: 0,
            demoInterval: null,
            stepDuration: 4000, // 每个步骤持续4秒

            // 演示步骤
            demoSteps: [
                {
                    title: "1. 原始数据",
                    description: "这是我们的原始二维数据。我们的目标是将其降到一维，同时保留尽可能多的信息。"
                },
                {
                    title: "2. 数据中心化",
                    description: "首先，我们将数据中心化，使每个特征的均值为0。这相当于将数据点平移到坐标原点周围。"
                },
                {
                    title: "3. 计算协方差矩阵",
                    description: "接下来，我们计算数据的协方差矩阵，这反映了不同特征之间的关系。"
                },
                {
                    title: "4. 计算特征值和特征向量",
                    description: "我们对协方差矩阵进行特征值分解，得到特征值和特征向量。特征向量指示数据的主要方向。"
                },
                {
                    title: "5. 绘制主成分方向",
                    description: "特征向量就是主成分的方向。第一主成分（红色）指向数据方差最大的方向，第二主成分（蓝色）与第一主成分正交。"
                },
                {
                    title: "6. 选择主成分",
                    description: "为了降维，我们选择保留第一主成分，它捕获了数据中最多的方差。"
                },
                {
                    title: "7. 数据投影",
                    description: "最后，我们将原始数据点投影到第一主成分上，得到降维后的一维数据。"
                }
            ],

            // 可视化参数
            svg: null,
            width: 700,
            height: 500,
            margin: { top: 40, right: 40, bottom: 40, left: 40 },

            // 数据
            originalData: [],
            centeredData: [],
            covarianceMatrix: [],
            eigenvalues: [],
            eigenvectors: [],
            projectedData: [],

            // 排序题
            correctStepOrder: [
                { text: "对原始数据进行中心化处理" },
                { text: "计算中心化数据的协方差矩阵" },
                { text: "对协方差矩阵进行特征值分解" },
                { text: "将特征值和特征向量按降序排列" },
                { text: "选择前k个主成分作为投影矩阵" },
                { text: "将原始数据投影到新的低维空间" }
            ],
            userSortedSteps: [],
            orderAttempts: 0
        };
    },
    methods: {
        initDemo() {
            // 清除之前的可视化
            d3.select(this.$refs.processVisualization).selectAll("*").remove();

            // 生成随机数据
            this.generateData();

            // 创建SVG
            this.svg = d3.select(this.$refs.processVisualization)
                .append("svg")
                .attr("width", this.width)
                .attr("height", this.height);

            // 绘制初始状态
            this.drawStep(0);

            // 初始化排序题
            this.initSortingQuestion();
        },

        generateData() {
            // 生成带有一定相关性的二维数据（保持不变）
            const numPoints = 50;
            const correlation = 0.8;
            const variance1 = 5;
            const variance2 = 1;

            this.originalData = [];
            for (let i = 0; i < numPoints; i++) {
                const x = this.randomNormal() * Math.sqrt(variance1);
                const y = correlation * x + this.randomNormal() * Math.sqrt(variance2);
                this.originalData.push([x, y]);
            }

            // 计算中心化数据（保持不变）
            const meanX = d3.mean(this.originalData, d => d[0]);
            const meanY = d3.mean(this.originalData, d => d[1]);
            this.centeredData = this.originalData.map(d => [
                d[0] - meanX,
                d[1] - meanY
            ]);

            // 计算协方差矩阵（保持不变）
            let covXX = 0, covXY = 0, covYY = 0;
            this.centeredData.forEach(point => {
                covXX += point[0] * point[0];
                covXY += point[0] * point[1];
                covYY += point[1] * point[1];
            });
            covXX /= this.centeredData.length;
            covXY /= this.centeredData.length;
            covYY /= this.centeredData.length;
            this.covarianceMatrix = [
                [covXX, covXY],
                [covXY, covYY]
            ];

            // ========== 修正的特征值/向量计算部分 ==========
            this.computeEigenvectors();

            // ========== 投影计算部分（保持不变） ==========
            this.projectedData = this.centeredData.map(point => {
                const dot = point[0] * this.eigenvectors[0][0] + point[1] * this.eigenvectors[0][1];
                return {
                    original: point,
                    projected: [
                        dot * this.eigenvectors[0][0],
                        dot * this.eigenvectors[0][1]
                    ],
                    value: dot
                };
            });
        },
        // 在您的Vue组件methods中添加这个方法
        computeEigenvectors() {
            try {
                const cov = this.covarianceMatrix;

                // 对于2x2矩阵，我们可以直接计算特征值和特征向量
                const a = cov[0][0], b = cov[0][1];
                const c = cov[1][0], d = cov[1][1];

                // 计算特征值
                const trace = a + d;
                const det = a * d - b * c;
                const discriminant = trace * trace - 4 * det;

                if (discriminant < 0) {
                    throw new Error("矩阵没有实数特征值");
                }

                const sqrtDisc = Math.sqrt(discriminant);
                this.eigenvalues = [
                    (trace + sqrtDisc) / 2,
                    (trace - sqrtDisc) / 2
                ];

                // 计算特征向量
                this.eigenvectors = [];
                for (let i = 0; i < 2; i++) {
                    const lambda = this.eigenvalues[i];
                    // 解 (A - λI)v = 0
                    let x, y;

                    if (b !== 0) {
                        x = b;
                        y = lambda - a;
                    } else if (c !== 0) {
                        x = lambda - d;
                        y = c;
                    } else {
                        // 对角矩阵情况
                        x = 1;
                        y = 0;
                    }

                    // 归一化
                    const length = Math.sqrt(x * x + y * y);
                    this.eigenvectors.push([x / length, y / length]);
                }

                // 确保按特征值降序排列
                if (this.eigenvalues[0] < this.eigenvalues[1]) {
                    [this.eigenvalues[0], this.eigenvalues[1]] = [this.eigenvalues[1], this.eigenvalues[0]];
                    [this.eigenvectors[0], this.eigenvectors[1]] = [this.eigenvectors[1], this.eigenvectors[0]];
                }

            } catch (e) {
                console.error("特征计算错误:", e);
                // 安全默认值
                this.eigenvalues = [1, 0];
                this.eigenvectors = [[1, 0], [0, 1]];
            }
        },

        randomNormal() {
            // Box-Muller变换生成标准正态分布随机数
            const u1 = Math.random();
            const u2 = Math.random();

            return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        },

        drawStep(step) {
            // 清除SVG内容
            this.svg.selectAll("*").remove();

            // 创建绘图组
            const g = this.svg.append("g")
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

            // 绘图区域尺寸
            const plotWidth = this.width - this.margin.left - this.margin.right;
            const plotHeight = this.height - this.margin.top - this.margin.bottom;

            // 根据当前步骤绘制不同内容
            switch (step) {
                case 0: // 原始数据
                    this.drawOriginalData(g, plotWidth, plotHeight);
                    break;
                case 1: // 数据中心化
                    this.drawCenteredData(g, plotWidth, plotHeight);
                    break;
                case 2: // 协方差矩阵
                    this.drawCovarianceMatrix(g, plotWidth, plotHeight);
                    break;
                case 3: // 特征值和特征向量
                    this.drawEigenDecomposition(g, plotWidth, plotHeight);
                    break;
                case 4: // 主成分方向
                    this.drawPrincipalComponents(g, plotWidth, plotHeight);
                    break;
                case 5: // 选择主成分
                    this.drawSelectedComponent(g, plotWidth, plotHeight);
                    break;
                case 6: // 数据投影
                    this.drawProjection(g, plotWidth, plotHeight);
                    break;
            }
        },

        drawOriginalData(g, width, height) {
            // 计算数据范围
            const xExtent = d3.extent(this.originalData, d => d[0]);
            const yExtent = d3.extent(this.originalData, d => d[1]);

            // 添加边距
            const xRange = [
                xExtent[0] - (xExtent[1] - xExtent[0]) * 0.1,
                xExtent[1] + (xExtent[1] - xExtent[0]) * 0.1
            ];

            const yRange = [
                yExtent[0] - (yExtent[1] - yExtent[0]) * 0.1,
                yExtent[1] + (yExtent[1] - yExtent[0]) * 0.1
            ];

            // 创建比例尺
            const xScale = d3.scaleLinear()
                .domain(xRange)
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain(yRange)
                .range([height, 0]);

            // 绘制坐标轴
            g.append("g")
                .attr("transform", `translate(0,${yScale(0)})`)
                .call(d3.axisBottom(xScale));

            g.append("g")
                .attr("transform", `translate(${xScale(0)},0)`)
                .call(d3.axisLeft(yScale));

            // 绘制数据点
            g.selectAll(".data-point")
                .data(this.originalData)
                .enter()
                .append("circle")
                .attr("class", "data-point")
                .attr("cx", d => xScale(d[0]))
                .attr("cy", d => yScale(d[1]))
                .attr("r", 5)
                .style("fill", "#69b3a2")
                .style("opacity", 0.7);

            // 添加标题
            g.append("text")
                .attr("x", width / 2)
                .attr("y", -20)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("font-weight", "bold")
                .text("原始二维数据");

            // 保存当前比例尺以便后续使用
            this.xScale = xScale;
            this.yScale = yScale;
        },

        drawCenteredData(g, width, height) {
            // 创建比例尺
            const maxValue = d3.max([
                ...this.centeredData.map(d => Math.abs(d[0])),
                ...this.centeredData.map(d => Math.abs(d[1]))
            ]) * 1.2;

            const xScale = d3.scaleLinear()
                .domain([-maxValue, maxValue])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([-maxValue, maxValue])
                .range([height, 0]);

            // 绘制坐标轴
            g.append("g")
                .attr("transform", `translate(0,${yScale(0)})`)
                .call(d3.axisBottom(xScale));

            g.append("g")
                .attr("transform", `translate(${xScale(0)},0)`)
                .call(d3.axisLeft(yScale));

            // 绘制原始数据点（淡色）
            g.selectAll(".original-point")
                .data(this.originalData)
                .enter()
                .append("circle")
                .attr("class", "original-point")
                .attr("cx", d => this.xScale(d[0]))
                .attr("cy", d => this.yScale(d[1]))
                .attr("r", 5)
                .style("fill", "#cccccc")
                .style("opacity", 0.5);

            // 绘制中心化数据点
            g.selectAll(".centered-point")
                .data(this.centeredData)
                .enter()
                .append("circle")
                .attr("class", "centered-point")
                .attr("cx", d => xScale(d[0]))
                .attr("cy", d => yScale(d[1]))
                .attr("r", 5)
                .style("fill", "#69b3a2")
                .style("opacity", 0.7);

            // 添加中心点
            g.append("circle")
                .attr("cx", xScale(0))
                .attr("cy", yScale(0))
                .attr("r", 7)
                .style("fill", "red")
                .style("opacity", 0.7);

            // 添加标题
            g.append("text")
                .attr("x", width / 2)
                .attr("y", -20)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("font-weight", "bold")
                .text("中心化后的数据");

            // 添加说明
            g.append("text")
                .attr("x", width - 20)
                .attr("y", 20)
                .attr("text-anchor", "end")
                .style("font-size", "14px")
                .text("灰色：原始数据");

            g.append("text")
                .attr("x", width - 20)
                .attr("y", 40)
                .attr("text-anchor", "end")
                .style("font-size", "14px")
                .text("绿色：中心化数据");

            // 保存当前比例尺
            this.xScale = xScale;
            this.yScale = yScale;
        },

        drawCovarianceMatrix(g, width, height) {
            // 保留中心化数据的绘制
            this.drawCenteredData(g, width, height);

            // 在图表上添加协方差矩阵
            const matrixContainer = g.append("g")
                .attr("transform", `translate(${width - 180}, ${height - 180})`);

            matrixContainer.append("rect")
                .attr("width", 160)
                .attr("height", 120)
                .attr("fill", "white")
                .attr("stroke", "#333")
                .attr("opacity", 0.9);

            matrixContainer.append("text")
                .attr("x", 80)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .style("font-weight", "bold")
                .text("协方差矩阵");

            // 添加矩阵内容
            const matrixContent = matrixContainer.append("g")
                .attr("transform", "translate(10, 40)");

            // 左括号
            matrixContent.append("text")
                .attr("x", 0)
                .attr("y", 35)
                .attr("text-anchor", "middle")
                .style("font-size", "40px")
                .text("[");

            // 右括号
            matrixContent.append("text")
                .attr("x", 140)
                .attr("y", 35)
                .attr("text-anchor", "middle")
                .style("font-size", "40px")
                .text("]");

            // 矩阵元素
            const cellPositions = [
                { x: 40, y: 20 },
                { x: 100, y: 20 },
                { x: 40, y: 50 },
                { x: 100, y: 50 }
            ];

            const flatMatrix = [
                this.covarianceMatrix[0][0],
                this.covarianceMatrix[0][1],
                this.covarianceMatrix[1][0],
                this.covarianceMatrix[1][1]
            ];

            for (let i = 0; i < 4; i++) {
                matrixContent.append("text")
                    .attr("x", cellPositions[i].x)
                    .attr("y", cellPositions[i].y)
                    .attr("text-anchor", "middle")
                    .text(flatMatrix[i].toFixed(2));
            }
        },

        drawEigenDecomposition(g, width, height) {
            // 保留中心化数据的绘制
            this.drawCenteredData(g, width, height);

            // 在图表上添加特征值和特征向量信息
            const eigenContainer = g.append("g")
                .attr("transform", `translate(${width - 230}, ${height - 200})`);

            eigenContainer.append("rect")
                .attr("width", 210)
                .attr("height", 180)
                .attr("fill", "white")
                .attr("stroke", "#333")
                .attr("opacity", 0.9);

            eigenContainer.append("text")
                .attr("x", 105)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .style("font-weight", "bold")
                .text("特征值和特征向量");

            // 添加特征值
            eigenContainer.append("text")
                .attr("x", 20)
                .attr("y", 50)
                .text(`λ₁ = ${this.eigenvalues[0].toFixed(2)}`);

            eigenContainer.append("text")
                .attr("x", 20)
                .attr("y", 70)
                .text(`λ₂ = ${this.eigenvalues[1].toFixed(2)}`);

            // 添加特征向量
            eigenContainer.append("text")
                .attr("x", 20)
                .attr("y", 100)
                .text("第一特征向量:");

            eigenContainer.append("text")
                .attr("x", 40)
                .attr("y", 120)
                .text(`[${this.eigenvectors[0][0].toFixed(2)}, ${this.eigenvectors[0][1].toFixed(2)}]`);

            eigenContainer.append("text")
                .attr("x", 20)
                .attr("y", 140)
                .text("第二特征向量:");

            eigenContainer.append("text")
                .attr("x", 40)
                .attr("y", 160)
                .text(`[${this.eigenvectors[1][0].toFixed(2)}, ${this.eigenvectors[1][1].toFixed(2)}]`);
        },

        drawPrincipalComponents(g, width, height) {
            // 保留中心化数据的绘制
            this.drawCenteredData(g, width, height);

            // 绘制特征向量（主成分方向）
            const scaleFactor = Math.sqrt(
                d3.max([...this.centeredData.map(d => Math.abs(d[0])), ...this.centeredData.map(d => Math.abs(d[1]))])
            ) * 1.5;

            // 第一主成分方向（红色）
            g.append("line")
                .attr("x1", this.xScale(-this.eigenvectors[0][0] * scaleFactor))
                .attr("y1", this.yScale(-this.eigenvectors[0][1] * scaleFactor))
                .attr("x2", this.xScale(this.eigenvectors[0][0] * scaleFactor))
                .attr("y2", this.yScale(this.eigenvectors[0][1] * scaleFactor))
                .style("stroke", "red")
                .style("stroke-width", 2);

            // 第二主成分方向（蓝色）
            g.append("line")
                .attr("x1", this.xScale(-this.eigenvectors[1][0] * scaleFactor))
                .attr("y1", this.yScale(-this.eigenvectors[1][1] * scaleFactor))
                .attr("x2", this.xScale(this.eigenvectors[1][0] * scaleFactor))
                .attr("y2", this.yScale(this.eigenvectors[1][1] * scaleFactor))
                .style("stroke", "blue")
                .style("stroke-width", 2);

            // 添加标签
            g.append("text")
                .attr("x", this.xScale(this.eigenvectors[0][0] * scaleFactor))
                .attr("y", this.yScale(this.eigenvectors[0][1] * scaleFactor))
                .attr("dx", 10)
                .style("fill", "red")
                .text("第一主成分");

            g.append("text")
                .attr("x", this.xScale(this.eigenvectors[1][0] * scaleFactor))
                .attr("y", this.yScale(this.eigenvectors[1][1] * scaleFactor))
                .attr("dx", 10)
                .style("fill", "blue")
                .text("第二主成分");

            // 添加特征值信息
            g.append("text")
                .attr("x", width - 200)
                .attr("y", 50)
                .style("font-size", "14px")
                .text(`第一主成分方差: ${this.eigenvalues[0].toFixed(2)}`);

            g.append("text")
                .attr("x", width - 200)
                .attr("y", 70)
                .style("font-size", "14px")
                .text(`第二主成分方差: ${this.eigenvalues[1].toFixed(2)}`);

            g.append("text")
                .attr("x", width - 200)
                .attr("y", 100)
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text(`方差解释比: ${(this.eigenvalues[0] / (this.eigenvalues[0] + this.eigenvalues[1]) * 100).toFixed(1)}%`);
        },

        drawSelectedComponent(g, width, height) {
            // 保留中心化数据和主成分方向的绘制
            this.drawPrincipalComponents(g, width, height);

            // 突出显示第一主成分
            const scaleFactor = Math.sqrt(
                d3.max([...this.centeredData.map(d => Math.abs(d[0])), ...this.centeredData.map(d => Math.abs(d[1]))])
            ) * 1.5;

            // 高亮第一主成分
            g.append("line")
                .attr("x1", this.xScale(-this.eigenvectors[0][0] * scaleFactor))
                .attr("y1", this.yScale(-this.eigenvectors[0][1] * scaleFactor))
                .attr("x2", this.xScale(this.eigenvectors[0][0] * scaleFactor))
                .attr("y2", this.yScale(this.eigenvectors[0][1] * scaleFactor))
                .style("stroke", "red")
                .style("stroke-width", 4);

            // 添加选择指示
            g.append("text")
                .attr("x", width / 2)
                .attr("y", height - 20)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("font-weight", "bold")
                .style("fill", "red")
                .text("选择第一主成分进行降维");
        },

        drawProjection(g, width, height) {
            // 保留中心化数据和主成分方向的绘制
            this.drawSelectedComponent(g, width, height);

            // 绘制投影线段和投影点
            g.selectAll(".projection-line")
                .data(this.projectedData)
                .enter()
                .append("line")
                .attr("class", "projection-line")
                .attr("x1", d => this.xScale(d.original[0]))
                .attr("y1", d => this.yScale(d.original[1]))
                .attr("x2", d => this.xScale(d.projected[0]))
                .attr("y2", d => this.yScale(d.projected[1]))
                .style("stroke", "#999")
                .style("stroke-width", 1)
                .style("stroke-dasharray", "3,3");

            // 绘制投影后的点
            g.selectAll(".projected-point")
                .data(this.projectedData)
                .enter()
                .append("circle")
                .attr("class", "projected-point")
                .attr("cx", d => this.xScale(d.projected[0]))
                .attr("cy", d => this.yScale(d.projected[1]))
                .attr("r", 5)
                .style("fill", "#ff7f0e")
                .style("opacity", 0.7);

            // 添加一维表示
            const oneDScale = d3.scaleLinear()
                .domain(d3.extent(this.projectedData, d => d.value))
                .range([0, width * 0.7]);

            const oneDAxis = g.append("g")
                .attr("transform", `translate(${width * 0.15},${height - 60})`);

            // 绘制1D轴
            oneDAxis.append("line")
                .attr("x1", 0)
                .attr("y1", 0)
                .attr("x2", width * 0.7)
                .attr("y2", 0)
                .style("stroke", "black")
                .style("stroke-width", 2);

            // 添加刻度
            oneDAxis.call(d3.axisBottom(oneDScale));

            // 绘制投影到1D的点
            oneDAxis.selectAll(".oneD-point")
                .data(this.projectedData)
                .enter()
                .append("circle")
                .attr("class", "oneD-point")
                .attr("cx", d => oneDScale(d.value))
                .attr("cy", 0)
                .attr("r", 5)
                .style("fill", "#ff7f0e")
                .style("opacity", 0.7);

            // 添加说明
            oneDAxis.append("text")
                .attr("x", width * 0.35)
                .attr("y", -30)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text("降维后的一维数据表示");
        },

        startDemo() {
            if (this.isPlaying) return;

            this.isPlaying = true;

            // 如果演示已经完成，则重置
            if (this.currentStep >= this.demoSteps.length) {
                this.resetDemo();
            }

            // 创建定时器，自动播放演示
            this.demoInterval = setInterval(() => {
                if (this.currentStep < this.demoSteps.length - 1) {
                    this.currentStep++;
                    this.drawStep(this.currentStep);
                } else {
                    // 演示完成，停止定时器
                    this.currentStep = this.demoSteps.length;
                    clearInterval(this.demoInterval);
                    this.isPlaying = false;
                }
            }, this.stepDuration);
        },

        pauseDemo() {
            if (!this.isPlaying) return;

            clearInterval(this.demoInterval);
            this.isPlaying = false;
        },

        resetDemo() {
            // 停止定时器
            if (this.demoInterval) {
                clearInterval(this.demoInterval);
            }

            // 重置状态
            this.currentStep = 0;
            this.isPlaying = false;

            // 重新绘制第一步
            this.drawStep(0);
        },

        initSortingQuestion() {
            // 初始化排序题的步骤，随机打乱顺序
            this.userSortedSteps = [...this.correctStepOrder]
                .map(a => ({ ...a }))
                .sort(() => Math.random() - 0.5);
        },

        moveStep(index, direction) {
            // 交换元素位置
            if (
                (direction === -1 && index > 0) ||
                (direction === 1 && index < this.userSortedSteps.length - 1)
            ) {
                const temp = this.userSortedSteps[index];
                this.$set(this.userSortedSteps, index, this.userSortedSteps[index + direction]);
                this.$set(this.userSortedSteps, index + direction, temp);
            }
        },

        checkStepOrder() {
            this.orderAttempts++;

            // 检查用户排序是否正确
            let isCorrect = true;
            for (let i = 0; i < this.correctStepOrder.length; i++) {
                if (this.userSortedSteps[i].text !== this.correctStepOrder[i].text) {
                    isCorrect = false;
                    break;
                }
            }

            if (isCorrect) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "步骤顺序正确！",
                    "您已正确排列了PCA降维的完整计算步骤。这些步骤构成了PCA算法的核心流程：从数据预处理到最终降维。",
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.orderAttempts >= 2) {
                    hint = "提示：回顾演示中的各个步骤。PCA的第一步是对数据进行什么处理？之后如何计算数据分布特性？";
                }

                this.$refs.baseSegment.showResponse(
                    "步骤顺序不正确",
                    `请仔细思考PCA降维的流程，重新排列步骤。${hint}`,
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
        // 初始化演示
        this.$nextTick(() => {
            this.initDemo();
        });
    },
    beforeDestroy() {
        // 清理资源
        if (this.demoInterval) {
            clearInterval(this.demoInterval);
        }

        if (this.svg) {
            d3.select(this.$refs.processVisualization).selectAll("*").remove();
        }
    }
}
</script>

<style scoped>
.dim-reduction-interactive {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.process-controls {
    margin-bottom: 20px;
}

.process-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
}

.step-display {
    margin: 20px 0;
}

.visualization-container {
    width: 100%;
    height: 500px;
    margin: 20px 0;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    display: flex;
    justify-content: center;
}

.step-description {
    margin: 15px 0;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    border-left: 4px solid #409EFF;
}

.understanding-check {
    margin-top: 30px;
    padding: 15px;
    background-color: #ecf5ff;
    border-radius: 4px;
}

.sortable-container {
    margin: 20px 0;
}

.sort-item {
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.step-content {
    display: flex;
    align-items: center;
    gap: 10px;
}

.step-number {
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

.step-controls {
    display: flex;
    gap: 5px;
}

.check-order-button {
    margin-top: 20px;
}

/* D3可视化样式 */
:deep(.x-axis) path,
:deep(.y-axis) path {
    stroke: #888;
}

:deep(.x-axis) text,
:deep(.y-axis) text {
    fill: #555;
    font-size: 12px;
}
</style>