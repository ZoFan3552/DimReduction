<!-- LDAVisualizationExamples.vue - LDA可视化示例教学组件 -->
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

        <!-- 互动区域 - LDA交互式可视化 -->
        <div v-if="!isCompleted" class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-data-line"></i> 互动练习：LDA降维可视化
            </h3>

            <p class="interaction-description">
                使用下面的交互式工具，探索LDA降维的效果以及各参数对于降维结果的影响。
            </p>

            <!-- <div class="visualization-container">
                <div class="control-panel">
                    <h4>数据集选择</h4>
                    <el-radio-group v-model="selectedDataset" @change="updateVisualization">
                        <el-radio :label="'iris'">鸢尾花数据集</el-radio>
                        <el-radio :label="'wine'">葡萄酒数据集</el-radio>
                        <el-radio :label="'digits'">手写数字数据集</el-radio>
                    </el-radio-group>

                    <h4>预处理选项</h4>
                    <el-checkbox v-model="useStandardization" @change="updateVisualization">标准化数据</el-checkbox>

                    <h4>可视化设置</h4>
                    <div class="control-group">
                        <span class="control-label">显示类别个数:</span>
                        <el-slider v-model="numClassesToShow" :min="2" :max="maxClasses" :step="1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="control-group">
                        <span class="control-label">点大小:</span>
                        <el-slider v-model="pointSize" :min="3" :max="10" :step="1"
                            @change="updateVisualization"></el-slider>
                    </div>

                    <div class="dataset-info">
                        <h4>当前数据集信息</h4>
                        <p><strong>名称:</strong> {{ datasetInfo.name }}</p>
                        <p><strong>类别数:</strong> {{ datasetInfo.numClasses }}</p>
                        <p><strong>特征数:</strong> {{ datasetInfo.numFeatures }}</p>
                        <p><strong>样本数:</strong> {{ datasetInfo.numSamples }}</p>
                    </div>

                    <div class="lda-info">
                        <h4>LDA信息</h4>
                        <p><strong>投影维度:</strong> {{ numClassesToShow - 1 }}</p>
                        <p><strong>类内散布矩阵条件数:</strong> {{ ldaInfo.swCondition.toExponential(2) }}</p>
                        <p><strong>特征值占比:</strong></p>
                        <div class="explained-variance-bars">
                            <div v-for="(value, index) in ldaInfo.explainedVarianceRatio" :key="index"
                                class="variance-bar" :style="{ width: `${value * 100}%` }"
                                :title="`特征值${index + 1}: ${(value * 100).toFixed(2)}%`"></div>
                        </div>
                    </div>
                </div>

                <div class="visualization-panel">
                    <div class="vis-tabs">
                        <el-tabs v-model="activeVisTab">
                            <el-tab-pane label="2D可视化" name="2d">
                                <div id="lda-2d-viz" ref="lda2dContainer"></div>
                            </el-tab-pane>
                            <el-tab-pane label="3D可视化" name="3d" v-if="numClassesToShow >= 4">
                                <div id="lda-3d-viz" ref="lda3dContainer"></div>
                            </el-tab-pane>
                            <el-tab-pane label="原始数据PCA" name="pca">
                                <div id="pca-viz" ref="pcaContainer"></div>
                            </el-tab-pane>
                        </el-tabs>
                    </div>
                </div>
            </div> -->

            <div class="interactive-quiz">
                <h4>基于你的探索，回答以下问题:</h4>

                <div class="quiz-item">
                    <p class="question">1. 对于鸢尾花数据集，以下哪种方法产生了最好的类别分离效果？</p>
                    <el-radio-group v-model="quizAnswers[0]">
                        <el-radio :label="0">标准化后的PCA</el-radio>
                        <el-radio :label="1">未标准化的PCA</el-radio>
                        <el-radio :label="2">标准化后的LDA</el-radio>
                        <el-radio :label="3">未标准化的LDA</el-radio>
                    </el-radio-group>
                </div>

                <div class="quiz-item">
                    <p class="question">2. 当类别数量增加时，LDA的最大可能投影维度会如何变化？</p>
                    <el-radio-group v-model="quizAnswers[1]">
                        <el-radio :label="0">保持不变</el-radio>
                        <el-radio :label="1">随类别数量增加而增加</el-radio>
                        <el-radio :label="2">随类别数量增加而减少</el-radio>
                        <el-radio :label="3">与类别数量无关</el-radio>
                    </el-radio-group>
                </div>

                <div class="quiz-item">
                    <p class="question">3. 从实验结果来看，LDA相对于PCA的主要优势是什么？</p>
                    <el-radio-group v-model="quizAnswers[2]">
                        <el-radio :label="0">LDA总是能提取更多的特征</el-radio>
                        <el-radio :label="1">LDA总能保留更多的原始数据方差</el-radio>
                        <el-radio :label="2">LDA更好地保留了类别间的可分性</el-radio>
                        <el-radio :label="3">LDA计算速度更快</el-radio>
                    </el-radio-group>
                </div>

                <div class="quiz-actions">
                    <el-button type="primary" @click="checkAnswers" :disabled="!allQuestionsAnswered || quizChecked">
                        提交答案
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

            <div class="action-buttons" v-if="quizCorrect">
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
// import * as d3 from 'd3';

// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}

export default {
    name: 'LDAVisualizationExamples',
    props: {
        sectionId: {
            type: String,
            default: 'lda-visualization'
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
            title: "LDA可视化示例",
            markdownContent: `
  # LDA可视化示例
  
  将理论付诸实践，本节我们将通过可视化LDA的应用效果，加深对算法的理解。通过观察LDA对不同数据集的降维结果，我们可以直观地体会LDA在分类和降维方面的优势。
  
  ## LDA的可视化意义
  
  可视化对于理解和评估降维算法至关重要，它可以帮助我们：
  
  1. 直观地观察数据降维后的分布情况
  2. 对比不同降维方法（如LDA和PCA）的效果差异
  3. 评估类别间的可分离程度
  4. 检测可能的异常值或错误分类样本
  
  ## 常用数据集的LDA应用
  
  ### 1. 鸢尾花数据集 (Iris)
  
  鸢尾花数据集包含3个类别的鸢尾花，每个样本有4个特征（萼片长度、萼片宽度、花瓣长度、花瓣宽度）。这是测试分类算法的经典数据集。
  
  使用LDA将4维特征降至2维后，我们通常可以观察到三个类别的良好分离，特别是其中一个类别（Setosa）与其他两个类别的明显区分。
  
  ### 2. 葡萄酒数据集 (Wine)
  
  葡萄酒数据集包含3种不同品种的葡萄酒，每个样本有13个化学成分特征。LDA在这个数据集上通常表现出色，可以将13维特征有效地投影到2维空间，同时保持类别分离。
  
  ### 3. 手写数字数据集 (Digits)
  
  手写数字数据集包含0-9共10个类别的手写数字图像，每个图像被表示为64维特征向量。对于这样的高维数据，LDA可以将其降至最多9维（类别数-1），保留类别判别信息。
  
  ## LDA与PCA的可视化对比
  
  与无监督的PCA不同，LDA利用类别信息进行降维，因此在保持类别分离方面通常有更好的表现：
  
  - **PCA**：寻找数据方差最大的方向，不考虑类别信息
  - **LDA**：寻找能最大化类别分离的方向，利用监督信息
  
  通过可视化对比，我们通常可以观察到LDA在类别分离方面的优势，尤其是当类内变异小而类间差异大时。
  
  在下面的互动练习中，你可以通过调整参数，探索LDA在不同数据集上的表现，并将其与PCA进行对比。
        `,
            isCompleted: false,

            // 可视化数据
            selectedDataset: 'iris',
            useStandardization: true,
            numClassesToShow: 3,
            pointSize: 5,
            activeVisTab: '2d',

            // 数据集和LDA信息
            datasetInfo: {
                name: "鸢尾花数据集",
                numClasses: 3,
                numFeatures: 4,
                numSamples: 150
            },
            maxClasses: 3,
            ldaInfo: {
                swCondition: 1.5e3,
                explainedVarianceRatio: [0.7, 0.3]
            },

            // 可视化对象
            svg2d: null,
            svg3d: null,
            svgPca: null,

            // 问题回答
            quizAnswers: [null, null, null],
            correctAnswers: [2, 1, 2],
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
        },
        allQuestionsAnswered() {
            return this.quizAnswers.every(answer => answer !== null);
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const completedSections = this.getCompletedSections();
        this.isCompleted = completedSections.includes(this.sectionId);

        if (!this.isCompleted) {
            // 初始化可视化
            this.$nextTick(() => {
                // this.initVisualization();
                // this.updateVisualization();
            });
        }
    },
    methods: {
        // initVisualization() {
        //     // 初始化2D LDA可视化
        //     const container2d = this.$refs.lda2dContainer;
        //     const width2d = container2d.clientWidth || 500;
        //     const height2d = 400;

        //     this.svg2d = d3.select("#lda-2d-viz")
        //         .append("svg")
        //         .attr("width", width2d)
        //         .attr("height", height2d);

        //     // 初始化3D LDA可视化（如果需要）
        //     if (this.$refs.lda3dContainer) {
        //         const container3d = this.$refs.lda3dContainer;
        //         const width3d = container3d.clientWidth || 500;
        //         const height3d = 400;

        //         this.svg3d = d3.select("#lda-3d-viz")
        //             .append("svg")
        //             .attr("width", width3d)
        //             .attr("height", height3d);
        //     }

        //     // 初始化PCA可视化
        //     const containerPca = this.$refs.pcaContainer;
        //     const widthPca = containerPca.clientWidth || 500;
        //     const heightPca = 400;

        //     this.svgPca = d3.select("#pca-viz")
        //         .append("svg")
        //         .attr("width", widthPca)
        //         .attr("height", heightPca);

        //     // 根据数据集更新界面信息
        //     this.updateDatasetInfo();
        // },

        // updateDatasetInfo() {
        //     // 更新数据集信息
        //     switch (this.selectedDataset) {
        //         case 'iris':
        //             this.datasetInfo = {
        //                 name: "鸢尾花数据集",
        //                 numClasses: 3,
        //                 numFeatures: 4,
        //                 numSamples: 150
        //             };
        //             this.maxClasses = 3;
        //             this.numClassesToShow = Math.min(this.numClassesToShow, this.maxClasses);
        //             break;
        //         case 'wine':
        //             this.datasetInfo = {
        //                 name: "葡萄酒数据集",
        //                 numClasses: 3,
        //                 numFeatures: 13,
        //                 numSamples: 178
        //             };
        //             this.maxClasses = 3;
        //             this.numClassesToShow = Math.min(this.numClassesToShow, this.maxClasses);
        //             break;
        //         case 'digits':
        //             this.datasetInfo = {
        //                 name: "手写数字数据集",
        //                 numClasses: 10,
        //                 numFeatures: 64,
        //                 numSamples: 1797
        //             };
        //             this.maxClasses = 10;
        //             break;
        //     }

        //     // 更新LDA信息
        //     this.updateLdaInfo();
        // },

        // updateLdaInfo() {
        //     // 这里是模拟的LDA信息，在实际应用中应该根据真实计算结果更新
        //     switch (this.selectedDataset) {
        //         case 'iris':
        //             this.ldaInfo = {
        //                 swCondition: this.useStandardization ? 1.5e2 : 1.5e3,
        //                 explainedVarianceRatio: [0.7, 0.3]
        //             };
        //             break;
        //         case 'wine':
        //             this.ldaInfo = {
        //                 swCondition: this.useStandardization ? 2.3e2 : 5.7e4,
        //                 explainedVarianceRatio: [0.65, 0.35]
        //             };
        //             break;
        //         case 'digits': {
        //             // 根据显示的类别数调整方差比例
        //             const varRatio = [];
        //             const total = this.numClassesToShow - 1;
        //             for (let i = 0; i < total; i++) {
        //                 if (i === 0) varRatio.push(0.4);
        //                 else if (i === 1) varRatio.push(0.3);
        //                 else varRatio.push((0.3 / (total - 2)).toFixed(2));
        //             }

        //             this.ldaInfo = {
        //                 swCondition: this.useStandardization ? 1.2e3 : 8.4e6,
        //                 explainedVarianceRatio: varRatio
        //             };
        //         }

        //             break;
        //     }
        // },

        // updateVisualization() {
        //     // 更新数据集信息
        //     this.updateDatasetInfo();

        //     // 生成模拟数据
        //     const generateData = () => {
        //         const result = {
        //             lda2d: [],
        //             lda3d: [],
        //             pca2d: []
        //         };

        //         // 根据数据集生成不同的模拟数据点
        //         for (let c = 0; c < this.numClassesToShow; c++) {
        //             const numPoints = 30; // 每个类别的点数
        //             const baseX = (c % 3) * 4 - 4;
        //             const baseY = Math.floor(c / 3) * 4 - 2;

        //             for (let i = 0; i < numPoints; i++) {
        //                 // LDA 2D投影 - 类别分离良好
        //                 const ldaX = baseX + (Math.random() - 0.5) * 1.5;
        //                 const ldaY = baseY + (Math.random() - 0.5) * 1.5;

        //                 result.lda2d.push({
        //                     x: ldaX,
        //                     y: ldaY,
        //                     class: c
        //                 });

        //                 // LDA 3D投影（如果需要）
        //                 if (this.numClassesToShow >= 4) {
        //                     const ldaZ = c % 2 === 0 ? 2 + Math.random() : -2 + Math.random();

        //                     result.lda3d.push({
        //                         x: ldaX,
        //                         y: ldaY,
        //                         z: ldaZ,
        //                         class: c
        //                     });
        //                 }

        //                 // PCA 2D投影 - 类别重叠较多
        //                 let pcaX, pcaY;

        //                 if (this.selectedDataset === 'iris') {
        //                     // 鸢尾花数据集的PCA投影模拟 - 有一个类别分离较好
        //                     if (c === 0) {
        //                         pcaX = -4 + Math.random() * 2;
        //                         pcaY = -2 + Math.random() * 4;
        //                     } else {
        //                         pcaX = -1 + Math.random() * 6;
        //                         pcaY = -2 + Math.random() * 4;
        //                     }
        //                 } else {
        //                     // 其他数据集的PCA投影模拟 - 类别重叠较多
        //                     pcaX = -3 + Math.random() * 6 + c * 1.5;
        //                     pcaY = -3 + Math.random() * 6;
        //                 }

        //                 result.pca2d.push({
        //                     x: pcaX,
        //                     y: pcaY,
        //                     class: c
        //                 });
        //             }
        //         }

        //         return result;
        //     };

        //     const data = generateData();

        //     // 绘制2D LDA可视化
        //     this.draw2DLDA(data.lda2d);

        //     // 绘制3D LDA可视化（如果需要）
        //     if (this.numClassesToShow >= 4 && this.svg3d) {
        //         this.draw3DLDA(data.lda3d);
        //     }

        //     // 绘制PCA可视化
        //     this.drawPCA(data.pca2d);
        // },

        // draw2DLDA(data) {
        //     // 清除已有内容
        //     this.svg2d.selectAll("*").remove();

        //     const width = this.svg2d.attr("width");
        //     const height = this.svg2d.attr("height");
        //     const margin = { top: 30, right: 30, bottom: 40, left: 50 };

        //     // 创建比例尺
        //     const xExtent = d3.extent(data, d => d.x);
        //     const yExtent = d3.extent(data, d => d.y);
        //     const padding = 1.2;

        //     const xScale = d3.scaleLinear()
        //         .domain([xExtent[0] * padding, xExtent[1] * padding])
        //         .range([margin.left, width - margin.right]);

        //     const yScale = d3.scaleLinear()
        //         .domain([yExtent[0] * padding, yExtent[1] * padding])
        //         .range([height - margin.bottom, margin.top]);

        //     // 添加坐标轴
        //     const xAxis = d3.axisBottom(xScale);
        //     const yAxis = d3.axisLeft(yScale);

        //     this.svg2d.append("g")
        //         .attr("transform", `translate(0,${height - margin.bottom})`)
        //         .call(xAxis);

        //     this.svg2d.append("g")
        //         .attr("transform", `translate(${margin.left},0)`)
        //         .call(yAxis);

        //     // 添加坐标轴标签
        //     this.svg2d.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("x", width / 2)
        //         .attr("y", height - 5)
        //         .text("LD1");

        //     this.svg2d.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("transform", "rotate(-90)")
        //         .attr("x", -height / 2)
        //         .attr("y", 15)
        //         .text("LD2");

        //     // 添加标题
        //     this.svg2d.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("x", width / 2)
        //         .attr("y", 15)
        //         .text("LDA 2D可视化")
        //         .style("font-weight", "bold");

        //     // 颜色比例尺
        //     const colors = d3.schemeCategory10;

        //     // 绘制数据点
        //     this.svg2d.selectAll("circle")
        //         .data(data)
        //         .enter()
        //         .append("circle")
        //         .attr("cx", d => xScale(d.x))
        //         .attr("cy", d => yScale(d.y))
        //         .attr("r", this.pointSize)
        //         .attr("fill", d => colors[d.class])
        //         .attr("opacity", 0.7)
        //         .attr("stroke", "white")
        //         .attr("stroke-width", 0.5);

        //     // 添加图例
        //     const legend = this.svg2d.selectAll(".legend")
        //         .data(d3.range(this.numClassesToShow))
        //         .enter()
        //         .append("g")
        //         .attr("class", "legend")
        //         .attr("transform", (d, i) => `translate(0,${i * 20 + margin.top})`);

        //     legend.append("rect")
        //         .attr("x", width - margin.right + 10)
        //         .attr("width", 10)
        //         .attr("height", 10)
        //         .attr("fill", d => colors[d]);

        //     legend.append("text")
        //         .attr("x", width - margin.right + 25)
        //         .attr("y", 5)
        //         .attr("dy", ".35em")
        //         .style("font-size", "10px")
        //         .text(d => `类别 ${d}`);
        // },

        // draw3DLDA(data) {
        //     // 简化版的3D可视化，实际中可以使用Three.js等库实现更好的3D效果
        //     // 这里只实现一个简单的2D投影版本

        //     // 清除已有内容
        //     this.svg3d.selectAll("*").remove();

        //     const width = this.svg3d.attr("width");
        //     const height = this.svg3d.attr("height");
        //     const margin = { top: 30, right: 30, bottom: 40, left: 50 };

        //     // 创建比例尺
        //     const xExtent = d3.extent(data, d => d.x);
        //     const yExtent = d3.extent(data, d => d.y);
        //     const zExtent = d3.extent(data, d => d.z);
        //     const padding = 1.2;

        //     const xScale = d3.scaleLinear()
        //         .domain([xExtent[0] * padding, xExtent[1] * padding])
        //         .range([margin.left, width - margin.right]);

        //     const yScale = d3.scaleLinear()
        //         .domain([yExtent[0] * padding, yExtent[1] * padding])
        //         .range([height - margin.bottom, margin.top]);

        //     // 使用点大小表示z值
        //     const sizeScale = d3.scaleLinear()
        //         .domain(zExtent)
        //         .range([this.pointSize / 2, this.pointSize * 2]);

        //     // 添加坐标轴
        //     const xAxis = d3.axisBottom(xScale);
        //     const yAxis = d3.axisLeft(yScale);

        //     this.svg3d.append("g")
        //         .attr("transform", `translate(0,${height - margin.bottom})`)
        //         .call(xAxis);

        //     this.svg3d.append("g")
        //         .attr("transform", `translate(${margin.left},0)`)
        //         .call(yAxis);

        //     // 添加坐标轴标签
        //     this.svg3d.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("x", width / 2)
        //         .attr("y", height - 5)
        //         .text("LD1");

        //     this.svg3d.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("transform", "rotate(-90)")
        //         .attr("x", -height / 2)
        //         .attr("y", 15)
        //         .text("LD2");

        //     // LDAVisualizationExamples.vue (第二部分) - 继续完成方法部分

        //     // 添加标题
        //     this.svg3d.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("x", width / 2)
        //         .attr("y", 15)
        //         .text("LDA 3D投影（LD3用点大小表示）")
        //         .style("font-weight", "bold");

        //     // 颜色比例尺
        //     const colors = d3.schemeCategory10;

        //     // 绘制数据点
        //     this.svg3d.selectAll("circle")
        //         .data(data)
        //         .enter()
        //         .append("circle")
        //         .attr("cx", d => xScale(d.x))
        //         .attr("cy", d => yScale(d.y))
        //         .attr("r", d => sizeScale(d.z))
        //         .attr("fill", d => colors[d.class])
        //         .attr("opacity", 0.7)
        //         .attr("stroke", "white")
        //         .attr("stroke-width", 0.5);

        //     // 添加图例
        //     const legend = this.svg3d.selectAll(".legend")
        //         .data(d3.range(this.numClassesToShow))
        //         .enter()
        //         .append("g")
        //         .attr("class", "legend")
        //         .attr("transform", (d, i) => `translate(0,${i * 20 + margin.top})`);

        //     legend.append("rect")
        //         .attr("x", width - margin.right + 10)
        //         .attr("width", 10)
        //         .attr("height", 10)
        //         .attr("fill", d => colors[d]);

        //     legend.append("text")
        //         .attr("x", width - margin.right + 25)
        //         .attr("y", 5)
        //         .attr("dy", ".35em")
        //         .style("font-size", "10px")
        //         .text(d => `类别 ${d}`);

        //     // 添加Z轴图例
        //     this.svg3d.append("text")
        //         .attr("x", margin.left)
        //         .attr("y", margin.top / 2)
        //         .text("LD3: 点大小表示Z值")
        //         .style("font-size", "10px");
        // },

        // drawPCA(data) {
        //     // 清除已有内容
        //     this.svgPca.selectAll("*").remove();

        //     const width = this.svgPca.attr("width");
        //     const height = this.svgPca.attr("height");
        //     const margin = { top: 30, right: 30, bottom: 40, left: 50 };

        //     // 创建比例尺
        //     const xExtent = d3.extent(data, d => d.x);
        //     const yExtent = d3.extent(data, d => d.y);
        //     const padding = 1.2;

        //     const xScale = d3.scaleLinear()
        //         .domain([xExtent[0] * padding, xExtent[1] * padding])
        //         .range([margin.left, width - margin.right]);

        //     const yScale = d3.scaleLinear()
        //         .domain([yExtent[0] * padding, yExtent[1] * padding])
        //         .range([height - margin.bottom, margin.top]);

        //     // 添加坐标轴
        //     const xAxis = d3.axisBottom(xScale);
        //     const yAxis = d3.axisLeft(yScale);

        //     this.svgPca.append("g")
        //         .attr("transform", `translate(0,${height - margin.bottom})`)
        //         .call(xAxis);

        //     this.svgPca.append("g")
        //         .attr("transform", `translate(${margin.left},0)`)
        //         .call(yAxis);

        //     // 添加坐标轴标签
        //     this.svgPca.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("x", width / 2)
        //         .attr("y", height - 5)
        //         .text("PC1");

        //     this.svgPca.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("transform", "rotate(-90)")
        //         .attr("x", -height / 2)
        //         .attr("y", 15)
        //         .text("PC2");

        //     // 添加标题
        //     this.svgPca.append("text")
        //         .attr("text-anchor", "middle")
        //         .attr("x", width / 2)
        //         .attr("y", 15)
        //         .text(`PCA 2D可视化 (${this.useStandardization ? '标准化' : '未标准化'})`)
        //         .style("font-weight", "bold");

        //     // 颜色比例尺
        //     const colors = d3.schemeCategory10;

        //     // 绘制数据点
        //     this.svgPca.selectAll("circle")
        //         .data(data)
        //         .enter()
        //         .append("circle")
        //         .attr("cx", d => xScale(d.x))
        //         .attr("cy", d => yScale(d.y))
        //         .attr("r", this.pointSize)
        //         .attr("fill", d => colors[d.class])
        //         .attr("opacity", 0.7)
        //         .attr("stroke", "white")
        //         .attr("stroke-width", 0.5);

        //     // 添加图例
        //     const legend = this.svgPca.selectAll(".legend")
        //         .data(d3.range(this.numClassesToShow))
        //         .enter()
        //         .append("g")
        //         .attr("class", "legend")
        //         .attr("transform", (d, i) => `translate(0,${i * 20 + margin.top})`);

        //     legend.append("rect")
        //         .attr("x", width - margin.right + 10)
        //         .attr("width", 10)
        //         .attr("height", 10)
        //         .attr("fill", d => colors[d]);

        //     legend.append("text")
        //         .attr("x", width - margin.right + 25)
        //         .attr("y", 5)
        //         .attr("dy", ".35em")
        //         .style("font-size", "10px")
        //         .text(d => `类别 ${d}`);
        // },

        checkAnswers() {
            this.quizChecked = true;

            // 检查答案是否全部正确
            const allCorrect = this.quizAnswers.every((answer, index) => answer === this.correctAnswers[index]);
            this.quizCorrect = allCorrect;

            // 生成回应
            if (allCorrect) {
                this.response = `
### 🎉 太棒了！所有答案都正确！

你已经很好地理解了LDA降维的可视化结果和特性：

1. 对于鸢尾花数据集，标准化后的LDA确实产生了最好的类别分离效果，这显示了预处理对LDA性能的影响。

2. 当类别数量增加时，LDA的最大可能投影维度确实会随类别数量增加而增加，最大为(类别数-1)维。

3. LDA相对于PCA的主要优势确实是更好地保留了类别间的可分性，这是因为LDA利用了类别信息进行降维。

通过本节的互动可视化和练习，你现在应该对LDA的实际应用效果有了更直观的理解。
    `;
            } else {
                // 找出错误的答案
                let errorMessages = "请仔细回顾以下问题的答案：\n\n";

                if (this.quizAnswers[0] !== this.correctAnswers[0]) {
                    errorMessages += "- 问题1：通过比较不同的可视化，标准化后的LDA通常能产生最好的类别分离效果，这说明了合适的预处理对LDA的重要性。\n\n";
                }

                if (this.quizAnswers[1] !== this.correctAnswers[1]) {
                    errorMessages += "- 问题2：LDA的最大投影维度受限于类别数量，具体为(类别数-1)维。增加类别数量会增加可能的投影维度。\n\n";
                }

                if (this.quizAnswers[2] !== this.correctAnswers[2]) {
                    errorMessages += "- 问题3：LDA利用了类别信息进行降维，因此在保留类别间可分性方面通常优于无监督的PCA。\n\n";
                }

                this.response = `
### 有些答案不正确

${errorMessages}

请再次通过互动可视化工具，观察不同算法、不同参数设置下的降维效果，加深对LDA的理解。
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