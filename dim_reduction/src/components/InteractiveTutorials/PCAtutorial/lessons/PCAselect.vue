<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="scree-plot-interactive">
                <h3>主成分选择交互式练习</h3>
                <p>通过调整特征值分布，观察不同的主成分选择方法。</p>

                <div class="dataset-selection">
                    <h4>选择数据集类型</h4>
                    <el-radio-group v-model="selectedDataset" @change="updateVisualization">
                        <el-radio :label="0">均匀分布的特征值</el-radio>
                        <el-radio :label="1">主要有两个主成分</el-radio>
                        <el-radio :label="2">主要有一个主成分</el-radio>
                        <el-radio :label="3">逐渐衰减的特征值</el-radio>
                    </el-radio-group>
                </div>

                <div class="visualization-container">
                    <div id="scree-plot" ref="screePlotContainer"></div>
                </div>

                <div class="selection-methods">
                    <h4>主成分选择方法</h4>

                    <div class="method-container">
                        <div class="method-description">
                            <h5>1. 方差解释比例法</h5>
                            <p>选择累计方差贡献率达到指定阈值的主成分数量</p>
                            <el-slider v-model="varianceThreshold" :min="50" :max="99"
                                :format-tooltip="value => `${value}%`" @change="updateThresholdLine"></el-slider>
                            <p class="result-text">
                                选择主成分数量：<span class="result-value">{{ selectedComponentsByVariance }}</span>
                            </p>
                        </div>

                        <div class="method-description">
                            <h5>2. Kaiser法则</h5>
                            <p>选择特征值大于1的主成分（当数据标准化时适用）</p>
                            <div class="kaiser-control">
                                <span>特征值阈值：</span>
                                <el-input-number v-model="kaiserThreshold" :min="0.1" :max="5" :step="0.1"
                                    @change="updateThresholdLine"></el-input-number>
                            </div>
                            <p class="result-text">
                                选择主成分数量：<span class="result-value">{{ selectedComponentsByKaiser }}</span>
                            </p>
                        </div>

                        <div class="method-description">
                            <h5>3. 肘部法则</h5>
                            <p>在碎石图中寻找"肘部"，即曲线急剧变化的点</p>
                            <p class="result-text">
                                建议选择主成分数量：<span class="result-value">{{ suggestedElbowComponents }}</span>
                            </p>
                        </div>
                    </div>
                </div>

                <div class="understanding-check">
                    <h4>理解检查</h4>
                    <p>基于您的观察，以下关于主成分选择的描述哪一项是正确的？</p>

                    <el-radio-group v-model="selectedAnswer" class="understanding-options">
                        <el-radio :label="0">所有数据集都应该保留所有主成分以获得最佳结果</el-radio>
                        <el-radio :label="1">应该始终保留特征值最大的前三个主成分</el-radio>
                        <el-radio :label="2">根据具体数据集特征和应用需求，使用不同的方法选择合适数量的主成分</el-radio>
                        <el-radio :label="3">不应该使用主观方法如肘部法则，只能使用严格的数学标准</el-radio>
                    </el-radio-group>

                    <el-button type="primary" @click="checkAnswer" :disabled="selectedAnswer === null"
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

