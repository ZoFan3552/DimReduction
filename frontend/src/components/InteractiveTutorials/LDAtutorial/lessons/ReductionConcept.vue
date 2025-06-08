<!-- DimensionalityReductionConcept.vue - 降维概念教学组件 -->
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

        <!-- 互动区域 - D3.js交互式可视化 -->
        <div v-if="!isCompleted" class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-data-line"></i> 互动练习：探索2D到1D的投影
            </h3>

            <p class="interaction-instruction">
                拖动下方的投影线，尝试找到一个投影方向，使得蓝色点和橙色点在投影后能够被最好地分离开。
                <br>完成后，点击"检查投影"按钮，看看你的解决方案如何。
            </p>

            <div class="visualization-container">
                <div id="dimension-reduction-viz" ref="d3Container"></div>

                <div class="viz-controls">
                    <p v-if="projectionAngle !== null">
                        当前投影角度: {{ Math.round(projectionAngle * 180 / Math.PI) }}°
                    </p>
                    <el-button type="primary" @click="checkProjection" :disabled="projectionChecked">
                        检查投影
                    </el-button>
                    <el-button type="info" @click="resetVisualization" :disabled="projectionChecked">
                        重置
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

            <div class="action-buttons">
                <el-button type="primary" @click="completeSection">
                    继续学习 <i class="el-icon-arrow-right"></i>
                </el-button>
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
    name: 'DimensionalityReductionConcept',
    props: {
        sectionId: {
            type: String,
            default: 'dimensionality-reduction'
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
            title: "降维概念",
            markdownContent: `
  # 降维概念
  
  ## 什么是降维？
  
  降维是将高维度数据转换为低维度表示的过程，同时保留数据的重要特征和结构。
  
  
  ## 为什么需要降维？
  
  在机器学习和数据分析中，降维是一个重要的预处理步骤，主要有以下几个原因：
  
  ### 1. 克服维度灾难
  
  高维数据会导致"维度灾难"问题，表现为：
  
  - 数据点之间的距离度量变得不直观
  - 算法计算复杂度急剧增加
  - 需要的训练样本数量呈指数级增长
  
  ### 2. 数据可视化
  
  人类只能直观理解2D或3D数据，降维可以帮助我们可视化高维数据，发现数据中的模式和结构。
  
  ### 3. 减少噪声和冗余
  
  真实数据通常存在大量冗余和噪声特征，降维可以帮助：
  
  - 提取更紧凑的数据表示
  - 减少过拟合风险
  - 提高算法性能
  
  ### 4. 计算效率
  
  降低数据维度可以：
  
  - 减少存储需求
  - 加速模型训练
  - 提高推理速度
  
  ## 主要降维方法
  
  降维方法可以分为两大类：
  
  ### 线性降维方法
  - **主成分分析(PCA)** - 基于最大方差
  - **线性判别分析(LDA)** - 基于类别区分
  - **因子分析(FA)** - 基于潜在变量模型
  
  ### 非线性降维方法
  - **t-SNE** - 基于概率分布的相似性
  - **流形学习** - 如Isomap、LLE等
  - **自编码器** - 基于神经网络
  
  ## 投影作为降维的概念
  
  降维最直观的理解方式是将数据投影到低维空间：
  
  - 在2D空间中，点可以投影到一条直线上(1D)
  - 在3D空间中，点可以投影到一个平面上(2D)
  
  投影方向的选择决定了降维的质量 - 好的投影方向应该保留数据中最重要的信息。
  
  对于分类问题，好的投影方向应该使不同类别的数据在投影后尽可能分开，这正是LDA的核心思想。
        `,
            isCompleted: false,

            // D3可视化数据
            svg: null,
            width: 600,
            height: 400,
            margin: { top: 20, right: 20, bottom: 30, left: 40 },
            data: null,
            projectionLine: null,
            projectionAxis: null,
            projectionAngle: null,
            optimalAngle: Math.PI / 4, // 最佳投影角度（示例值，实际会根据数据计算）
            projectionChecked: false,

            // 回应部分数据
            showResponse: false,
            isCorrect: false,
            response: '',
            scorePercentage: 0
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
            return this.scorePercentage >= 70 ? 'el-icon-check correct' : 'el-icon-warning-outline warning';
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
        initVisualization() {
            // 生成两类2D数据点
            this.generateData();

            const containerWidth = this.$refs.d3Container.clientWidth || this.width;
            const width = containerWidth - this.margin.left - this.margin.right;
            const height = this.height - this.margin.top - this.margin.bottom;

            // 创建SVG容器
            this.svg = d3.select("#dimension-reduction-viz")
                .append("svg")
                .attr("width", containerWidth)
                .attr("height", this.height)
                .append("g")
                .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

            // 创建X和Y比例尺
            const xExtent = d3.extent(this.data, d => d.x);
            const yExtent = d3.extent(this.data, d => d.y);
            const padding = 1.2; // 添加一些填充以便看到所有点

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] * padding, xExtent[1] * padding])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] * padding, yExtent[1] * padding])
                .range([height, 0]);

            // 绘制轴
            this.svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", `translate(0,${height})`)
                .call(d3.axisBottom(xScale));

            this.svg.append("g")
                .attr("class", "y-axis")
                .call(d3.axisLeft(yScale));

            // 绘制数据点
            this.svg.selectAll(".datapoint")
                .data(this.data)
                .enter()
                .append("circle")
                .attr("class", "datapoint")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 5)
                .attr("fill", d => d.class === 0 ? "#409EFF" : "#E6A23C")
                .attr("stroke", "white")
                .attr("stroke-width", 1);

            // 添加投影线（默认为45度角）
            const lineLength = Math.max(Math.abs(xExtent[1] - xExtent[0]), Math.abs(yExtent[1] - yExtent[0])) * padding;
            this.projectionAngle = Math.PI / 4; // 初始角度45度

            const lineStart = {
                x: 0 - Math.cos(this.projectionAngle) * lineLength,
                y: 0 - Math.sin(this.projectionAngle) * lineLength
            };

            const lineEnd = {
                x: 0 + Math.cos(this.projectionAngle) * lineLength,
                y: 0 + Math.sin(this.projectionAngle) * lineLength
            };

            this.projectionLine = this.svg.append("line")
                .attr("class", "projection-line")
                .attr("x1", xScale(lineStart.x))
                .attr("y1", yScale(lineStart.y))
                .attr("x2", xScale(lineEnd.x))
                .attr("y2", yScale(lineEnd.y))
                .attr("stroke", "#67C23A")
                .attr("stroke-width", 2)
                .attr("stroke-dasharray", "5,5");

            // 添加拖动功能
            const drag = d3.drag()
                .on("drag", (event) => {
                    if (this.projectionChecked) return;

                    const mouseX = xScale.invert(event.x);
                    const mouseY = yScale.invert(event.y);

                    // 计算新的投影角度
                    this.projectionAngle = Math.atan2(mouseY, mouseX);

                    // 更新投影线
                    const newLineStart = {
                        x: 0 - Math.cos(this.projectionAngle) * lineLength,
                        y: 0 - Math.sin(this.projectionAngle) * lineLength
                    };

                    const newLineEnd = {
                        x: 0 + Math.cos(this.projectionAngle) * lineLength,
                        y: 0 + Math.sin(this.projectionAngle) * lineLength
                    };

                    this.projectionLine
                        .attr("x1", xScale(newLineStart.x))
                        .attr("y1", yScale(newLineStart.y))
                        .attr("x2", xScale(newLineEnd.x))
                        .attr("y2", yScale(newLineEnd.y));

                    // 更新投影轴上的投影点
                    if (this.projectionAxis) {
                        this.updateProjectedPoints(xScale, yScale, width, height);
                    }
                });

            // 添加拖动手柄
            this.svg.append("circle")
                .attr("cx", xScale(lineEnd.x))
                .attr("cy", yScale(lineEnd.y))
                .attr("r", 8)
                .attr("fill", "#67C23A")
                .style("cursor", "pointer")
                .call(drag);

            // 添加投影轴
            this.projectionAxis = this.svg.append("line")
                .attr("class", "projection-axis")
                .attr("x1", 0)
                .attr("y1", height + 20)
                .attr("x2", width)
                .attr("y2", height + 20)
                .attr("stroke", "#909399")
                .attr("stroke-width", 2);

            // 初始绘制投影点
            this.updateProjectedPoints(xScale, yScale, width, height);

            // 计算"最佳"投影方向（这里只是演示，实际应该根据LDA原理计算）
            this.calculateOptimalDirection();
        },

        generateData() {
            // 生成两类二维数据
            this.data = [];

            // 第一类 - 围绕 (2,2) 的点
            for (let i = 0; i < 30; i++) {
                this.data.push({
                    x: 2 + (Math.random() - 0.5) * 2,
                    y: 2 + (Math.random() - 0.5) * 3,
                    class: 0
                });
            }

            // 第二类 - 围绕 (4,6) 的点
            for (let i = 0; i < 30; i++) {
                this.data.push({
                    x: 4 + (Math.random() - 0.5) * 2,
                    y: 6 + (Math.random() - 0.5) * 3,
                    class: 1
                });
            }
        },

        updateProjectedPoints(xScale, yScale, width, height) {
            // 移除之前的投影点
            this.svg.selectAll(".projected-point").remove();

            // 将每个数据点投影到投影线上
            const projectedPoints = this.data.map(d => {
                // 计算投影
                const projectedValue = d.x * Math.cos(this.projectionAngle) + d.y * Math.sin(this.projectionAngle);
                return {
                    value: projectedValue,
                    class: d.class,
                    original: d
                };
            });

            // 找到投影值的范围，用于缩放
            const projRange = d3.extent(projectedPoints, d => d.value);
            const projScale = d3.scaleLinear()
                .domain(projRange)
                .range([0, width]);

            // 在投影轴上绘制投影点
            this.svg.selectAll(".projected-point")
                .data(projectedPoints)
                .enter()
                .append("circle")
                .attr("class", "projected-point")
                .attr("cx", d => projScale(d.value))
                .attr("cy", height + 20)
                .attr("r", 5)
                .attr("fill", d => d.class === 0 ? "#409EFF" : "#E6A23C")
                .attr("stroke", "white")
                .attr("stroke-width", 1);

            // 绘制从原始点到投影点的连接线
            this.svg.selectAll(".projection-connector").remove();

            this.svg.selectAll(".projection-connector")
                .data(this.data)
                .enter()
                .append("line")
                .attr("class", "projection-connector")
                .attr("x1", d => xScale(d.x))
                .attr("y1", d => yScale(d.y))
                .attr("x2", (d, i) => projScale(projectedPoints[i].value))
                .attr("y2", height + 20)
                .attr("stroke", d => d.class === 0 ? "#409EFF" : "#E6A23C")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "2,2")
                .style("opacity", 0.4);
        },

        calculateOptimalDirection() {
            // 在实际应用中，这里应该使用LDA算法计算最佳投影方向
            // 为了简化演示，我们假设最佳方向已知

            // 计算每个类的均值
            const class0Points = this.data.filter(d => d.class === 0);
            const class1Points = this.data.filter(d => d.class === 1);

            const mean0 = {
                x: d3.mean(class0Points, d => d.x),
                y: d3.mean(class0Points, d => d.y)
            };

            const mean1 = {
                x: d3.mean(class1Points, d => d.x),
                y: d3.mean(class1Points, d => d.y)
            };

            // 计算两类均值的差向量
            const diff = {
                x: mean1.x - mean0.x,
                y: mean1.y - mean0.y
            };

            // 归一化差向量，得到投影方向
            const magnitude = Math.sqrt(diff.x * diff.x + diff.y * diff.y);
            const direction = {
                x: diff.x / magnitude,
                y: diff.y / magnitude
            };

            // 计算投影角度
            this.optimalAngle = Math.atan2(direction.y, direction.x);
        },

        checkProjection() {
            this.projectionChecked = true;

            // 计算用户选择的投影与最佳投影的接近程度
            const angleDiff = Math.abs(this.projectionAngle - this.optimalAngle);
            const normalizedDiff = Math.min(angleDiff, Math.PI - angleDiff) / (Math.PI / 2);
            this.scorePercentage = Math.round((1 - normalizedDiff) * 100);

            // 生成反馈
            let feedback;
            if (this.scorePercentage >= 90) {
                feedback = `
  ### 🌟 优秀的投影！
  
  你找到了接近最佳的投影方向，评分：${this.scorePercentage}%
  
  你选择的投影角度能够很好地分离两个类别。在LDA中，我们正是寻找这样的投影方向，使得：
  - 不同类别在投影后尽可能分开（最大化类间距离）
  - 同一类别的样本在投影后尽可能聚集（最小化类内距离）
  
  LDA通过数学公式自动找到这样的最佳投影方向，而不需要手动尝试。
          `;
            } else if (this.scorePercentage >= 70) {
                feedback = `
  ### 👍 不错的尝试！
  
  你的投影方向相当不错，评分：${this.scorePercentage}%
  
  还可以进一步优化：理想的投影方向应该使投影后的两个类别尽可能分开，同时使每个类别内部的点尽可能聚集。
  
  LDA算法会自动计算出"最佳"投影方向，正是基于这一原理。
          `;
            } else {
                feedback = `
  ### 🤔 可以做得更好！
  
  你的投影评分：${this.scorePercentage}%
  
  尝试寻找一个方向，使投影后的两个类别点分隔得更开。观察两类数据点的分布，寻找连接它们均值的方向可能是一个好的起点。
  
  LDA算法会自动找到这个最佳方向，这正是LDA作为降维算法的核心优势。
          `;
            }

            this.response = feedback;
            this.showResponse = true;

            // 在可视化中显示最佳投影方向
            this.showOptimalDirection();
        },

        showOptimalDirection() {
            const containerWidth = this.$refs.d3Container.clientWidth || this.width;
            const width = containerWidth - this.margin.left - this.margin.right;
            const height = this.height - this.margin.top - this.margin.bottom;

            // 创建X和Y比例尺
            const xExtent = d3.extent(this.data, d => d.x);
            const yExtent = d3.extent(this.data, d => d.y);
            const padding = 1.2;

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] * padding, xExtent[1] * padding])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] * padding, yExtent[1] * padding])
                .range([height, 0]);

            // 添加最佳投影线
            const lineLength = Math.max(Math.abs(xExtent[1] - xExtent[0]), Math.abs(yExtent[1] - yExtent[0])) * padding;

            const lineStart = {
                x: 0 - Math.cos(this.optimalAngle) * lineLength,
                y: 0 - Math.sin(this.optimalAngle) * lineLength
            };

            const lineEnd = {
                x: 0 + Math.cos(this.optimalAngle) * lineLength,
                y: 0 + Math.sin(this.optimalAngle) * lineLength
            };

            this.svg.append("line")
                .attr("class", "optimal-line")
                .attr("x1", xScale(lineStart.x))
                .attr("y1", yScale(lineStart.y))
                .attr("x2", xScale(lineEnd.x))
                .attr("y2", yScale(lineEnd.y))
                .attr("stroke", "#F56C6C")
                .attr("stroke-width", 2)
                .attr("stroke-dasharray", "5,5");

            // 添加说明文本
            this.svg.append("text")
                .attr("x", xScale(lineEnd.x))
                .attr("y", yScale(lineEnd.y) - 10)
                .attr("text-anchor", "end")
                .attr("fill", "#F56C6C")
                .text("最佳投影方向");
        },

        resetVisualization() {
            // 移除原SVG并重新初始化
            d3.select("#dimension-reduction-viz svg").remove();
            this.projectionChecked = false;
            this.showResponse = false;
            this.initVisualization();
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

.markdown-content img {
    max-width: 100%;
    border-radius: 4px;
    margin: 10px 0;
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

.interaction-instruction {
    margin-bottom: 20px;
    font-size: 14px;
    color: #606266;
    line-height: 1.6;
}

.visualization-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 15px;
}

#dimension-reduction-viz {
    width: 100%;
    max-width: 600px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background-color: white;
    margin-bottom: 15px;
}

.viz-controls {
    display: flex;
    align-items: center;
    gap: 10px;
}

.viz-controls p {
    margin: 0;
    font-size: 14px;
    color: #606266;
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

.response-icon.warning {
    color: #E6A23C;
}

.response-message {
    flex: 1;
}

.action-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
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
</style>