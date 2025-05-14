<!-- BetweenClassScatterMatrix.vue - 类间散布矩阵教学组件 -->
<template>
    <div class="tutorial-section" :id="sectionId">
        <div class="section-header">
            <h2 class="section-title">{{ title }}</h2>
            <div class="section-progress">
                <el-tag v-if="isCompleted" type="success" effect="dark">已完成</el-tag>
                <el-tag v-else type="info" effect="plain">进行中</el-tag>
                <div class="section-number">{{ sectionIndex }}/{{ totalSections }}</div>
            </div>
        </div>

        <!-- 教学内容展示区 -->
        <div class="content-area">
            <div class="markdown-content" v-html="compiledMarkdown"></div>
        </div>

        <!-- 互动区域 - 类间散布矩阵可视化 -->
        <div class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-data-analysis"></i> 互动练习：探索类间散布矩阵
            </h3>

            <p class="interaction-description">
                调整下方的类别中心位置，观察类间散布矩阵的变化。尝试理解类间散布矩阵是如何度量不同类别之间分离程度的。
            </p>

            <div class="visualization-container">
                <div id="between-class-viz" ref="d3Container"></div>

                <div class="viz-controls">
                    <div class="control-group">
                        <span class="control-label">类别1中心 X:</span>
                        <el-slider v-model="class1MeanX" :min="0" :max="10" :step="0.5" @change="updateVisualization"
                            style="width: 100%;"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别1中心 Y:</span>
                        <el-slider v-model="class1MeanY" :min="0" :max="10" :step="0.5" @change="updateVisualization"
                            style="width: 100%;"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别2中心 X:</span>
                        <el-slider v-model="class2MeanX" :min="0" :max="10" :step="0.5" @change="updateVisualization"
                            style="width: 100%;"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别2中心 Y:</span>
                        <el-slider v-model="class2MeanY" :min="0" :max="10" :step="0.5" @change="updateVisualization"
                            style="width: 100%;"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别3中心 X:</span>
                        <el-slider v-model="class3MeanX" :min="0" :max="10" :step="0.5" @change="updateVisualization"
                            style="width: 100%;"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别3中心 Y:</span>
                        <el-slider v-model="class3MeanY" :min="0" :max="10" :step="0.5" @change="updateVisualization"
                            style="width: 100%;"></el-slider>
                    </div>

                    <div class="matrix-display">
                        <h4>类间散布矩阵 S<sub>B</sub>:</h4>
                        <div class="matrix">
                            <div class="matrix-row">
                                <div class="matrix-cell">{{ formatNumber(betweenClassMatrix[0][0]) }}</div>
                                <div class="matrix-cell">{{ formatNumber(betweenClassMatrix[0][1]) }}</div>
                            </div>
                            <div class="matrix-row">
                                <div class="matrix-cell">{{ formatNumber(betweenClassMatrix[1][0]) }}</div>
                                <div class="matrix-cell">{{ formatNumber(betweenClassMatrix[1][1]) }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="data-info">
                        <h4>几何意义说明:</h4>
                        <p>
                            <span class="dot" style="background-color: #409EFF;"></span> 类别1中心 ({{
                                formatNumber(class1MeanX) }}, {{ formatNumber(class1MeanY) }})
                        </p>
                        <p>
                            <span class="dot" style="background-color: #E6A23C;"></span> 类别2中心 ({{
                                formatNumber(class2MeanX) }}, {{ formatNumber(class2MeanY) }})
                        </p>
                        <p>
                            <span class="dot" style="background-color: #F56C6C;"></span> 类别3中心 ({{
                                formatNumber(class3MeanX) }}, {{ formatNumber(class3MeanY) }})
                        </p>
                        <p>
                            <span class="dot" style="background-color: #909399;"></span> 全局均值 ({{
                                formatNumber(globalMean[0]) }}, {{ formatNumber(globalMean[1]) }})
                        </p>
                        <p>
                            <span class="ellipse-marker" style="border-color: #67C23A;"></span> 类间散布椭圆
                        </p>
                    </div>
                </div>
            </div>

            <div class="interactive-quiz">
                <h4>根据你的观察回答以下问题:</h4>

                <p class="question">当类别中心相距更远时，类间散布矩阵有什么变化？</p>

                <el-radio-group v-model="quizAnswer">
                    <el-radio :label="0">类间散布矩阵的特征值变小，椭圆变小</el-radio>
                    <el-radio :label="1">类间散布矩阵的特征值变大，椭圆变大</el-radio>
                    <el-radio :label="2">类间散布矩阵不受类别中心距离影响</el-radio>
                </el-radio-group>

                <div class="quiz-actions">
                    <el-button type="primary" @click="checkAnswer" :disabled="quizAnswer === null || quizChecked">
                        提交答案
                    </el-button>

                    <el-button type="success" @click="completeSection" v-if="quizCorrect">
                        继续学习 <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
        </div>

        <!-- 回应区域 -->
        <div v-if="showResponse" class="response-area">
            <div class="response-content">
                <i :class="['response-icon', responseIconClass]"></i>
                <div class="response-message" v-html="compiledResponse"></div>
            </div>
        </div>

        <div v-if="isCompleted" class="completed-message">
            <i class="el-icon-circle-check"></i>
            <span>此部分已完成！</span>
            <el-button v-if="hasNext" type="text" @click="navigateToNext">
                前往下一部分 <i class="el-icon-arrow-right"></i>
            </el-button>
        </div>

        <el-divider></el-divider>
    </div>
</template>

<script>
import { marked } from 'marked';
import 'katex/dist/katex.min.css';
import katex from 'katex';
import * as d3 from 'd3';

// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}

export default {
    name: 'BetweenClassScatterMatrix',
    props: {
        sectionId: {
            type: String,
            default: 'between-class-scatter'
        },
        sectionIndex: {
            type: Number,
            required: true
        },
        totalSections: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            title: "类间散布矩阵",
            markdownContent: `
# 类间散布矩阵 (Between-Class Scatter Matrix)

类间散布矩阵是LDA算法的另一个核心概念，它度量了不同类别之间的分离程度。

## 数学定义

类间散布矩阵 $S_B$ 定义为：

$$
S_B = \\sum_{c=1}^{k} n_c (\\mu_c - \\mu)(\\mu_c - \\mu)^T
$$

其中：
- $k$ 是类别数量
- $n_c$ 是类别 $c$ 中的样本数量
- $\\mu_c$ 是类别 $c$ 的均值向量
- $\\mu$ 是全局均值向量，即所有样本的均值

## 几何意义

类间散布矩阵 $S_B$ 反映了不同类别中心之间的距离。从几何角度看，它度量了各个类别均值相对于全局均值的分散程度，加权考虑了每个类别的样本数量。

对于两个类别的简单情况，$S_B$ 可以简化为：

$$
S_B = \\frac{n_1 n_2}{n_1 + n_2} (\\mu_1 - \\mu_2)(\\mu_1 - \\mu_2)^T
$$

这表明类间散布矩阵与两个类别均值之间的距离平方成正比。

## 类间散布矩阵的特性

类间散布矩阵 $S_B$ 有以下重要特性：

1. $S_B$ 是一个对称半正定矩阵
2. $S_B$ 的秩最大为 $k-1$，其中 $k$ 是类别数
3. 当类别数为2时，$S_B$ 的秩为1，意味着最优投影空间是一维的
4. $S_B$ 的特征向量指向类别均值差异最大的方向

## 类间散布矩阵在LDA中的作用

在LDA中，我们希望最大化类间散度，即希望不同类别的样本在投影后尽可能分开。这意味着我们希望投影后的类别中心之间的距离尽可能大。

投影后的类间散度可以表示为：

$$
w^T S_B w
$$

其中 $w$ 是投影方向。

LDA寻找的是最大化 $w^T S_B w$ 同时最小化 $w^T S_W w$ 的投影方向，即最大化：

$$
J(w) = \\frac{w^T S_B w}{w^T S_W w}
$$

在下面的互动练习中，你可以调整不同类别的中心位置，观察它们对类间散布矩阵的影响，以及这如何影响LDA的分类性能。
      `,

            isCompleted: false,

            // D3可视化数据
            svg: null,
            width: 600,
            height: 400,
            margin: { top: 30, right: 30, bottom: 30, left: 40 },

            // 可调整参数
            class1MeanX: 2.5,
            class1MeanY: 2.5,
            class2MeanX: 7.5,
            class2MeanY: 2.5,
            class3MeanX: 5.0,
            class3MeanY: 7.5,

            // 计算结果
            betweenClassMatrix: [[0.0, 0.0], [0.0, 0.0]],
            globalMean: [5.0, 4.17],
            class1Samples: [],
            class2Samples: [],
            class3Samples: [],

            // 问题回答
            quizAnswer: null,
            quizChecked: false,
            quizCorrect: false,

            // 回应部分数据
            showResponse: false,
            response: ''
        }
    },
    computed: {
        compiledMarkdown() {
            const withMath = renderMath(this.markdownContent);
            return marked(withMath);
        },
        compiledResponse() {
            const withMath = renderMath(this.response);
            return marked(withMath);
        },
        responseIconClass() {
            return this.quizCorrect ? 'el-icon-check correct' : 'el-icon-close incorrect';
        },
        hasNext() {
            return this.sectionIndex < this.totalSections;
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const completedSections = this.getCompletedSections();
        this.isCompleted = completedSections.includes(this.sectionId);

        if (!this.isCompleted) {
            // 初始化D3可视化
            this.$nextTick(() => {
                this.initVisualization();
            });
        }
    },
    methods: {
        formatNumber(num) {
            return num.toFixed(2);
        },

        initVisualization() {
            const containerWidth = this.$refs.d3Container.clientWidth || this.width;
            const width = containerWidth - this.margin.left - this.margin.right;
            const height = this.height - this.margin.top - this.margin.bottom;

            // 创建SVG容器
            this.svg = d3.select("#between-class-viz")
                .append("svg")
                .attr("width", containerWidth)
                .attr("height", this.height)
                .append("g")
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

            // 初始化坐标系
            const xScale = d3.scaleLinear()
                .domain([0, 10])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([0, 10])
                .range([height, 0]);

            // 添加X和Y轴
            this.svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", `translate(0,${height})`)
                .call(d3.axisBottom(xScale));

            this.svg.append("g")
                .attr("class", "y-axis")
                .call(d3.axisLeft(yScale));

            // 添加网格线
            this.svg.append("g")
                .attr("class", "grid-lines")
                .selectAll("line")
                .data(d3.range(0, 11, 1))
                .enter()
                .append("line")
                .attr("x1", d => xScale(d))
                .attr("y1", yScale(0))
                .attr("x2", d => xScale(d))
                .attr("y2", yScale(10))
                .attr("stroke", "#eee")
                .attr("stroke-width", 1);

            this.svg.append("g")
                .attr("class", "grid-lines")
                .selectAll("line")
                .data(d3.range(0, 11, 1))
                .enter()
                .append("line")
                .attr("x1", xScale(0))
                .attr("y1", d => yScale(d))
                .attr("x2", xScale(10))
                .attr("y2", d => yScale(d))
                .attr("stroke", "#eee")
                .attr("stroke-width", 1);

            // 生成初始数据
            this.generateData();

            // 绘制数据点和椭圆
            this.updateVisualization();
        },
        // 这是BetweenClassScatterMatrix.vue组件的方法部分

        // 将以下方法添加到BetweenClassScatterMatrix.vue组件的methods对象中

        generateData() {
            // 计算全局均值（所有类别均值的平均）
            this.globalMean = [
                (this.class1MeanX + this.class2MeanX + this.class3MeanX) / 3,
                (this.class1MeanY + this.class2MeanY + this.class3MeanY) / 3
            ];

            // 计算类间散布矩阵
            const calculateBetweenClassMatrix = () => {
                // 假设每个类别的样本数量相等
                const n1 = 1, n2 = 1, n3 = 1;
                // const totalSamples = n1 + n2 + n3;

                // 类别均值与全局均值的差
                const diff1 = [
                    this.class1MeanX - this.globalMean[0],
                    this.class1MeanY - this.globalMean[1]
                ];

                const diff2 = [
                    this.class2MeanX - this.globalMean[0],
                    this.class2MeanY - this.globalMean[1]
                ];

                const diff3 = [
                    this.class3MeanX - this.globalMean[0],
                    this.class3MeanY - this.globalMean[1]
                ];

                // 计算类间散布矩阵
                return [
                    [
                        n1 * diff1[0] * diff1[0] + n2 * diff2[0] * diff2[0] + n3 * diff3[0] * diff3[0],
                        n1 * diff1[0] * diff1[1] + n2 * diff2[0] * diff2[1] + n3 * diff3[0] * diff3[1]
                    ],
                    [
                        n1 * diff1[1] * diff1[0] + n2 * diff2[1] * diff2[0] + n3 * diff3[1] * diff3[0],
                        n1 * diff1[1] * diff1[1] + n2 * diff2[1] * diff2[1] + n3 * diff3[1] * diff3[1]
                    ]
                ];
            };

            this.betweenClassMatrix = calculateBetweenClassMatrix();

            // 为每个类别生成少量样本点用于可视化
            const generateSamples = (mean, n, variance) => {
                const samples = [];
                for (let i = 0; i < n; i++) {
                    samples.push([
                        mean[0] + (Math.random() - 0.5) * variance,
                        mean[1] + (Math.random() - 0.5) * variance
                    ]);
                }
                return samples;
            };

            this.class1Samples = generateSamples([this.class1MeanX, this.class1MeanY], 20, 1.0);
            this.class2Samples = generateSamples([this.class2MeanX, this.class2MeanY], 20, 1.0);
            this.class3Samples = generateSamples([this.class3MeanX, this.class3MeanY], 20, 1.0);
        },

        updateVisualization() {
            // 重新生成数据
            this.generateData();

            const containerWidth = this.$refs.d3Container.clientWidth || this.width;
            const width = containerWidth - this.margin.left - this.margin.right;
            const height = this.height - this.margin.top - this.margin.bottom;

            // 刷新坐标系
            const xScale = d3.scaleLinear()
                .domain([0, 10])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([0, 10])
                .range([height, 0]);

            // 移除已有的数据点和椭圆
            this.svg.selectAll(".data-point, .class-mean, .global-mean, .between-scatter-ellipse").remove();

            // 绘制类别1的数据点
            this.svg.selectAll(".class1-point")
                .data(this.class1Samples)
                .enter()
                .append("circle")
                .attr("class", "data-point class1-point")
                .attr("cx", d => xScale(d[0]))
                .attr("cy", d => yScale(d[1]))
                .attr("r", 3)
                .attr("fill", "#409EFF")
                .attr("opacity", 0.5);

            // 绘制类别2的数据点
            this.svg.selectAll(".class2-point")
                .data(this.class2Samples)
                .enter()
                .append("circle")
                .attr("class", "data-point class2-point")
                .attr("cx", d => xScale(d[0]))
                .attr("cy", d => yScale(d[1]))
                .attr("r", 3)
                .attr("fill", "#E6A23C")
                .attr("opacity", 0.5);

            // 绘制类别3的数据点
            this.svg.selectAll(".class3-point")
                .data(this.class3Samples)
                .enter()
                .append("circle")
                .attr("class", "data-point class3-point")
                .attr("cx", d => xScale(d[0]))
                .attr("cy", d => yScale(d[1]))
                .attr("r", 3)
                .attr("fill", "#F56C6C")
                .attr("opacity", 0.5);

            // 绘制类别1的中心
            this.svg.append("circle")
                .attr("class", "class-mean class1-mean")
                .attr("cx", xScale(this.class1MeanX))
                .attr("cy", yScale(this.class1MeanY))
                .attr("r", 6)
                .attr("fill", "#409EFF")
                .attr("stroke", "white")
                .attr("stroke-width", 2);

            // 绘制类别2的中心
            this.svg.append("circle")
                .attr("class", "class-mean class2-mean")
                .attr("cx", xScale(this.class2MeanX))
                .attr("cy", yScale(this.class2MeanY))
                .attr("r", 6)
                .attr("fill", "#E6A23C")
                .attr("stroke", "white")
                .attr("stroke-width", 2);

            // 绘制类别3的中心
            this.svg.append("circle")
                .attr("class", "class-mean class3-mean")
                .attr("cx", xScale(this.class3MeanX))
                .attr("cy", yScale(this.class3MeanY))
                .attr("r", 6)
                .attr("fill", "#F56C6C")
                .attr("stroke", "white")
                .attr("stroke-width", 2);

            // 绘制全局均值
            this.svg.append("circle")
                .attr("class", "global-mean")
                .attr("cx", xScale(this.globalMean[0]))
                .attr("cy", yScale(this.globalMean[1]))
                .attr("r", 8)
                .attr("fill", "#909399")
                .attr("stroke", "white")
                .attr("stroke-width", 2);

            // 从全局均值到各类别中心的连线
            this.svg.append("line")
                .attr("class", "between-scatter-ellipse")
                .attr("x1", xScale(this.globalMean[0]))
                .attr("y1", yScale(this.globalMean[1]))
                .attr("x2", xScale(this.class1MeanX))
                .attr("y2", yScale(this.class1MeanY))
                .attr("stroke", "#409EFF")
                .attr("stroke-width", 2)
                .attr("stroke-dasharray", "5,5");

            this.svg.append("line")
                .attr("class", "between-scatter-ellipse")
                .attr("x1", xScale(this.globalMean[0]))
                .attr("y1", yScale(this.globalMean[1]))
                .attr("x2", xScale(this.class2MeanX))
                .attr("y2", yScale(this.class2MeanY))
                .attr("stroke", "#E6A23C")
                .attr("stroke-width", 2)
                .attr("stroke-dasharray", "5,5");

            this.svg.append("line")
                .attr("class", "between-scatter-ellipse")
                .attr("x1", xScale(this.globalMean[0]))
                .attr("y1", yScale(this.globalMean[1]))
                .attr("x2", xScale(this.class3MeanX))
                .attr("y2", yScale(this.class3MeanY))
                .attr("stroke", "#F56C6C")
                .attr("stroke-width", 2)
                .attr("stroke-dasharray", "5,5");

            // 绘制类间散布矩阵的椭圆表示
            if (this.betweenClassMatrix[0][0] > 0 || this.betweenClassMatrix[1][1] > 0) {
                const [eigen, rotation] = this.eigenDecomposition(this.betweenClassMatrix);

                // 椭圆大小与特征值平方根成正比
                const width = 1.5 * Math.sqrt(eigen.values[0]);
                const height = 1.5 * Math.sqrt(eigen.values[1]);

                // 生成椭圆路径
                const arc = d3.arc()
                    .startAngle(0)
                    .endAngle(2 * Math.PI)
                    .innerRadius(0)
                    .outerRadius(1);

                const ellipsePath = d3.path();
                arc.context(ellipsePath)({
                    x: xScale(this.globalMean[0]),
                    y: yScale(this.globalMean[1]),
                    // 调整半径模拟椭圆
                    r: Math.max(width * (xScale(1) - xScale(0)), height * (yScale(0) - yScale(1))),
                    // 可选：旋转
                    rotation: rotation
                });


                // 添加椭圆到SVG
                this.svg.append("path")
                    .attr("class", "between-scatter-ellipse")
                    .attr("d", ellipsePath.toString())
                    .attr("fill", "none")
                    .attr("stroke", "#67C23A")
                    .attr("stroke-width", 2);
            }
        },

        // 工具函数：特征值分解
        eigenDecomposition(A) {
            // 对于2x2矩阵，直接计算特征值和特征向量
            const a = A[0][0];
            const b = A[0][1];
            const c = A[1][0];
            const d = A[1][1];

            const trace = a + d;
            const det = a * d - b * c;

            // 避免负数的平方根
            let discriminant = trace * trace - 4 * det;
            discriminant = Math.max(0, discriminant);

            const lambda1 = (trace + Math.sqrt(discriminant)) / 2;
            const lambda2 = (trace - Math.sqrt(discriminant)) / 2;

            // 计算特征向量
            let v1, v2;
            if (b !== 0) {
                v1 = [lambda1 - d, c];
                v2 = [lambda2 - d, c];
            } else if (c !== 0) {
                v1 = [b, lambda1 - a];
                v2 = [b, lambda2 - a];
            } else {
                v1 = [1, 0];
                v2 = [0, 1];
            }

            // 归一化特征向量
            const norm1 = Math.sqrt(v1[0] * v1[0] + v1[1] * v1[1]) || 1;
            const norm2 = Math.sqrt(v2[0] * v2[0] + v2[1] * v2[1]) || 1;

            v1 = [v1[0] / norm1, v1[1] / norm1];
            v2 = [v2[0] / norm2, v2[1] / norm2];

            // 计算旋转角度
            const rotation = Math.atan2(v1[1], v1[0]);

            return [
                {
                    values: [lambda1, lambda2],
                    vectors: [v1, v2]
                },
                rotation
            ];
        },

        checkAnswer() {
            this.quizChecked = true;
            this.quizCorrect = this.quizAnswer === 1;

            if (this.quizCorrect) {
                this.response = `
### 🎉 回答正确！

当类别中心相距更远时，类间散布矩阵的特征值确实会变大，椭圆也会变大。这是因为：

1. 类间散布矩阵 $S_B$ 度量了各类别均值与全局均值之间的差异
2. 当类别中心相距更远时，它们与全局均值的距离也会增大
3. 这会导致 $S_B$ 中的分量变大，从而使得特征值增大
4. 几何上，类间散布椭圆变大反映了类别之间可分性的增强

在LDA中，我们希望最大化类间散布矩阵的度量，因为这意味着不同类别更容易被分开。
    `;
            } else {
                this.response = `
### ❌ 回答不正确

当类别中心相距更远时，类间散布矩阵的特征值会变大，椭圆也会变大。

类间散布矩阵 $S_B = \\sum_{c=1}^{k} n_c (\\mu_c - \\mu)(\\mu_c - \\mu)^T$ 中的每一项都是类别均值与全局均值差值的外积。当类别中心相距更远时，这些差值会变大，导致 $S_B$ 的特征值增大。

请再观察一下可视化结果，尝试调整各类别中心的位置，看看类间散布椭圆的变化。
    `;
            }

            this.showResponse = true;
        },

        completeSection() {
            this.isCompleted = true;
            this.$emit('complete', this.sectionId);

            // 滚动到下一部分
            if (this.hasNext) {
                this.navigateToNext();
            }
        },

        getCompletedSections() {
            const saved = localStorage.getItem('lda-tutorial-progress');
            if (saved) {
                try {
                    return JSON.parse(saved);
                } catch (e) {
                    console.error('Failed to parse completed sections:', e);
                    return [];
                }
            }
            return [];
        },

        navigateToNext() {
            // 计算下一个部分的ID
            const allSections = this.$parent.sections;
            const currentIndex = allSections.findIndex(s => s.id === this.sectionId);

            if (currentIndex >= 0 && currentIndex < allSections.length - 1) {
                const nextSectionId = allSections[currentIndex + 1].id;
                this.$parent.scrollToSection(nextSectionId);
            }
        }
    }
}
</script>

<style scoped>
.tutorial-section {
    margin-bottom: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.section-title {
    margin: 0;
    color: #303133;
}

.section-progress {
    display: flex;
    align-items: center;
}

.section-number {
    margin-left: 10px;
    font-size: 14px;
    color: #909399;
}

.content-area {
    margin-bottom: 20px;
}

.markdown-content {
    line-height: 1.6;
}

/* 互动区域样式 */
.interaction-area {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
}

.interaction-title {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    color: #606266;
}

.interaction-description {
    margin-bottom: 20px;
    font-size: 14px;
    color: #606266;
}

.visualization-container {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
}

#between-class-viz {
    width: 100%;
    max-width: 600px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background-color: white;
    margin-bottom: 15px;
    align-self: center;
}

.viz-controls {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.control-group {
    display: flex;
    align-items: center;
    width: 100%;
}

.control-label {
    width: 120px;
    font-size: 14px;
    color: #606266;
}

.matrix-display {
    margin-top: 10px;
    padding: 10px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
}

.matrix-display h4 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 14px;
    color: #606266;
}

.matrix {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
}

.matrix-row {
    display: flex;
    gap: 5px;
}

.matrix-cell {
    width: 60px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #dcdfe6;
    background-color: #f5f7fa;
    font-family: monospace;
    font-size: 14px;
}

.data-info {
    margin-top: 10px;
    padding: 10px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
}

.data-info h4 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 14px;
    color: #606266;
}

