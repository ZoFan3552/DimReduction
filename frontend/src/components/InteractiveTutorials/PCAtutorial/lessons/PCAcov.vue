<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="covariance-interactive">
                <h3>协方差矩阵交互式练习</h3>
                <p>在这个练习中，您将通过实际操作理解协方差矩阵的计算及其在PCA中的作用。</p>

                <div class="data-input-section">
                    <h4>输入数据点</h4>
                    <p>请输入2-3个2维数据点（每行一个点，用逗号分隔X和Y值）：</p>

                    <el-input type="textarea" :rows="4" placeholder="例如：
  1, 2
  3, 4
  2, 3" v-model="rawDataInput" @change="validateInput"></el-input>

                    <div v-if="inputError" class="error-message">
                        {{ inputError }}
                    </div>

                    <el-button type="primary" @click="calculateCovariance" :disabled="!isInputValid || processingData"
                        class="calculate-button">
                        计算协方差矩阵
                    </el-button>
                </div>

                <div v-if="showResults" class="results-section" ref="mathContent">
                    <h4>数据可视化</h4>
                    <div class="visualization-container" ref="dataVisualization"></div>

                    <h4>计算过程</h4>
                    <div class="calculation-steps">
                        <p><strong>步骤1：计算均值</strong></p>
                        <p>$\mu_X = \frac{1}{n}\sum_{i=1}^{n}x_i = {{ meanX.toFixed(2) }}$</p>
                        <p>$\mu_Y = \frac{1}{n}\sum_{i=1}^{n}y_i = {{ meanY.toFixed(2) }}$</p>

                        <p><strong>步骤2：计算协方差矩阵</strong></p>
                        <table class="covariance-table">
                            <tr>
                                <td></td>
                                <td>X</td>
                                <td>Y</td>
                            </tr>
                            <tr>
                                <td>X</td>
                                <td>{{ covMatrix[0][0].toFixed(4) }}</td>
                                <td>{{ covMatrix[0][1].toFixed(4) }}</td>
                            </tr>
                            <tr>
                                <td>Y</td>
                                <td>{{ covMatrix[1][0].toFixed(4) }}</td>
                                <td>{{ covMatrix[1][1].toFixed(4) }}</td>
                            </tr>
                        </table>

                        <p><strong>解读</strong>：</p>
                        <ul>
                            <li>协方差矩阵对角线元素：X和Y的方差</li>
                            <li>非对角线元素：X和Y之间的协方差</li>
                        </ul>

                       <div v-if="eigenResults && eigenResults.length > 0" class="eigenvalue-section">
                            <p><strong>步骤3：计算特征值和特征向量</strong></p>

                            <p><strong>特征值：</strong></p>
                            <ul>
                                <li v-for="(result, index) in eigenResults" :key="'value-' + index">
                                    $\lambda$<sub>{{ index + 1 }}</sub> = {{ result.value.toFixed(4) }}
                                </li>
                            </ul>

                            <p><strong>对应特征向量：</strong></p>
                            <ul>
                                <li v-for="(result, index) in eigenResults" :key="'vector-' + index">
                                    $v$<sub>{{ index + 1 }}</sub> = [{{ result.vector[0].toFixed(4) }}, {{
                                    result.vector[1].toFixed(4) }}]<sup>T</sup>
                                </li>
                            </ul>

                            <p><strong>结论</strong>：这些特征向量就是主成分的方向，特征值表示沿着这些方向的方差大小。</p>
                        </div>
                    </div>

                    <div class="understanding-check">
                        <h4>理解检查</h4>
                        <p>基于您计算的结果，请回答以下问题：</p>
                        <p>特征值大小与主成分关系的正确描述是？</p>

                        <el-radio-group v-model="understandingAnswer" class="understanding-options">
                            <el-radio :label="0">特征值越小，对应的特征向量就是越重要的主成分</el-radio>
                            <el-radio :label="1">特征值越大，对应的特征向量就是越重要的主成分</el-radio>
                            <el-radio :label="2">特征值的大小与主成分的重要性无关</el-radio>
                            <el-radio :label="3">只有特征值等于1的特征向量才是主成分</el-radio>
                        </el-radio-group>

                        <el-button type="primary" @click="checkUnderstanding" :disabled="understandingAnswer === null"
                            class="understanding-submit">
                            提交答案
                        </el-button>
                    </div>
                </div>
            </div>
        </template>
    </base-segment>
</template>

<script>
import BaseSegment from './BaseSegment.vue'
import * as d3 from 'd3'

