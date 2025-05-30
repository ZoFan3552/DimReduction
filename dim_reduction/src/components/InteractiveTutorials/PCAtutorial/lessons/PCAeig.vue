<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="eigenvalues-interactive">
                <h3>特征向量与特征值可视化</h3>
                <p>这个交互式演示帮助您理解特征向量和特征值与数据分布的关系。</p>

                <div class="matrix-input-section">
                    <h4>选择一个预设的协方差矩阵</h4>
                    <el-radio-group v-model="selectedMatrix" @change="updateVisualization">
                        <el-radio :label="0">矩阵A: 主要沿X轴分布</el-radio>
                        <el-radio :label="1">矩阵B: 主要沿Y轴分布</el-radio>
                        <el-radio :label="2">矩阵C: 沿对角线分布(正相关)</el-radio>
                        <el-radio :label="3">矩阵D: 沿反对角线分布(负相关)</el-radio>
                    </el-radio-group>

                    <div class="matrix-display">
                        <h4>当前协方差矩阵</h4>
                        <div class="matrix-container">
                            <div class="matrix-bracket matrix-left-bracket"></div>
                            <div class="matrix-content">
                                <div class="matrix-row">
                                    <span class="matrix-element">{{ currentMatrix[0][0].toFixed(2) }}</span>
                                    <span class="matrix-element">{{ currentMatrix[0][1].toFixed(2) }}</span>
                                </div>
                                <div class="matrix-row">
                                    <span class="matrix-element">{{ currentMatrix[1][0].toFixed(2) }}</span>
                                    <span class="matrix-element">{{ currentMatrix[1][1].toFixed(2) }}</span>
                                </div>
                            </div>
                            <div class="matrix-bracket matrix-right-bracket"></div>
                        </div>
                    </div>
                </div>

                <div class="visualization-section">
                    <div class="visualization-container" ref="eigenVisualization"></div>

                    <div class="eigen-results">
                        <h4>特征值和特征向量</h4>
                        <div class="eigen-display">
                            <div class="eigen-item">
                                <p><strong>第一特征值(λ₁):</strong> {{ eigenvalues[0].toFixed(4) }}</p>
                                <p><strong>第一特征向量:</strong> [{{ eigenvectors[0][0].toFixed(4) }}, {{
                                    eigenvectors[0][1].toFixed(4) }}]</p>
                            </div>
                            <div class="eigen-item">
                                <p><strong>第二特征值(λ₂):</strong> {{ eigenvalues[1].toFixed(4) }}</p>
                                <p><strong>第二特征向量:</strong> [{{ eigenvectors[1][0].toFixed(4) }}, {{
                                    eigenvectors[1][1].toFixed(4) }}]</p>
                            </div>
                        </div>

                        <div class="eigen-explanation">
                            <p class="eigen-ratio">信息保留比: λ₁/(λ₁+λ₂) = {{ (eigenvalues[0] / (eigenvalues[0] +
                                eigenvalues[1]) * 100).toFixed(2) }}%</p>
                            <p>这表示第一主成分包含了上述百分比的数据方差信息。</p>
                        </div>
                    </div>
                </div>

                <div class="understanding-check">
                    <h4>理解检查</h4>
                    <p>根据您的观察，下列哪项关于特征向量和特征值的描述是正确的？</p>

                    <el-checkbox-group v-model="checkedUnderstandings" class="understanding-options">
                        <el-checkbox :label="0">特征向量总是指向数据分布的主要方向</el-checkbox>
                        <el-checkbox :label="1">特征值的大小与数据在该方向上的方差成正比</el-checkbox>
                        <el-checkbox :label="2">PCA中，不同的特征向量总是相互正交（垂直）</el-checkbox>
                        <el-checkbox :label="3">协方差矩阵的对角元素等于沿特征向量方向的方差</el-checkbox>
                    </el-checkbox-group>

                    <el-button type="primary" @click="checkUnderstanding" :disabled="checkedUnderstandings.length === 0"
                        class="understanding-submit">
                        提交答案
                    </el-button>
                </div>
            </div>
        </template>
    </base-segment>
</template>

<script>
import BaseSegment from './BaseSegment.vue'
import * as d3 from 'd3'
import * as math from 'mathjs'

