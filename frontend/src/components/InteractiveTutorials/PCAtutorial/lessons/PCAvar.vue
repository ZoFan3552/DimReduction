<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted">

        <!-- 互动部分：D3.js可视化与交互 -->
        <template v-slot:interaction>
            <div class="interactive-visualization">
                <h3>数据方差可视化练习</h3>
                <p>请拖动下面的滑块来调整数据点的分布，观察方差和主方向的变化。</p>

                <div class="controls">
                    <div class="control-item">
                        <span>X方向方差: {{ varianceX.toFixed(2) }}</span>
                        <el-slider v-model="varianceX" :min="0.5" :max="5" :step="0.1"
                            @input="updateVisualization"></el-slider>
                    </div>
                    <div class="control-item">
                        <span>Y方向方差: {{ varianceY.toFixed(2) }}</span>
                        <el-slider v-model="varianceY" :min="0.5" :max="5" :step="0.1"
                            @input="updateVisualization"></el-slider>
                    </div>
                    <div class="control-item">
                        <span>相关系数: {{ correlation.toFixed(2) }}</span>
                        <el-slider v-model="correlation" :min="-0.9" :max="0.9" :step="0.1"
                            @input="updateVisualization"></el-slider>
                    </div>
                </div>

                <div class="visualization-container">
                    <div id="variance-visualization" ref="visualizationContainer"></div>
                </div>

                <div class="reflection-question">
                    <h4>思考问题</h4>
                    <p>根据您的观察，当两个维度的方差不同时，PCA会优先选择哪个方向作为第一主成分？</p>

                    <el-radio-group v-model="reflectionAnswer" class="reflection-options">
                        <el-radio :label="0">方差较小的方向</el-radio>
                        <el-radio :label="1">方差较大的方向</el-radio>
                        <el-radio :label="2">两个方向的平均方向</el-radio>
                        <el-radio :label="3">与两个原始坐标轴夹角45度的方向</el-radio>
                    </el-radio-group>

                    <el-button type="primary" @click="checkReflection" :disabled="reflectionAnswer === null"
                        class="reflection-submit">
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