export default {
    name: 'SelectingPCs',
    components: {
        BaseSegment
    },
    data() {
        return {
            title: '5. 选择主成分',
            segmentId: 'selecting-pcs',
            content: `
  ## 如何选择最优的主成分数量
  
  在应用PCA时，一个关键问题是：我们应该保留多少个主成分？这涉及到降维程度与信息保留之间的权衡。
  
  ### 主成分选择的原则
  
  主成分选择的核心原则是：**保留足够的信息，同时实现最大程度的降维**。具体来说，我们希望：
  
  1. **减少数据维度**：降低计算复杂度，避免维度灾难
  2. **过滤噪声**：较小的特征值往往对应噪声
  3. **保留主要信息**：确保重要的数据模式不丢失
  
  ### 常用的选择方法
  
  实践中常用的主成分选择方法包括：
  
  #### 1. 累计方差贡献率法
  
  设定一个方差解释比例的阈值（通常为85%、90%或95%），选择累计方差贡献率达到该阈值的最少主成分数量。
  
  计算方法：
  $$\\frac{\\sum_{i=1}^{k} \\lambda_i}{\\sum_{i=1}^{n} \\lambda_i} \\geq \\text{threshold}$$
  
  其中 $\\lambda_i$ 是第i个特征值，$k$是要选择的主成分数量，$n$是特征总数。
  
  #### 2. Kaiser法则
  
  选择特征值大于1的主成分。这个方法基于这样的想法：只有解释了比单个原始变量更多方差的主成分才值得保留。
  
  注意：此方法适用于已标准化（方差为1）的数据。
  
  #### 3. 肘部法则（碎石图）
  
  绘制特征值递减图（碎石图），寻找曲线中的"肘部"，即曲线斜率发生显著变化的点。这一点之后的主成分贡献较小，可以舍弃。
  
  
  #### 4. 交叉验证
  
  使用交叉验证评估不同主成分数量的模型性能，选择性能最佳的主成分数量。这是一种数据驱动的方法，但计算成本较高。
  
  ### 实际考量
  
  在实际应用中，最佳的主成分数量还取决于：
  
  - **应用需求**：可视化可能只需要2-3个主成分，而数据压缩可能需要更多
  - **计算资源限制**：更多的主成分意味着更高的计算和存储成本
  - **领域知识**：对数据和问题的理解有助于判断合适的主成分数量
  
  接下来，通过交互式练习来理解不同主成分选择方法的效果。
        `,
            // 可视化和互动数据
            selectedDataset: 0,
            svg: null,
            width: 600,
            height: 400,
            margin: { top: 50, right: 50, bottom: 50, left: 50 },
            eigenvalues: [],
            cumulativeVariance: [],
            totalVariance: 0,

            // 选择方法参数
            varianceThreshold: 90,  // 默认90%
            kaiserThreshold: 1.0,   // 默认特征值>1

            // 选择结果
            selectedComponentsByVariance: 0,
            selectedComponentsByKaiser: 0,
            suggestedElbowComponents: 0,

            // 可视化元素
            varianceThresholdLine: null,
            kaiserThresholdLine: null,
            elbowPoint: null,

            // 理解检查
            selectedAnswer: null,
            attempts: 0
        };
    },
    methods: {
        generateDataset() {
            const numComponents = 10;

            // 根据所选数据集生成特征值
            switch (this.selectedDataset) {
                case 0: // 均匀分布的特征值
                    this.eigenvalues = Array.from({ length: numComponents }, (_, i) =>
                        10 - i * (8 / numComponents)
                    );
                    break;

                case 1: // 主要有两个主成分
                    this.eigenvalues = [15, 10];
                    for (let i = 2; i < numComponents; i++) {
                        this.eigenvalues.push(2 - 0.15 * (i - 2));
                    }
                    break;

                case 2: // 主要有一个主成分
                    this.eigenvalues = [20];
                    for (let i = 1; i < numComponents; i++) {
                        this.eigenvalues.push(3 - 0.25 * (i - 1));
                    }
                    break;

                case 3: // 逐渐衰减的特征值
                    this.eigenvalues = Array.from({ length: numComponents }, (_, i) =>
                        12 / (i + 1)
                    );
                    break;
            }

            // 确保所有特征值为正
            this.eigenvalues = this.eigenvalues.map(v => Math.max(0.1, v));

            // 计算累计方差比例
            this.totalVariance = this.eigenvalues.reduce((sum, val) => sum + val, 0);
            let cumulativeSum = 0;
            this.cumulativeVariance = this.eigenvalues.map(val => {
                cumulativeSum += val;
                return (cumulativeSum / this.totalVariance) * 100;
            });

            // 计算各方法的选择结果
            this.calculateSelectionResults();
        },

        calculateSelectionResults() {
            // 方差解释比例法
            this.selectedComponentsByVariance = this.cumulativeVariance.findIndex(
                val => val >= this.varianceThreshold
            ) + 1;

            // Kaiser法则
            this.selectedComponentsByKaiser = this.eigenvalues.filter(
                val => val >= this.kaiserThreshold
            ).length;

            // 肘部法则（简化实现）
            // 寻找曲线斜率变化最显著的点
            const diffs = [];
            for (let i = 1; i < this.eigenvalues.length; i++) {
                diffs.push(this.eigenvalues[i - 1] - this.eigenvalues[i]);
            }

            // 寻找差异最大的点
            let maxDiffIndex = 0;
            let maxDiff = 0;
            for (let i = 0; i < diffs.length - 1; i++) {
                const diff = diffs[i] - diffs[i + 1];
                if (diff > maxDiff) {
                    maxDiff = diff;
                    maxDiffIndex = i;
                }
            }

            this.suggestedElbowComponents = maxDiffIndex + 1;
        },

        updateVisualization() {
            // 生成数据集
            this.generateDataset();

            // 清除之前的可视化
            d3.select(this.$refs.screePlotContainer).selectAll("*").remove();

            // 创建SVG
            this.svg = d3.select(this.$refs.screePlotContainer)
                .append("svg")
                .attr("width", this.width)
                .attr("height", this.height);

            const plotWidth = this.width - this.margin.left - this.margin.right;
            const plotHeight = this.height - this.margin.top - this.margin.bottom;

            // 创建一个包含所有图形的组
            const g = this.svg.append("g")
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

            // 创建X比例尺（主成分索引）
            const xScale = d3.scaleLinear()
                .domain([0, this.eigenvalues.length - 1])
                .range([0, plotWidth]);

            // 创建Y比例尺（特征值）
            const maxEigenvalue = Math.max(...this.eigenvalues) * 1.1;
            const yScaleEigenvalue = d3.scaleLinear()
                .domain([0, maxEigenvalue])
                .range([plotHeight, 0]);

            // 创建Y2比例尺（累计方差百分比）
            const yScaleCumulative = d3.scaleLinear()
                .domain([0, 100])
                .range([plotHeight, 0]);

            // 添加X轴
            g.append("g")
                .attr("class", "x-axis")
                .attr("transform", `translate(0,${plotHeight})`)
                .call(d3.axisBottom(xScale).ticks(this.eigenvalues.length).tickFormat(d => d + 1));

            // 添加Y轴（特征值）
            g.append("g")
                .attr("class", "y-axis-eigenvalue")
                .call(d3.axisLeft(yScaleEigenvalue));

            // 添加Y2轴（累计方差百分比）
            g.append("g")
                .attr("class", "y-axis-cumulative")
                .attr("transform", `translate(${plotWidth},0)`)
                .call(d3.axisRight(yScaleCumulative).tickFormat(d => d + "%"));

            // 添加轴标签
            g.append("text")
                .attr("class", "x-axis-label")
                .attr("text-anchor", "middle")
                .attr("x", plotWidth / 2)
                .attr("y", plotHeight + 40)
                .text("主成分索引");

            g.append("text")
                .attr("class", "y-axis-label")
                .attr("text-anchor", "middle")
                .attr("transform", "rotate(-90)")
                .attr("x", -plotHeight / 2)
                .attr("y", -40)
                .text("特征值");

            g.append("text")
                .attr("class", "y2-axis-label")
                .attr("text-anchor", "middle")
                .attr("transform", "rotate(90)")
                .attr("x", plotHeight / 2)
                .attr("y", -plotWidth - 40)
                .text("累计方差百分比 (%)");

            // 绘制柱状图（特征值）
            g.selectAll(".eigenvalue-bar")
                .data(this.eigenvalues)
                .enter()
                .append("rect")
                .attr("class", "eigenvalue-bar")
                .attr("x", (d, i) => xScale(i) - 15)
                .attr("y", d => yScaleEigenvalue(d))
                .attr("width", 30)
                .attr("height", d => plotHeight - yScaleEigenvalue(d))
                .attr("fill", "#69b3a2")
                .attr("opacity", 0.7);

            // 绘制折线图（累计方差百分比）
            const line = d3.line()
                .x((d, i) => xScale(i))
                .y(d => yScaleCumulative(d));

            g.append("path")
                .datum(this.cumulativeVariance)
                .attr("class", "cumulative-line")
                .attr("fill", "none")
                .attr("stroke", "#e63946")
                .attr("stroke-width", 2)
                .attr("d", line);

            // 添加累计方差的点
            g.selectAll(".cumulative-point")
                .data(this.cumulativeVariance)
                .enter()
                .append("circle")
                .attr("class", "cumulative-point")
                .attr("cx", (d, i) => xScale(i))
                .attr("cy", d => yScaleCumulative(d))
                .attr("r", 4)
                .attr("fill", "#e63946");

            // 添加图例
            const legend = g.append("g")
                .attr("class", "legend")
                .attr("transform", `translate(${plotWidth - 180}, 10)`);

            // 特征值图例
            legend.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", 15)
                .attr("height", 15)
                .attr("fill", "#69b3a2")
                .attr("opacity", 0.7);

            legend.append("text")
                .attr("x", 20)
                .attr("y", 12)
                .text("特征值");

            // 累计方差图例
            legend.append("line")
                .attr("x1", 0)
                .attr("y1", 35)
                .attr("x2", 15)
                .attr("y2", 35)
                .attr("stroke", "#e63946")
                .attr("stroke-width", 2);

            legend.append("circle")
                .attr("cx", 7.5)
                .attr("cy", 35)
                .attr("r", 4)
                .attr("fill", "#e63946");

            legend.append("text")
                .attr("x", 20)
                .attr("y", 40)
                .text("累计方差百分比");

            // 保存阈值线和肘部点的引用，以便后续更新
            // 方差阈值线
            this.varianceThresholdLine = g.append("line")
                .attr("class", "threshold-line")
                .attr("x1", 0)
                .attr("y1", yScaleCumulative(this.varianceThreshold))
                .attr("x2", plotWidth)
                .attr("y2", yScaleCumulative(this.varianceThreshold))
                .attr("stroke", "#e63946")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "5,5");

            g.append("text")
                .attr("class", "threshold-label")
                .attr("x", 5)
                .attr("y", yScaleCumulative(this.varianceThreshold) - 5)
                .attr("fill", "#e63946")
                .text(`${this.varianceThreshold}%阈值`);

            // Kaiser阈值线
            this.kaiserThresholdLine = g.append("line")
                .attr("class", "kaiser-line")
                .attr("x1", 0)
                .attr("y1", yScaleEigenvalue(this.kaiserThreshold))
                .attr("x2", plotWidth)
                .attr("y2", yScaleEigenvalue(this.kaiserThreshold))
                .attr("stroke", "#1d3557")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "5,5");

            g.append("text")
                .attr("class", "kaiser-label")
                .attr("x", 5)
                .attr("y", yScaleEigenvalue(this.kaiserThreshold) - 5)
                .attr("fill", "#1d3557")
                .text(`特征值=${this.kaiserThreshold}阈值`);

            // 标记肘部点
            this.elbowPoint = g.append("circle")
                .attr("class", "elbow-point")
                .attr("cx", xScale(this.suggestedElbowComponents - 1))
                .attr("cy", yScaleEigenvalue(this.eigenvalues[this.suggestedElbowComponents - 1]))
                .attr("r", 8)
                .attr("fill", "none")
                .attr("stroke", "#ffb703")
                .attr("stroke-width", 2);

            g.append("text")
                .attr("class", "elbow-label")
                .attr("x", xScale(this.suggestedElbowComponents - 1) + 10)
                .attr("y", yScaleEigenvalue(this.eigenvalues[this.suggestedElbowComponents - 1]) - 10)
                .attr("fill", "#ffb703")
                .text("肘部");

            // 保存比例尺以便更新
            this.xScale = xScale;
            this.yScaleEigenvalue = yScaleEigenvalue;
            this.yScaleCumulative = yScaleCumulative;
        },

        updateThresholdLine() {
            // 更新选择结果
            this.calculateSelectionResults();

            // 更新方差阈值线
            this.varianceThresholdLine
                .attr("y1", this.yScaleCumulative(this.varianceThreshold))
                .attr("y2", this.yScaleCumulative(this.varianceThreshold));

            // 更新Kaiser阈值线
            this.kaiserThresholdLine
                .attr("y1", this.yScaleEigenvalue(this.kaiserThreshold))
                .attr("y2", this.yScaleEigenvalue(this.kaiserThreshold));

            // 更新肘部点
            this.elbowPoint
                .attr("cx", this.xScale(this.suggestedElbowComponents - 1))
                .attr("cy", this.yScaleEigenvalue(this.eigenvalues[this.suggestedElbowComponents - 1]));

            // 更新标签
            this.svg.select(".threshold-label")
                .attr("y", this.yScaleCumulative(this.varianceThreshold) - 5)
                .text(`${this.varianceThreshold}%阈值`);

            this.svg.select(".kaiser-label")
                .attr("y", this.yScaleEigenvalue(this.kaiserThreshold) - 5)
                .text(`特征值=${this.kaiserThreshold}阈值`);

            this.svg.select(".elbow-label")
                .attr("x", this.xScale(this.suggestedElbowComponents - 1) + 10)
                .attr("y", this.yScaleEigenvalue(this.eigenvalues[this.suggestedElbowComponents - 1]) - 10);
        },

        checkAnswer() {
            this.attempts++;
            const correctAnswer = 2; // 正确答案：根据具体数据集特征和应用需求...

            if (this.selectedAnswer === correctAnswer) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "回答正确！",
                    "选择主成分的数量确实应该根据具体数据集的特征和应用需求来确定。不同的方法（如方差贡献率、Kaiser法则、肘部法则等）可能在不同情况下更适用。这是PCA应用中的一个重要决策点。",
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.attempts >= 2) {
                    hint = "提示：尝试在不同的数据集上应用各种选择方法，观察结果的差异。思考为什么没有一种方法在所有情况下都是最佳的。";
                }

                this.$refs.baseSegment.showResponse(
                    "回答不正确",
                    `请再思考主成分选择的原则和方法。${hint}`,
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
            d3.select(this.$refs.screePlotContainer).selectAll("*").remove();
        }
    }
}
</script>

<style scoped>
.scree-plot-interactive {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.dataset-selection {
    margin-bottom: 20px;
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

.selection-methods {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.method-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 15px;
}

.method-description {
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.method-description h5 {
    margin-top: 0;
    color: #409EFF;
}

.kaiser-control {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 10px 0;
}

.result-text {
    margin-top: 10px;
    font-weight: bold;
}

.result-value {
    color: #409EFF;
    font-size: 1.1em;
}

.understanding-check {
    margin-top: 30px;
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

/* D3可视化样式 */
:deep(.x-axis) path,
:deep(.y-axis-eigenvalue) path,
:deep(.y-axis-cumulative) path {
    stroke: #888;
}

:deep(.x-axis) text,
:deep(.y-axis-eigenvalue) text,
:deep(.y-axis-cumulative) text {
    fill: #555;
    font-size: 12px;
}

:deep(.x-axis-label),
:deep(.y-axis-label),
:deep(.y2-axis-label) {
    fill: #333;
    font-size: 14px;
    font-weight: bold;
}
</style>