export default {
    name: 'EigenvectorsAndValues',
    components: {
        BaseSegment
    },
    props: {
        savedAnswer: {
            type: String,
            default: null
        }
    },
    watch: {
        // 监听savedAnswer属性的变化
        savedAnswer: {
            immediate: true,
            handler(newValue) {
                console.log("特征值特征向量子组件接受回答", newValue);
                if (newValue) {
                    this.checkedUnderstandings = JSON.parse(newValue);
                    //   this.hasSubmittedAnswer = true;
                    //   this.feedback = '您之前已经完成了这个章节的练习。';
                }
            }
        }
    },
    data() {
        return {
            title: '4. 特征向量与特征值',
            segmentId: 'eigenvectors',
            content: `
  ## 特征向量和特征值：PCA的核心组件
  
  在PCA中，**特征向量**和**特征值**是理解和实现算法的核心概念。它们提供了数据主要变化方向和各方向上信息量的指标。
  
  ### 特征向量与特征值的定义
  
  对于一个方阵 $A$，如果存在非零向量 $v$ 和标量 $\\lambda$ 满足：
  
  $$A v = \\lambda v$$
  
  则 $v$ 被称为矩阵 $A$ 的**特征向量**，对应的 $\\lambda$ 被称为**特征值**。
  
  在PCA中，我们关注的是数据协方差矩阵的特征向量和特征值。
  
  ### 特征向量在PCA中的几何意义
  
  特征向量表示数据分布的主要方向。第一特征向量（对应最大特征值的向量）指向数据方差最大的方向，第二特征向量指向与第一特征向量正交且方差最大的方向，依此类推。
  
  
  ### 特征值的意义
  
  特征值表示数据沿着对应特征向量方向的方差大小。特征值越大，表示该方向上的数据变化越显著，包含的信息量越大。
  
  特征值可以用来确定需要保留的主成分数量。通常的做法是：
  1. 计算所有特征值的总和
  2. 计算每个特征值占总和的比例
  3. 选择能解释足够数据方差（如95%）的前几个主成分
  
  ### 特征向量的正交性
  
  协方差矩阵是对称的，其特征向量具有以下重要性质：
  - 不同特征值对应的特征向量相互正交
  - 可以将特征向量标准化为单位长度
  
  这些性质使得PCA中的主成分转换成为一个正交变换，保证了变换后的各个维度是不相关的。
  
  在下面的互动演示中，您可以观察不同协方差矩阵的特征向量和特征值，以及它们与数据分布的关系。
        `,
            // 协方差矩阵预设
            matricesPresets: [
                [[3.0, 0.5], [0.5, 1.0]],  // 主要沿X轴分布
                [[1.0, 0.5], [0.5, 3.0]],  // 主要沿Y轴分布
                [[2.0, 1.5], [1.5, 2.0]],  // 沿对角线分布(正相关)
                [[2.0, -1.5], [-1.5, 2.0]]  // 沿反对角线分布(负相关)
            ],
            selectedMatrix: 0,
            currentMatrix: [[3.0, 0.5], [0.5, 1.0]],

            // 特征值和特征向量
            eigenvalues: [0, 0],
            eigenvectors: [[0, 0], [0, 0]],

            // 可视化
            svg: null,
            width: 500,
            height: 400,
            margin: { top: 30, right: 30, bottom: 40, left: 40 },
            points: [],

            // 理解检查
            checkedUnderstandings: [],
            understandingAttempts: 0
        };
    },
    methods: {
        updateVisualization() {
            // 更新当前矩阵
            this.currentMatrix = this.matricesPresets[this.selectedMatrix];

            // 计算特征值和特征向量
            this.calculateEigenDecomposition();

            // 生成数据点
            this.generateDataPoints();

            // 更新可视化
            this.$nextTick(() => {
                this.drawVisualization();
            });
        },

        calculateEigenDecomposition() {
            try {
                const matrix = math.matrix(this.currentMatrix);
                const eig = math.eigs(matrix);

                // 1. 兼容性提取特征值和特征向量
                const values = eig.values.toArray ? eig.values.toArray() : Array.isArray(eig.values) ? eig.values : [];

                const rawVectors = eig.eigenvectors || eig.vectors;
                let vectors;

                // 提取特征向量并转换为数组
                if (Array.isArray(rawVectors)) {
                    vectors = rawVectors.map(item => item.vector.toArray ? item.vector.toArray() : []);
                } else {
                    // 如果没有特征向量，可以使用默认值
                    vectors = [[1, 0], [0, 1]];
                }

                // 2. 安全提取实部
                const getRealPart = val => {
                    if (typeof val === 'number') return val;
                    if (val && typeof val.re === 'number') return val.re;
                    if (math.isComplex(val)) return math.re(val);
                    return 0; // 默认值
                };

                // 3. 处理结果
                this.eigenvalues = [
                    getRealPart(values[0]),
                    getRealPart(values[1])
                ];

                this.eigenvectors = [
                    [
                        getRealPart(vectors[0][0]),
                        getRealPart(vectors[1][0])
                    ],
                    [
                        getRealPart(vectors[0][1]),
                        getRealPart(vectors[1][1])
                    ]
                ];

                // 4. 排序和标准化
                if (this.eigenvalues[0] < this.eigenvalues[1]) {
                    [this.eigenvalues[0], this.eigenvalues[1]] = [this.eigenvalues[1], this.eigenvalues[0]];
                    [this.eigenvectors[0], this.eigenvectors[1]] = [this.eigenvectors[1], this.eigenvectors[0]];
                }

                // 标准化特征向量
                this.eigenvectors = this.eigenvectors.map(vec => {
                    const [x, y] = vec;
                    const mag = Math.sqrt(x * x + y * y);
                    return mag > 0 ? [x / mag, y / mag] : [x, y];
                });

            } catch (e) {
                console.error("特征分解错误:", e);
                // 安全默认值
                this.eigenvalues = [1, 0];
                this.eigenvectors = [[1, 0], [0, 1]];
            }
        }
        ,


        generateDataPoints() {
            this.points = [];
            const numPoints = 200;
            const mean = [0, 0];

            try {
                // 方案1：优先使用math.js的Cholesky分解（如果可用）
                let L;
                if (typeof math.cholesky === 'function') {
                    L = math.cholesky(math.matrix(this.currentMatrix)).toArray();
                }
                // 方案2：手动实现Cholesky分解（2x2矩阵特化）
                else {
                    // eslint-disable-next-line
                    const [[a, b], [c, d]] = this.currentMatrix;
                    const l11 = Math.sqrt(a);
                    const l21 = b / l11;
                    const l22 = Math.sqrt(d - l21 * l21);
                    L = [[l11, 0], [l21, l22]];
                }

                // 生成数据点
                for (let i = 0; i < numPoints; i++) {
                    const z1 = this.randomNormal();
                    const z2 = this.randomNormal();

                    const x = mean[0] + L[0][0] * z1 + L[0][1] * z2;
                    const y = mean[1] + L[1][0] * z1 + L[1][1] * z2;

                    this.points.push([x, y]);
                }

            } catch (e) {
                console.error("生成数据点时出错:", e);

                // 方案3：基于特征分解的备选方案
                const generateFromEigen = () => {
                    const points = [];
                    for (let i = 0; i < numPoints; i++) {
                        const r1 = this.randomNormal() * Math.sqrt(this.eigenvalues[0]);
                        const r2 = this.randomNormal() * Math.sqrt(this.eigenvalues[1]);

                        const x = mean[0] + r1 * this.eigenvectors[0][0] + r2 * this.eigenvectors[1][0];
                        const y = mean[1] + r1 * this.eigenvectors[0][1] + r2 * this.eigenvectors[1][1];

                        points.push([x, y]);
                    }
                    return points;
                };

                this.points = generateFromEigen();
            }
        },

        randomNormal() {
            // Box-Muller变换生成标准正态分布随机数
            const u1 = Math.random();
            const u2 = Math.random();

            return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        },

        drawVisualization() {
            // 清除之前的可视化
            d3.select(this.$refs.eigenVisualization).selectAll("*").remove();

            // 设置SVG
            this.svg = d3.select(this.$refs.eigenVisualization)
                .append("svg")
                .attr("width", this.width)
                .attr("height", this.height);

            const g = this.svg.append("g")
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

            // 实际绘图区域尺寸
            const plotWidth = this.width - this.margin.left - this.margin.right;
            const plotHeight = this.height - this.margin.top - this.margin.bottom;

            // 计算数据范围
            const xExtent = d3.extent(this.points, d => d[0]);
            const yExtent = d3.extent(this.points, d => d[1]);

            // 确保比例尺是对称的，并添加一些边距
            const maxX = Math.max(Math.abs(xExtent[0]), Math.abs(xExtent[1])) * 1.2;
            const maxY = Math.max(Math.abs(yExtent[0]), Math.abs(yExtent[1])) * 1.2;

            // 创建X和Y比例尺
            const xScale = d3.scaleLinear()
                .domain([-maxX, maxX])
                .range([0, plotWidth]);

            const yScale = d3.scaleLinear()
                .domain([-maxY, maxY])
                .range([plotHeight, 0]);

            // 添加X和Y轴
            g.append("g")
                .attr("transform", `translate(0,${yScale(0)})`)
                .call(d3.axisBottom(xScale).ticks(5));

            g.append("g")
                .attr("transform", `translate(${xScale(0)},0)`)
                .call(d3.axisLeft(yScale).ticks(5));

            // 绘制数据点
            g.selectAll(".data-point")
                .data(this.points)
                .enter()
                .append("circle")
                .attr("class", "data-point")
                .attr("cx", d => xScale(d[0]))
                .attr("cy", d => yScale(d[1]))
                .attr("r", 2)
                .style("fill", "#69b3a2")
                .style("opacity", 0.5);

            // 绘制特征向量
            const origin = [0, 0];
            const scaleFactor = Math.max(maxX, maxY) * 0.7;

            // 第一特征向量（红色）
            const ev1End = [
                origin[0] + this.eigenvectors[0][0] * scaleFactor * Math.sqrt(this.eigenvalues[0]),
                origin[1] + this.eigenvectors[0][1] * scaleFactor * Math.sqrt(this.eigenvalues[0])
            ];

            g.append("line")
                .attr("x1", xScale(origin[0]))
                .attr("y1", yScale(origin[1]))
                .attr("x2", xScale(ev1End[0]))
                .attr("y2", yScale(ev1End[1]))
                .style("stroke", "red")
                .style("stroke-width", 2)
                .style("stroke-dasharray", "5,5");

            // 第二特征向量（蓝色）
            const ev2End = [
                origin[0] + this.eigenvectors[1][0] * scaleFactor * Math.sqrt(this.eigenvalues[1]),
                origin[1] + this.eigenvectors[1][1] * scaleFactor * Math.sqrt(this.eigenvalues[1])
            ];

            g.append("line")
                .attr("x1", xScale(origin[0]))
                .attr("y1", yScale(origin[1]))
                .attr("x2", xScale(ev2End[0]))
                .attr("y2", yScale(ev2End[1]))
                .style("stroke", "blue")
                .style("stroke-width", 2)
                .style("stroke-dasharray", "5,5");

            // 添加标签
            g.append("text")
                .attr("x", xScale(ev1End[0]))
                .attr("y", yScale(ev1End[1]))
                .attr("dx", 5)
                .style("fill", "red")
                .text("第一特征向量 (λ₁)");

            g.append("text")
                .attr("x", xScale(ev2End[0]))
                .attr("y", yScale(ev2End[1]))
                .attr("dx", 5)
                .style("fill", "blue")
                .text("第二特征向量 (λ₂)");

            // 绘制椭圆表示数据分布
            const confidenceEllipse = this.calculateConfidenceEllipse(1.5);

            // 创建椭圆路径
            const ellipsePath = d3.line()
                .x(d => xScale(d[0]))
                .y(d => yScale(d[1]))
                .curve(d3.curveCardinalClosed);

            g.append("path")
                .attr("d", ellipsePath(confidenceEllipse))
                .style("stroke", "#333")
                .style("stroke-width", 1)
                .style("fill", "none")
                .style("stroke-dasharray", "3,3");
        },

        calculateConfidenceEllipse(scale = 1) {
            // 计算置信椭圆上的点
            const points = [];
            const steps = 100;
            const angle = 2 * Math.PI / steps;

            for (let i = 0; i < steps; i++) {
                const theta = i * angle;
                const x = scale * Math.sqrt(this.eigenvalues[0]) * Math.cos(theta);
                const y = scale * Math.sqrt(this.eigenvalues[1]) * Math.sin(theta);

                // 旋转到特征向量坐标系
                const rotatedX = x * this.eigenvectors[0][0] + y * this.eigenvectors[1][0];
                const rotatedY = x * this.eigenvectors[0][1] + y * this.eigenvectors[1][1];

                points.push([rotatedX, rotatedY]);
            }

            return points;
        },

        checkUnderstanding() {
            this.understandingAttempts++;

            // 正确答案是选项1和2
            const correctAnswers = [1, 2];
            const userAnswers = this.checkedUnderstandings.sort();

            // 向父组件发送答案提交事件
            this.$emit('answer-submitted', JSON.stringify(userAnswers));

            // 检查答案是否相同
            let isCorrect = correctAnswers.length === userAnswers.length;
            if (isCorrect) {
                for (let i = 0; i < correctAnswers.length; i++) {
                    if (correctAnswers[i] !== userAnswers[i]) {
                        isCorrect = false;
                        break;
                    }
                }
            }

            if (isCorrect) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "回答正确！",
                    "您选择了正确的答案：特征值的大小与数据在该方向上的方差成正比，且PCA中的特征向量总是相互正交。这两个性质是PCA算法的核心基础。",
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.understandingAttempts >= 2) {
                    hint = "提示：考虑我们刚刚演示的可视化，观察特征向量的方向和特征值的大小。同时，想想协方差矩阵的对角元素是否等于特征值？";
                }

                this.$refs.baseSegment.showResponse(
                    "回答不正确",
                    `请再思考特征向量和特征值的性质。正确答案有两项。${hint}`,
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
            this.updateVisualization();
        });
    },
    beforeDestroy() {
        // 清理D3资源
        if (this.svg) {
            d3.select(this.$refs.eigenVisualization).selectAll("*").remove();
        }
    }
}
</script>

