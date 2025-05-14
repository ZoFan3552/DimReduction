<!-- WithinClassScatterMatrix.vue - 类内散布矩阵教学组件 -->
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

        <!-- 互动区域 - 类内散布矩阵可视化 -->
        <div v-if="!isCompleted" class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-data-analysis"></i> 互动练习：探索类内散布矩阵
            </h3>

            <p class="interaction-description">
                调整下方的散布椭圆参数，观察类内散布矩阵的几何意义。尝试理解类内散布矩阵是如何度量同一类别内样本分散程度的。
            </p>

            <div class="visualization-container">
                <div id="within-class-viz" ref="d3Container"></div>

                <div class="viz-controls">
                    <div class="control-group">
                        <span class="control-label">类别1方差 X:</span>
                        <el-slider v-model="class1VarX" :min="0.5" :max="5" :step="0.1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别1方差 Y:</span>
                        <el-slider v-model="class1VarY" :min="0.5" :max="5" :step="0.1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别1协方差:</span>
                        <el-slider v-model="class1Cov" :min="-2" :max="2" :step="0.1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别2方差 X:</span>
                        <el-slider v-model="class2VarX" :min="0.5" :max="5" :step="0.1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别2方差 Y:</span>
                        <el-slider v-model="class2VarY" :min="0.5" :max="5" :step="0.1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">类别2协方差:</span>
                        <el-slider v-model="class2Cov" :min="-2" :max="2" :step="0.1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="matrix-display">
                        <h4>类内散布矩阵 S<sub>W</sub>:</h4>
                        <div class="matrix">
                            <div class="matrix-row">
                                <div class="matrix-cell">{{ formatNumber(withinClassMatrix[0][0]) }}</div>
                                <div class="matrix-cell">{{ formatNumber(withinClassMatrix[0][1]) }}</div>
                            </div>
                            <div class="matrix-row">
                                <div class="matrix-cell">{{ formatNumber(withinClassMatrix[1][0]) }}</div>
                                <div class="matrix-cell">{{ formatNumber(withinClassMatrix[1][1]) }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="interactive-quiz">
                <h4>根据你的观察回答以下问题:</h4>

                <p class="question">当类内方差增大时，LDA的分类效果会如何变化？</p>

                <el-radio-group v-model="quizAnswer">
                    <el-radio :label="0">分类效果会变好，因为类内散布更大意味着数据分布更广</el-radio>
                    <el-radio :label="1">分类效果会变差，因为类内散布更大意味着类内样本更分散，更难区分</el-radio>
                    <el-radio :label="2">分类效果不受类内方差影响，只与类间距离有关</el-radio>
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
    name: 'WithinClassScatterMatrix',
    props: {
        sectionId: {
            type: String,
            default: 'within-class-scatter'
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
            title: "类内散布矩阵",
            markdownContent: `
# 类内散布矩阵 (Within-Class Scatter Matrix)

类内散布矩阵是LDA算法的核心概念之一，它度量了同一类别内样本的分散程度。

## 数学定义

类内散布矩阵 $S_W$ 定义为：

$$
S_W = \\sum_{c=1}^{k} \\sum_{i \\in c} (x_i - \\mu_c)(x_i - \\mu_c)^T
$$

其中：
- $k$ 是类别数量
- $x_i$ 是类别 $c$ 中的样本
- $\\mu_c$ 是类别 $c$ 的均值向量

## 几何意义

类内散布矩阵 $S_W$ 反映了每个类别内部数据点的分散程度。从几何角度看，它衡量了每个类别内数据点围绕其类均值的散布情况。

我们可以将 $S_W$ 理解为所有类的协方差矩阵的加权和：

$$
S_W = \\sum_{c=1}^{k} n_c \\Sigma_c
$$

其中 $\\Sigma_c$ 是类别 $c$ 的协方差矩阵，$n_c$ 是类别 $c$ 中的样本数量。

## 二维情况的直观理解

在二维空间中，协方差矩阵可以被可视化为一个椭圆。椭圆的主轴方向对应协方差矩阵的特征向量，轴的长度对应特征值的平方根。

对于类内散布矩阵：
- 椭圆越"扁平"表示数据在某个方向上的变化比其他方向大
- 椭圆的大小表示数据的总体分散程度
- 椭圆的倾斜角度反映了特征之间的相关性

## 类内散布矩阵在LDA中的作用

在LDA中，我们希望最小化类内散度，也就是希望每个类别内部的样本尽可能聚集。这意味着我们希望投影后的数据点在每个类别内的方差尽可能小。

投影后的类内散度可以表示为：

$$
w^T S_W w
$$

其中 $w$ 是投影方向。

LDA寻找的是最小化 $w^T S_W w$ 同时最大化 $w^T S_B w$ 的投影方向，即最大化：

$$
J(w) = \\frac{w^T S_B w}{w^T S_W w}
$$

在下面的互动练习中，你可以调整不同类别的协方差矩阵参数，观察它们对类内散布矩阵的影响，以及这如何影响LDA的分类性能。
      `,
            isCompleted: false,

            // D3可视化数据
            svg: null,
            width: 600,
            height: 400,
            margin: { top: 30, right: 30, bottom: 30, left: 40 },

            // 可调整参数
            class1VarX: 1.0,
            class1VarY: 1.0,
            class1Cov: 0.0,
            class2VarX: 1.0,
            class2VarY: 1.0,
            class2Cov: 0.0,

            // 计算结果
            withinClassMatrix: [[2.0, 0.0], [0.0, 2.0]],
            class1Samples: [],
            class2Samples: [],

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
            this.svg = d3.select("#within-class-viz")
                .append("svg")
                .attr("width", containerWidth)
                .attr("height", this.height)
                .append("g")
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

            // 初始化坐标系
            const xScale = d3.scaleLinear()
                .domain([-5, 15])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([-5, 15])
                .range([height, 0]);

            // 添加X和Y轴
            this.svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", `translate(0,${height / 2})`)
                .call(d3.axisBottom(xScale));

            this.svg.append("g")
                .attr("class", "y-axis")
                .attr("transform", `translate(${width / 2},0)`)
                .call(d3.axisLeft(yScale));

            // 添加网格线
            this.svg.append("g")
                .attr("class", "grid-lines")
                .selectAll("line")
                .data(d3.range(-5, 16, 1))
                .enter()
                .append("line")
                .attr("x1", d => xScale(d))
                .attr("y1", yScale(-5))
                .attr("x2", d => xScale(d))
                .attr("y2", yScale(15))
                .attr("stroke", "#eee")
                .attr("stroke-width", 1);

            this.svg.append("g")
                .attr("class", "grid-lines")
                .selectAll("line")
                .data(d3.range(-5, 16, 1))
                .enter()
                .append("line")
                .attr("x1", xScale(-5))
                .attr("y1", d => yScale(d))
                .attr("x2", xScale(15))
                .attr("y2", d => yScale(d))
                .attr("stroke", "#eee")
                .attr("stroke-width", 1);

            // 生成初始数据
            this.generateData();

            // 绘制数据点和椭圆
            this.updateVisualization();
        },

        generateData() {
            const generateSamples = (mean, cov, n) => {
                const samples = [];
                const chol = this.choleskyDecomposition(cov);

                for (let i = 0; i < n; i++) {
                    // 生成标准正态分布样本
                    const z1 = this.randn();
                    const z2 = this.randn();

                    // 转换为指定协方差的正态分布样本
                    const x = mean[0] + chol[0][0] * z1 + chol[0][1] * z2;
                    const y = mean[1] + chol[1][0] * z1 + chol[1][1] * z2;

                    samples.push([x, y]);
                }

                return samples;
            };

            // 生成类别1的样本（中心在 (3,3)）
            const cov1 = [
                [this.class1VarX, this.class1Cov],
                [this.class1Cov, this.class1VarY]
            ];
            this.class1Samples = generateSamples([3, 3], cov1, 50);

            // 生成类别2的样本（中心在 (8,8)）
            const cov2 = [
                [this.class2VarX, this.class2Cov],
                [this.class2Cov, this.class2VarY]
            ];
            this.class2Samples = generateSamples([8, 8], cov2, 50);

            // 计算类内散布矩阵
            this.calculateWithinClassMatrix();
        },

        updateVisualization() {
            // 重新生成数据
            this.generateData();

            const containerWidth = this.$refs.d3Container.clientWidth || this.width;
            const width = containerWidth - this.margin.left - this.margin.right;
            const height = this.height - this.margin.top - this.margin.bottom;

            // 刷新坐标系
            const xScale = d3.scaleLinear()
                .domain([-5, 15])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([-5, 15])
                .range([height, 0]);

            // 移除已有的数据点和椭圆
            this.svg.selectAll(".data-point, .confidence-ellipse").remove();

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
                .attr("opacity", 0.7);

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
                .attr("opacity", 0.7);

            // 绘制类别1的95%置信椭圆
            const cov1 = [
                [this.class1VarX, this.class1Cov],
                [this.class1Cov, this.class1VarY]
            ];
            this.drawConfidenceEllipse(xScale, yScale, [3, 3], cov1, "#409EFF");

            // 绘制类别2的95%置信椭圆
            const cov2 = [
                [this.class2VarX, this.class2Cov],
                [this.class2Cov, this.class2VarY]
            ];
            this.drawConfidenceEllipse(xScale, yScale, [8, 8], cov2, "#E6A23C");

            // 绘制总体类内散布椭圆
            const meanCombined = [5.5, 5.5]; // 两类中心点的中点
            this.drawConfidenceEllipse(xScale, yScale, meanCombined, this.withinClassMatrix, "#67C23A", "dashed");
        },

        drawConfidenceEllipse(xScale, yScale, mean, cov, color, strokeType = "solid") {
            // 计算椭圆参数
            const [eigen, rotation] = this.eigenDecomposition(cov);
            const width = 2.447 * Math.sqrt(eigen.values[0]); // 95%置信椭圆
            const height = 2.447 * Math.sqrt(eigen.values[1]);

            const arc = d3.arc()
                .startAngle(0)
                .endAngle(2 * Math.PI)
                .innerRadius(0)
                .outerRadius(1);

            const ellipsePath = d3.path();
            arc.context(ellipsePath)({
                x: xScale(mean[0]),
                y: yScale(mean[1]),
                // 调整半径模拟椭圆
                r: Math.max(width * (xScale(1) - xScale(0)), height * (yScale(0) - yScale(1))),
                // 可选：旋转
                rotation: rotation
            });

            // 添加到 SVG
            this.svg.append("path")
                .attr("class", "confidence-ellipse")
                .attr("d", ellipsePath.toString())
                .attr("fill", "none")
                .attr("stroke", color)
                .attr("stroke-width", 2)
                .attr("stroke-dasharray", strokeType === "dashed" ? "5,5" : "0");

            // 添加均值点
            this.svg.append("circle")
                .attr("class", "confidence-ellipse")
                .attr("cx", xScale(mean[0]))
                .attr("cy", yScale(mean[1]))
                .attr("r", 5)
                .attr("fill", color);
        },

        calculateWithinClassMatrix() {
            // 计算类内散布矩阵 = 类别1协方差矩阵 + 类别2协方差矩阵
            this.withinClassMatrix = [
                [this.class1VarX + this.class2VarX, this.class1Cov + this.class2Cov],
                [this.class1Cov + this.class2Cov, this.class1VarY + this.class2VarY]
            ];
        },

        // 工具函数：Cholesky分解
        choleskyDecomposition(A) {
            const n = A.length;
            const L = Array(n).fill().map(() => Array(n).fill(0));

            for (let i = 0; i < n; i++) {
                for (let j = 0; j <= i; j++) {
                    let sum = 0;
                    for (let k = 0; k < j; k++) {
                        sum += L[i][k] * L[j][k];
                    }

                    if (i === j) {
                        L[i][i] = Math.sqrt(A[i][i] - sum);
                    } else {
                        L[i][j] = (A[i][j] - sum) / L[j][j];
                    }
                }
            }

            return L;
        },

        // 工具函数：标准正态分布随机数
        randn() {
            let u = 0, v = 0;
            while (u === 0) u = Math.random();
            while (v === 0) v = Math.random();
            return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
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

            const discriminant = Math.sqrt(trace * trace - 4 * det);
            const lambda1 = (trace + discriminant) / 2;
            const lambda2 = (trace - discriminant) / 2;

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
            const norm1 = Math.sqrt(v1[0] * v1[0] + v1[1] * v1[1]);
            const norm2 = Math.sqrt(v2[0] * v2[0] + v2[1] * v2[1]);

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
  
  当类内方差增大时，LDA的分类效果确实会变差。这是因为：
  
  1. 类内散布矩阵越大，表示每个类别内部的样本越分散
  2. 分散的类内样本会使得不同类别之间的边界变得模糊
  3. 在Fisher准则 $J(W) = \\frac{W^T S_B W}{W^T S_W W}$ 中，类内散布矩阵 $S_W$ 在分母位置
  4. 因此，$S_W$ 越大，优化目标值越小，分类效果越差
  
  在实际应用中，我们希望类内散布尽可能小（样本聚集），类间散布尽可能大（类别分离）。
          `;
            } else {
                this.response = `
  ### ❌ 回答不正确
  
  当类内方差增大时，LDA的分类效果会变差。
  
  请记住，LDA的优化目标是 $J(W) = \\frac{W^T S_B W}{W^T S_W W}$，其中 $S_W$ 是类内散布矩阵，位于分母位置。类内散布矩阵越大，表示同一类别内的样本越分散，使得不同类别的边界更难区分。
  
  请重新思考并尝试回答问题。
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
</style>