export default {
    name: 'CovarianceMatrix',
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
                console.log("协方差子组件接受回答", newValue);
                if (newValue) {
                    this.understandingAnswer = Number(newValue);
                    //   this.hasSubmittedAnswer = true;
                    //   this.feedback = '您之前已经完成了这个章节的练习。';
                }
            }
        },
        showResults(val) {
            if (val) {
                this.$nextTick(() => {
                    this.typesetMath()
                })
            }
        },
        eigenResults: {
            handler() {
                this.$nextTick(() => {
                    this.typesetMath()
                })
            },
            deep: true
        }
    },
    data() {
        return {
            title: '3. 协方差矩阵',
            segmentId: 'covariance-matrix',
            content: `
  ## 协方差矩阵：PCA的数学基础
  
  在多维数据分析中，**协方差矩阵**是理解变量间关系的关键工具，也是PCA算法的数学基础。
  
  ### 协方差的概念
  
  **协方差**衡量两个变量之间的线性关系强度和方向。对于变量 $X$ 和 $Y$，它们的协方差计算公式为：
  
  $$\\text{cov}(X,Y) = \\frac{1}{n}\\sum_{i=1}^{n}(x_i - \\mu_X)(y_i - \\mu_Y)$$
  
  其中 $\\mu_X$ 和 $\\mu_Y$ 分别是 $X$ 和 $Y$ 的均值。
  
  协方差的解读：
  - 正值：表示两个变量同向变化（一个增大，另一个也倾向于增大）
  - 负值：表示两个变量反向变化（一个增大，另一个倾向于减小）
  - 接近零：表示两个变量之间几乎没有线性关系
  
  ### 协方差矩阵的结构
  
  对于包含 $p$ 个特征的数据集，协方差矩阵是一个 $p \\times p$ 的对称矩阵，其中第 $(i,j)$ 个元素表示第 $i$ 个特征和第 $j$ 个特征之间的协方差。
  
  对于二维数据，协方差矩阵为：
  
  $$\\Sigma = 
  \\begin{bmatrix} 
  \\text{var}(X) & \\text{cov}(X,Y) \\ 
  \\text{cov}(X,Y) & \\text{var}(Y)
  \\end{bmatrix}$$
  
  ### 协方差矩阵与PCA的关系
  
  PCA算法的数学过程可以总结为以下步骤：
  
  1. **数据中心化**：将每个特征的均值调整为0
  2. **计算协方差矩阵**：使用中心化后的数据
  3. **计算协方差矩阵的特征值和特征向量**：这些特征向量就是主成分方向
  4. **按特征值大小排序特征向量**：特征值越大，对应的特征向量包含的信息越多
  5. **选择前k个特征向量**：构建投影矩阵
  6. **将原始数据投影到新空间**：完成降维
  
  特征值表示沿着特征向量方向的方差大小。较大的特征值意味着该方向上的数据变化更显著，包含更多信息。
  
  在下面的互动练习中，您将亲自计算协方差矩阵，并观察其特征值和特征向量如何与数据分布关联。
        `,
            // 交互数据
            rawDataInput: "1, 2\n3, 4\n2, 3",
            inputError: null,
            isInputValid: true,
            processingData: false,
            showResults: false,

            // 计算结果
            parsedData: [],
            meanX: 0,
            meanY: 0,
            covMatrix: [[0, 0], [0, 0]],
            eigenResults: [],

            // 理解检查
            understandingAnswer: null,
            understandingAttempts: 0,

            // 可视化
            svg: null,
            width: 500,
            height: 400,
            margin: { top: 30, right: 30, bottom: 40, left: 40 }
        };
    },
    methods: {
        typesetMath() {
            this.$nextTick(() => {
                if (window.MathJax && window.MathJax.typesetPromise) {
                    window.MathJax.typesetPromise([this.$refs.mathContent])
                }
            })
        },
        validateInput() {
            this.inputError = null;
            this.isInputValid = true;

            try {
                const lines = this.rawDataInput.trim().split('\n');
                if (lines.length < 2) {
                    this.inputError = "请至少输入2个数据点";
                    this.isInputValid = false;
                    return;
                }

                const parsedPoints = [];

                for (const line of lines) {
                    const parts = line.split(',').map(p => p.trim());
                    if (parts.length !== 2) {
                        this.inputError = `格式不正确: "${line}" - 每行应有两个值，用逗号分隔`;
                        this.isInputValid = false;
                        return;
                    }

                    const x = parseFloat(parts[0]);
                    const y = parseFloat(parts[1]);

                    if (isNaN(x) || isNaN(y)) {
                        this.inputError = `无效的数字: "${line}"`;
                        this.isInputValid = false;
                        return;
                    }

                    parsedPoints.push([x, y]);
                }

                this.parsedData = parsedPoints;
            } catch (e) {
                this.inputError = "解析输入时出错：" + e.message;
                this.isInputValid = false;
            }
        },

        calculateCovariance() {
            this.processingData = true;
            this.validateInput();

            if (!this.isInputValid) {
                this.processingData = false;
                return;
            }

            // 计算均值
            this.meanX = d3.mean(this.parsedData, d => d[0]);
            this.meanY = d3.mean(this.parsedData, d => d[1]);

            // 计算协方差矩阵
            let covXX = 0, covXY = 0, covYY = 0;

            this.parsedData.forEach(point => {
                const diffX = point[0] - this.meanX;
                const diffY = point[1] - this.meanY;

                covXX += diffX * diffX;
                covXY += diffX * diffY;
                covYY += diffY * diffY;
            });

            covXX /= this.parsedData.length;
            covXY /= this.parsedData.length;
            covYY /= this.parsedData.length;

            this.covMatrix = [
                [covXX, covXY],
                [covXY, covYY]
            ];

            // 计算特征值和特征向量
            this.calculateEigen();

            // 显示结果
            this.showResults = true;
            this.processingData = false;

            // 创建可视化
            this.$nextTick(() => {
                this.createVisualization();
            });
        },

        calculateEigen() {
            const covXX = this.covMatrix[0][0];
            const covXY = this.covMatrix[0][1];
            const covYY = this.covMatrix[1][1];

            // 计算特征值
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

                v2x = lambda2 - covYY;
                v2y = covXY;

                // 归一化
                const norm2 = Math.sqrt(v2x * v2x + v2y * v2y);
                v2x /= norm2;
                v2y /= norm2;
            }

            // 存储结果
            this.eigenResults = [
                { value: lambda1, vector: [v1x, v1y] },
                { value: lambda2, vector: [v2x, v2y] }
            ];


            // 按特征值降序排序
            this.eigenResults.sort((a, b) => b.value - a.value);
            console.log("eigenResults", this.eigenResults);
            console.log("eigenResults001", this.eigenResults[0].vector[0].toFixed(4));

        },

        createVisualization() {
    d3.select(this.$refs.dataVisualization).selectAll("*").remove();

    const pointRadius = Math.min(8, Math.max(4, 10 - this.parsedData.length / 2));

    this.svg = d3.select(this.$refs.dataVisualization)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height);

    const container = this.svg.append("g");

    const g = container.append("g")
        .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

    const plotWidth = this.width - this.margin.left - this.margin.right;
    const plotHeight = this.height - this.margin.top - this.margin.bottom;

    const xExtent = d3.extent(this.parsedData, d => d[0]);
    const yExtent = d3.extent(this.parsedData, d => d[1]);

    const maxEigenValue = Math.max(this.eigenResults[0].value, this.eigenResults[1].value);
    const scale = Math.sqrt(maxEigenValue) * 2;

    const xRange = [
        Math.min(xExtent[0], this.meanX - scale),
        Math.max(xExtent[1], this.meanX + scale)
    ];
    const yRange = [
        Math.min(yExtent[0], this.meanY - scale),
        Math.max(yExtent[1], this.meanY + scale)
    ];

    const xScale = d3.scaleLinear().domain(xRange).range([0, plotWidth]).nice();
    const yScale = d3.scaleLinear().domain(yRange).range([plotHeight, 0]).nice();

    const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale);

    const xAxisGroup = g.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${yScale(0)})`)
        .call(xAxis);

    const yAxisGroup = g.append("g")
        .attr("class", "y-axis")
        .attr("transform", `translate(${xScale(0)},0)`)
        .call(yAxis);

    // 轴标签
    const xLabel = g.append("text")
        .attr("class", "x-label")
        .attr("x", plotWidth)
        .attr("y", yScale(0) + 20)
        .style("text-anchor", "end")
        .text("X轴");

    const yLabel = g.append("text")
        .attr("class", "y-label")
        .attr("x", xScale(0) - 10)
        .attr("y", 10)
        .style("text-anchor", "end")
        .text("Y轴");

    // 绘制数据点
    const points = g.selectAll(".data-point")
        .data(this.parsedData)
        .enter()
        .append("circle")
        .attr("class", "data-point")
        .attr("r", pointRadius)
        .style("fill", "#69b3a2")
        .style("opacity", 0.7);

    // 均值点
    const meanPoint = g.append("circle")
        .attr("class", "mean-point")
        .attr("r", pointRadius + 1)
        .style("fill", "#ff7700")
        .style("stroke", "black")
        .style("stroke-width", 1);

    // 特征向量
    const scaleFactor = 1.5 * scale;
    const evLines = g.selectAll(".eigen-line")
        .data(this.eigenResults)
        .enter()
        .append("line")
        .attr("class", (d, i) => `eigen-line eigen-line-${i}`)
        .style("stroke", (d, i) => i === 0 ? "red" : "blue")
        .style("stroke-width", 2)
        .style("stroke-dasharray", "5,5");

    const evLabels = g.selectAll(".eigen-label")
        .data(this.eigenResults)
        .enter()
        .append("text")
        .attr("class", "eigen-label")
        .attr("dx", 10)
        .style("fill", (d, i) => i === 0 ? "red" : "blue")
        .text((d, i) => i === 0 ? "第一主成分" : "第二主成分");

    // 初始化位置
    function updateElements(newXScale, newYScale) {
        xAxisGroup.call(xAxis.scale(newXScale));
        yAxisGroup.call(yAxis.scale(newYScale));

        xAxisGroup.attr("transform", `translate(0,${newYScale(0)})`);
        yAxisGroup.attr("transform", `translate(${newXScale(0)},0)`);

        xLabel.attr("x", plotWidth).attr("y", newYScale(0) + 20);
        yLabel.attr("x", newXScale(0) - 10).attr("y", 10);

        points
            .attr("cx", d => newXScale(d[0]))
            .attr("cy", d => newYScale(d[1]));

        meanPoint
            .attr("cx", newXScale(this.meanX))
            .attr("cy", newYScale(this.meanY));

        evLines
            .attr("x1", d => newXScale(this.meanX - scaleFactor * d.vector[0]))
            .attr("y1", d => newYScale(this.meanY - scaleFactor * d.vector[1]))
            .attr("x2", d => newXScale(this.meanX + scaleFactor * d.vector[0]))
            .attr("y2", d => newYScale(this.meanY + scaleFactor * d.vector[1]));

        evLabels
            .attr("x", d => newXScale(this.meanX + scaleFactor * d.vector[0]))
            .attr("y", d => newYScale(this.meanY + scaleFactor * d.vector[1]));
    }

    // 初始化位置
    updateElements.call(this, xScale, yScale);

    // 缩放行为
    const zoom = d3.zoom()
        .scaleExtent([0.5, 10])
        .on("zoom", (event) => {
            const newXScale = event.transform.rescaleX(xScale);
            const newYScale = event.transform.rescaleY(yScale);
            updateElements.call(this, newXScale, newYScale);
        });

    this.svg.call(zoom);
},

        checkUnderstanding() {
            this.understandingAttempts++;
            const correctAnswer = 1; // 特征值越大，对应的特征向量就是越重要的主成分

            // 向父组件发送答案提交事件
            this.$emit('answer-submitted', this.understandingAnswer);

            if (this.understandingAnswer === correctAnswer) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "回答正确！",
                    "特征值确实表示沿着对应特征向量方向的方差大小。特征值越大，表示该方向上的数据变化越显著，包含的信息量越大，因此对应的特征向量作为主成分的重要性越高。",
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
                    hint = "提示：想想PCA的目标是什么？它试图寻找数据中哪些方向的信息？";
                }

                this.$refs.baseSegment.showResponse(
                    "回答不正确",
                    `请再思考特征值和方差之间的关系。${hint}`,
                    "error"
                );
            }
        },

        onCompleted() {
            // 通知父组件此片段已完成
            this.$emit('completed', this.segmentId);
        }
    },
    updated() {
        this.typesetMath()
    },
    mounted() {
        // 初始验证输入
        this.validateInput();
        this.typesetMath()
    },
    beforeDestroy() {
        // 清理D3资源
        if (this.svg) {
            d3.select(this.$refs.dataVisualization).selectAll("*").remove();
        }
    },

}
</script>

<style scoped>
.covariance-interactive {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.data-input-section {
    margin-bottom: 20px;
}

.error-message {
    color: #f56c6c;
    margin-top: 5px;
    font-size: 14px;
}

.calculate-button {
    margin-top: 15px;
}

.results-section {
    margin-top: 20px;
    border-top: 1px dashed #dcdfe6;
    padding-top: 20px;
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

.calculation-steps {
    margin: 20px 0;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.covariance-table {
    margin: 15px 0;
    border-collapse: collapse;
    width: auto;
}

.covariance-table td {
    border: 1px solid #dcdfe6;
    padding: 8px 15px;
    text-align: center;
}

.covariance-table tr:first-child,
.covariance-table td:first-child {
    background-color: #f5f7fa;
    font-weight: bold;
}

.eigenvalue-section {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px dashed #dcdfe6;
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
</style>