<style scoped>
.eigenvalues-interactive {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.matrix-input-section {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.matrix-display {
    margin-top: 15px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.matrix-container {
    display: flex;
    align-items: center;
    margin: 10px 0;
}

.matrix-bracket {
    width: 10px;
    height: 80px;
    position: relative;
}

.matrix-left-bracket::before,
.matrix-left-bracket::after,
.matrix-right-bracket::before,
.matrix-right-bracket::after {
    content: "";
    position: absolute;
    width: 10px;
    height: 10px;
    border: 2px solid #333;
}

.matrix-left-bracket::before {
    top: 0;
    left: 0;
    border-right: none;
    border-bottom: none;
}

.matrix-left-bracket::after {
    bottom: 0;
    left: 0;
    border-right: none;
    border-top: none;
}

.matrix-right-bracket::before {
    top: 0;
    right: 0;
    border-left: none;
    border-bottom: none;
}

.matrix-right-bracket::after {
    bottom: 0;
    right: 0;
    border-left: none;
    border-top: none;
}

.matrix-content {
    padding: 0 10px;
}

.matrix-row {
    display: flex;
    justify-content: center;
    margin: 10px 0;
}

.matrix-element {
    width: 60px;
    text-align: center;
    font-weight: bold;
}

.visualization-section {
    margin: 20px 0;
}

.visualization-container {
    width: 100%;
    height: 400px;
    margin: 10px 0 20px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    display: flex;
    justify-content: center;
}

.eigen-results {
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    margin-bottom: 20px;
}

.eigen-display {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 10px 0;
}

.eigen-item {
    flex: 1;
    min-width: 200px;
    padding: 10px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.eigen-explanation {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px dashed #dcdfe6;
}

.eigen-ratio {
    font-weight: bold;
    color: #409EFF;
}

.understanding-check {
    margin-top: 20px;
    padding: 15px;
    background-color: #ecf5ff;
    border-radius: 4px;
    border-left: 4px solid #409eff;
}

.understanding-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 15px 0;
}

.understanding-submit {
    margin-top: 15px;
}
</style>