.data-info p {
    margin: 5px 0;
    font-size: 13px;
    color: #606266;
    display: flex;
    align-items: center;
}

.dot {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
}

.ellipse-marker {
    display: inline-block;
    width: 16px;
    height: 8px;
    border: 2px solid;
    border-radius: 50%;
    margin-right: 8px;
}

.interactive-quiz {
    margin-top: 20px;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
}

.interactive-quiz h4 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    color: #606266;
}

.question {
    margin-bottom: 15px;
    font-weight: 500;
    color: #303133;
}

.quiz-actions {
    margin-top: 15px;
    display: flex;
    gap: 10px;
}

/* 回应区域样式 */
.response-area {
    margin-top: 20px;
    padding: 15px;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
}

.response-content {
    display: flex;
    margin-bottom: 15px;
}

.response-icon {
    font-size: 24px;
    margin-right: 10px;
}

.response-icon.correct {
    color: #67C23A;
}

.response-icon.incorrect {
    color: #F56C6C;
}

.response-message {
    flex: 1;
}

.completed-message {
    display: flex;
    align-items: center;
    color: #67C23A;
    margin-top: 20px;
}

.completed-message i {
    font-size: 20px;
    margin-right: 8px;
}

/* KaTeX样式调整 */
:deep(.math-block) {
    overflow-x: auto;
    margin: 15px 0;
    padding: 10px;
    background-color: #f8f8f9;
    border-radius: 4px;
}
</style>