export default {
    name: 'DataVariance',
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
                console.log("方差子组件接受回答", newValue);
                if (newValue) {
                    this.reflectionAnswer = Number(newValue);
                    //   this.hasSubmittedAnswer = true;
                    //   this.feedback = '您之前已经完成了这个章节的练习。';
                }
            }
        }
    },
    data() {
        return {
            title: '2. 理解数据方差',
            segmentId: 'data-variance',
            content: `
  ## 方差与数据分布
  
  在理解PCA之前，我们需要深入了解**方差**的概念。方差是统计学中衡量数据分散程度的指标，它描述了数据点偏离均值的程度。
  
  数学上，一组数据 $x_1, x_2, ..., x_n$ 的方差计算公式为：
  
  $$\\sigma^2 = \\frac{1}{n}\\sum_{i=1}^{n}(x_i - \\mu)^2$$
  
  其中 $\\mu$ 是数据的均值： $\\mu = \\frac{1}{n}\\sum_{i=1}^{n}x_i$
  
  ### 方差与PCA的关系
  
  PCA的核心思想是**最大方差投影**。它假设数据中方差最大的方向包含了最多的信息。为什么这个假设有效呢？
  
  1. **信息量**：高方差通常意味着高信息量。如果一个维度的所有值都相同（方差为零），那这个维度不包含任何区分样本的信息。
  
  2. **信噪比**：在许多自然数据集中，较大的方差通常对应真实的模式，而较小的方差往往对应噪声。
  
  3. **可区分性**：方差大的方向使得数据点之间的区分更加明显，有利于后续的分类任务。
  
  ### 多维数据中的方差
  
  在多维数据中，我们不仅关注单一维度的方差，还关注不同维度之间的关系（协方差）。如果两个维度高度相关，意味着它们包含重复信息，可以压缩。
  
  
  ### 主方向与方差最大化
  
  PCA寻找的主成分就是数据方差最大的方向。第一主成分是方差最大的方向，第二主成分是与第一主成分正交且方差最大的方向，依此类推。
  
  在下面的交互练习中，您可以调整二维数据的分布，观察不同方差设置下的主方向变化。这将帮助您直观理解为什么PCA选择方差最大的方向作为主成分。
        `,
            // D3.js可视化参数
            varianceX: 2.0,
            varianceY: 1.0,
            correlation: 0.5,
            points: [],
            svg: null,
            width: 500,
            height: 400,
            margin: { top: 30, right: 30, bottom: 40, left: 40 },

            // 思考问题答案
            reflectionAnswer: null,
            reflectionAttempts: 0
        };
    },
    methods: {
        initializeVisualization() {
            // 清除之前的可视化
            d3.select(this.$refs.visualizationContainer).selectAll("*").remove();

            // 设置SVG
            this.svg = d3.select(this.$refs.visualizationContainer)
                .append("svg")
                .attr("width", this.width)
                .attr("height", this.height)
                .append("g")
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

            // 实际绘图区域尺寸
            const plotWidth = this.width - this.margin.left - this.margin.right;
            const plotHeight = this.height - this.margin.top - this.margin.bottom;

            // 创建X和Y比例尺
            this.xScale = d3.scaleLinear()
                .domain([-10, 10])
                .range([0, plotWidth]);

            this.yScale = d3.scaleLinear()
                .domain([-10, 10])
                .range([plotHeight, 0]);

            // 添加X和Y轴
            this.svg.append("g")
                .attr("transform", `translate(0,${plotHeight / 2})`)
                .call(d3.axisBottom(this.xScale));

            this.svg.append("g")
                .attr("transform", `translate(${plotWidth / 2},0)`)
                .call(d3.axisLeft(this.yScale));

            // 添加X和Y轴标签
            this.svg.append("text")
                .attr("x", plotWidth)
                .attr("y", plotHeight / 2 + 30)
                .style("text-anchor", "end")
                .text("X轴");

            this.svg.append("text")
                .attr("x", plotWidth / 2 - 30)
                .attr("y", 0)
                .style("text-anchor", "end")
                .text("Y轴");

            // 生成初始数据点
            this.generatePoints();
        },

        generatePoints() {
            // 清除现有点
            this.points = [];

            // 生成随机数据点
            const numPoints = 100;
            const mean = [0, 0];

            for (let i = 0; i < numPoints; i++) {
                // 生成相关的随机点
                const point = this.generateCorrelatedPoint(mean, this.varianceX, this.varianceY, this.correlation);
                this.points.push(point);
            }

            // 绘制点
            this.drawPoints();

            // 计算并绘制主成分
            this.calculateAndDrawPCA();
        },

        generateCorrelatedPoint(mean, varX, varY, corr) {
            // 生成独立的标准正态随机数
            const u1 = this.randomNormal();
            const u2 = this.randomNormal();

            // 使用Cholesky分解生成相关的随机变量
            const x = mean[0] + Math.sqrt(varX) * u1;
            const y = mean[1] + Math.sqrt(varY) * (corr * u1 + Math.sqrt(1 - corr * corr) * u2);

            return [x, y];
        },

        randomNormal() {
            // Box-Muller变换生成标准正态分布随机数
            const u1 = Math.random();
            const u2 = Math.random();

            return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        },

        drawPoints() {
            // 清除之前的点
            this.svg.selectAll(".data-point").remove();

            // 绘制新点
            this.svg.selectAll(".data-point")
                .data(this.points)
                .enter()
                .append("circle")
                .attr("class", "data-point")
                .attr("cx", d => this.xScale(d[0]))
                .attr("cy", d => this.yScale(d[1]))
                .attr("r", 3)
                .style("fill", "#69b3a2")
                .style("opacity", 0.7);
        },

        calculateAndDrawPCA() {
            // 计算数据的均值
            const meanX = d3.mean(this.points, d => d[0]);
            const meanY = d3.mean(this.points, d => d[1]);

            // 计算协方差矩阵
            let covXX = 0, covXY = 0, covYY = 0;

            this.points.forEach(point => {
                const diffX = point[0] - meanX;
                const diffY = point[1] - meanY;

                covXX += diffX * diffX;
                covXY += diffX * diffY;
                covYY += diffY * diffY;
            });

            covXX /= this.points.length;
            covXY /= this.points.length;
            covYY /= this.points.length;

            // 计算特征值和特征向量
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

                // 计算第二个特征向量（正交）
                v2x = -v1y;
                v2y = v1x;
            }

            // 绘制主成分轴
            this.drawPrincipalAxes(meanX, meanY, v1x, v1y, v2x, v2y, lambda1, lambda2);
        },

        drawPrincipalAxes(meanX, meanY, v1x, v1y, v2x, v2y, lambda1, lambda2) {
            // 清除之前的轴
            this.svg.selectAll(".principal-axis").remove();

            // 缩放参数
            const scale = 5;

            // 绘制第一主成分
            this.svg.append("line")
                .attr("class", "principal-axis")
                .attr("x1", this.xScale(meanX - scale * v1x * Math.sqrt(lambda1)))
                .attr("y1", this.yScale(meanY - scale * v1y * Math.sqrt(lambda1)))
                .attr("x2", this.xScale(meanX + scale * v1x * Math.sqrt(lambda1)))
                .attr("y2", this.yScale(meanY + scale * v1y * Math.sqrt(lambda1)))
                .style("stroke", "red")
                .style("stroke-width", 2)
                .style("stroke-dasharray", "5,5");

            // 绘制第二主成分
            this.svg.append("line")
                .attr("class", "principal-axis")
                .attr("x1", this.xScale(meanX - scale * v2x * Math.sqrt(lambda2)))
                .attr("y1", this.yScale(meanY - scale * v2y * Math.sqrt(lambda2)))
                .attr("x2", this.xScale(meanX + scale * v2x * Math.sqrt(lambda2)))
                .attr("y2", this.yScale(meanY + scale * v2y * Math.sqrt(lambda2)))
                .style("stroke", "blue")
                .style("stroke-width", 2)
                .style("stroke-dasharray", "5,5");

            // 添加标签
            this.svg.append("text")
                .attr("class", "principal-axis")
                .attr("x", this.xScale(meanX + scale * v1x * Math.sqrt(lambda1)))
                .attr("y", this.yScale(meanY + scale * v1y * Math.sqrt(lambda1)))
                .attr("dx", 10)
                .style("fill", "red")
                .text("第一主成分");

            this.svg.append("text")
                .attr("class", "principal-axis")
                .attr("x", this.xScale(meanX + scale * v2x * Math.sqrt(lambda2)))
                .attr("y", this.yScale(meanY + scale * v2y * Math.sqrt(lambda2)))
                .attr("dx", 10)
                .style("fill", "blue")
                .text("第二主成分");
        },

        updateVisualization() {
            // 重新生成点并更新可视化
            this.generatePoints();
        },

        checkReflection() {
            this.reflectionAttempts++;
            const correctAnswer = 1; // 正确答案是：方差较大的方向
            // 向父组件发送答案提交事件
            this.$emit('answer-submitted', this.reflectionAnswer);
            if (this.reflectionAnswer === correctAnswer) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "回答正确！",
                    "PCA确实优先选择方差较大的方向作为第一主成分，因为这个方向保留了数据中最多的信息。您可以在可视化中观察到，红色的第一主成分总是沿着数据分布最'拉伸'的方向。",
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.reflectionAttempts >= 2) {
                    hint = "提示：尝试将一个方向的方差设置得明显大于另一个方向，观察红色的第一主成分轴的变化。";
                }

                this.$refs.baseSegment.showResponse(
                    "回答不正确",
                    `请再观察可视化结果，思考PCA的主要目标是什么？${hint}`,
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
        // 初始化D3.js可视化
        this.$nextTick(() => {
            this.initializeVisualization();
        });
    },
    beforeDestroy() {
        // 清理D3资源
        if (this.svg) {
            d3.select(this.$refs.visualizationContainer).selectAll("*").remove();
        }
    }
}
</script>

<style scoped>
.interactive-visualization {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.controls {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 20px;
}

.control-item {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.visualization-container {
    width: 100%;
    height: 400px;
    margin: 20px 0;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    display: flex;
    justify-content: center;
}

.reflection-question {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.reflection-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 15px 0;
}

.reflection-submit {
    margin-top: 15px;
}
</style>