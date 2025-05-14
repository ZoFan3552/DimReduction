<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="applications-interactive">
                <h3>PCA应用场景探索</h3>
                <p>在这个互动环节中，我们将探索PCA在不同领域的实际应用。</p>

                <div class="application-tabs">
                    <el-tabs v-model="activeTab">
                        <el-tab-pane label="图像压缩" name="image">
                            <div class="application-content">
                                <h4>PCA在图像压缩中的应用</h4>

                                <div class="image-compression">
                                    

                                    <div class="compression-controls">
                                        <p>主成分数量: {{ pcCount }}</p>
                                        <el-slider v-model="pcCount" :min="1" :max="20"
                                            @change="updateCompressedImage"></el-slider>
                                        <p>信息保留率: {{ infoRetentionRate }}%</p>
                                    </div>

                                    <div class="compressed-image">
                                        <h5>压缩后图像</h5>
                                        <div class="image-container" ref="compressedImage">
                                            <!-- D3生成的压缩图像 -->
                                        </div>
                                    </div>
                                </div>

                                <div class="application-explanation">
                                    <p>
                                        使用PCA进行图像压缩的核心思想是，将图像视为高维数据，每个像素为一个特征。
                                        PCA可以找到图像中最重要的模式（特征脸），使用较少的主成分重建大部分图像信息。
                                    </p>
                                    <p>
                                        优势：适用于具有高度冗余信息的图像；压缩率可调节。<br>
                                        劣势：对于复杂纹理的图像效果较差；有损压缩。
                                    </p>
                                </div>
                            </div>
                        </el-tab-pane>

                        <el-tab-pane label="人脸识别" name="face">
                            <div class="application-content">
                                <h4>PCA在人脸识别中的应用</h4>

                                <div class="face-recognition">
                                    <div class="eigenfaces">
                                        <h5>特征脸（Eigenfaces）</h5>
                                        <div class="eigenfaces-grid" ref="eigenfacesGrid">
                                            <!-- D3生成的特征脸网格 -->
                                        </div>
                                    </div>

                                    <div class="recognition-demo">
                                        <h5>人脸识别演示</h5>
                                        <p>拖动滑块调整不同特征脸的权重，观察合成的人脸变化。</p>

                                        <div class="weight-sliders">
                                            <div v-for="(weight, index) in faceWeights" :key="index"
                                                class="weight-slider">
                                                <span>特征脸 {{ index + 1 }}: {{ weight.toFixed(2) }}</span>
                                                <el-slider v-model="faceWeights[index]" :min="-3" :max="3" :step="0.1"
                                                    @change="updateSynthesizedFace"></el-slider>
                                            </div>
                                        </div>

                                        <div class="synthesized-face" ref="synthesizedFace">
                                            <!-- D3生成的合成人脸 -->
                                        </div>
                                    </div>
                                </div>

                                <div class="application-explanation">
                                    <p>
                                        在人脸识别中，PCA被用来生成"特征脸"（Eigenfaces），这些特征脸捕捉了人脸变化的主要模式。
                                        每个人脸都可以表示为特征脸的线性组合，大大降低了表示和匹配人脸所需的维度。
                                    </p>
                                    <p>
                                        优势：降低计算复杂度；消除冗余信息；突出区分性特征。<br>
                                        劣势：对光照和姿势变化敏感；需要对齐的人脸图像。
                                    </p>
                                </div>
                            </div>
                        </el-tab-pane>

                        <el-tab-pane label="基因表达分析" name="gene">
                            <div class="application-content">
                                <h4>PCA在基因表达数据分析中的应用</h4>

                                <div class="gene-analysis">
                                    <div class="gene-visualization" ref="geneVisualization">
                                        <!-- D3生成的基因表达数据可视化 -->
                                    </div>

                                    <div class="analysis-controls">
                                        <p>选择显示维度：</p>
                                        <el-radio-group v-model="geneDimensions" @change="updateGeneVisualization">
                                            <el-radio :label="'pc1_pc2'">PC1 vs PC2</el-radio>
                                            <el-radio :label="'pc1_pc3'">PC1 vs PC3</el-radio>
                                            <el-radio :label="'pc2_pc3'">PC2 vs PC3</el-radio>
                                        </el-radio-group>

                                        <div class="cluster-toggle">
                                            <span>显示聚类：</span>
                                            <el-switch v-model="showClusters"
                                                @change="updateGeneVisualization"></el-switch>
                                        </div>
                                    </div>
                                </div>

                                <div class="application-explanation">
                                    <p>
                                        在基因表达分析中，PCA用于降低高维基因表达数据的复杂性，
                                        帮助研究人员发现基因表达模式，区分不同细胞类型或疾病状态。
                                    </p>
                                    <p>
                                        优势：处理高维度（数千至数万个基因）的数据；揭示隐藏的生物学模式；减少批次效应。<br>
                                        劣势：主成分的生物学解释可能不直观；可能掩盖稀有但重要的变异。
                                    </p>
                                </div>
                            </div>
                        </el-tab-pane>
                    </el-tabs>
                </div>

                <div class="case-study-exercise">
                    <h4>案例分析练习</h4>
                    <p>请分析以下场景，并选择最适合应用PCA的情况：</p>

                    <div class="case-descriptions">
                        <el-card v-for="(caseItem, index) in cases" :key="index" class="case-card"
                            :class="{ 'is-selected': selectedCase === index }">
                            <div class="case-content" @click="selectCase(index)">
                                <h5>案例 {{ index + 1 }}: {{ caseItem.title }}</h5>
                                <p>{{ caseItem.description }}</p>
                            </div>
                        </el-card>
                    </div>

                    <el-button type="primary" @click="checkCaseSelection" :disabled="selectedCase === null"
                        class="check-case-button">
                        提交选择
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
    name: 'PCAApplications',
    components: {
        BaseSegment
    },
    data() {
        return {
            title: '7. PCA应用场景',
            segmentId: 'pca-applications',
            content: `
  ## PCA的实际应用
  
  Principal Component Analysis (PCA)作为一种强大的降维技术，在许多领域有着广泛的应用。它能够有效地从高维数据中提取主要信息，帮助我们处理和分析复杂数据。
  
  ### PCA的主要应用领域
  
  #### 1. 数据可视化与探索
  
  降维至2-3维使得高维数据可以被可视化，帮助数据科学家直观地发现数据模式、聚类和异常值。
  
  #### 2. 数据压缩
  
  PCA可以减少数据存储空间需求，同时保留主要信息。例如，在图像和音频处理中常用于压缩数据。
  
  #### 3. 噪声过滤
  
  通过丢弃较小特征值对应的主成分，可以去除数据中的随机噪声，提高信噪比。
  
  #### 4. 特征提取
  
  PCA可以从原始特征中提取新的、更有代表性的特征，为后续的机器学习任务提供更好的输入。
  
  #### 5. 多重共线性处理
  
  在回归分析中，PCA可用于处理高度相关的预测变量，减轻多重共线性问题。
  
  ### 领域特定应用
  
  #### 图像处理
  
  - **人脸识别**：使用PCA生成"特征脸"(Eigenfaces)，大大降低表示和匹配人脸所需的维度
  - **图像压缩**：减少图像存储和传输的数据量
  - **背景建模**：在视频监控中分离前景和背景
  
  #### 生物信息学
  
  - **基因表达数据分析**：识别基因表达模式，区分不同细胞类型或疾病状态
  - **蛋白质结构分析**：研究蛋白质结构的主要变化模式
  - **药物发现**：分析分子特性，筛选潜在的药物候选物
  
  #### 金融分析
  
  - **投资组合优化**：分析资产回报的主要风险因素
  - **市场结构分析**：识别金融市场的主要驱动因素
  - **经济指标分析**：综合多个经济指标，提取关键经济趋势
  
  #### 自然语言处理
  
  - **潜在语义分析**：发现文档和词汇之间的隐藏关系
  - **词嵌入降维**：压缩高维词向量表示
  - **文本聚类和分类**：基于降维后的特征进行文档分组
  
  在下面的互动环节中，我们将深入探讨几个典型的PCA应用场景，并通过可视化演示了解PCA如何在实际问题中发挥作用。
        `,
            // 标签页控制
            activeTab: 'image',

            // 图像压缩相关
            pcCount: 5,
            infoRetentionRate: 75,
            imageData: null,

            // 人脸识别相关
            faceWeights: [0, 0, 0, 0, 0],

            // 基因表达分析相关
            geneDimensions: 'pc1_pc2',
            showClusters: true,
            geneData: null,

            // 案例分析练习
            cases: [
                {
                    title: "自然语言处理中的文本分类",
                    description: "有一个包含10,000个文档的语料库，使用TF-IDF表示，每个文档有30,000个特征。需要对文档进行主题分类。"
                },
                {
                    title: "销售数据分析",
                    description: "一家零售商有5年的销售数据，包含5个特征：产品类别、价格、季节、促销活动和销售量。需要分析这些因素之间的关系。"
                },
                {
                    title: "医学图像诊断",
                    description: "一组MRI扫描图像，每张图像有1024x1024像素。需要识别可能的肿瘤特征，并减少存储空间。"
                },
                {
                    title: "股票市场分析",
                    description: "有500支股票的10年每日价格数据，需要找出影响股票价格的主要因素，并构建投资组合。"
                }
            ],
            selectedCase: null,
            caseAttempts: 0
        };
    },
    methods: {
        initVisualizations() {
            // 初始化各选项卡的可视化
            this.$nextTick(() => {
                this.initImageCompression();
                this.initFaceRecognition();
                this.initGeneExpression();
            });
        },

        // ============ 图像压缩相关 ============
        initImageCompression() {
            // 清除之前的可视化
            d3.select(this.$refs.compressedImage).selectAll("*").remove();

            // 创建SVG
            const width = 200;
            const height = 200;

            d3.select(this.$refs.compressedImage)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 生成模拟的图像数据
            this.generateImageData(width, height);

            // 初始化压缩图像
            this.updateCompressedImage();
        },

        generateImageData(width, height) {
            // 创建一个模拟的"图像"数据集
            const pixels = width * height;
            this.imageData = {
                width: width,
                height: height,
                pixels: []
            };

            // 生成原始"像素"数据（模拟，非真实图像）
            for (let i = 0; i < pixels; i++) {
                const x = i % width;
                const y = Math.floor(i / width);

                // 生成一些图案，例如圆形渐变
                const centerX = width / 2;
                const centerY = height / 2;
                const distance = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2));
                const maxDistance = Math.sqrt(Math.pow(width / 2, 2) + Math.pow(height / 2, 2));

                // 归一化距离并反转（中心亮，边缘暗）
                const normalizedDistance = 1 - (distance / maxDistance);

                // 添加一些纹理（正弦波）
                const texture = 0.2 * Math.sin(x / 5) * Math.sin(y / 5);

                // 组合基本渐变和纹理
                const value = Math.max(0, Math.min(1, normalizedDistance + texture));

                this.imageData.pixels.push(value);
            }
        },

        updateCompressedImage() {
            // 更新信息保留率（基于主成分数量）
            this.infoRetentionRate = Math.min(100, Math.round(this.pcCount * 5));

            // 获取SVG和尺寸
            const svg = d3.select(this.$refs.compressedImage).select("svg");
            const width = this.imageData.width;
            // const height = this.imageData.height;

            // 清除之前的图像
            svg.selectAll("*").remove();

            // 创建像素网格
            const pixelSize = width / Math.sqrt(this.imageData.pixels.length);

            // 模拟压缩后的图像（根据主成分数量调整细节级别）
            const compressedPixels = this.simulateCompressedImage(this.pcCount);

            // 绘制压缩后的图像
            svg.selectAll("rect")
                .data(compressedPixels)
                .enter()
                .append("rect")
                .attr("x", (d, i) => (i % width) * pixelSize)
                .attr("y", (d, i) => Math.floor(i / width) * pixelSize)
                .attr("width", pixelSize)
                .attr("height", pixelSize)
                .attr("fill", d => this.grayScale(d));
        },

        simulateCompressedImage(pcCount) {
            // 模拟PCA压缩后的图像
            // 这里简化处理，使用模糊效果模拟压缩
            const pixels = this.imageData.pixels;
            const width = this.imageData.width;
            const height = this.imageData.height;

            // 模拟压缩后的像素
            const compressed = [];

            // 根据保留的主成分数量调整模糊程度
            // 主成分数量越少，模糊程度越高
            const blurRadius = Math.max(1, Math.floor(10 - pcCount * 0.5));

            for (let y = 0; y < height; y++) {
                for (let x = 0; x < width; x++) {
                    // 应用简单的盒式模糊
                    let sum = 0;
                    let count = 0;

                    for (let dy = -blurRadius; dy <= blurRadius; dy++) {
                        for (let dx = -blurRadius; dx <= blurRadius; dx++) {
                            const nx = x + dx;
                            const ny = y + dy;

                            if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
                                sum += pixels[ny * width + nx];
                                count++;
                            }
                        }
                    }

                    // 平均值作为压缩后的像素值
                    compressed.push(sum / count);
                }
            }

            // 添加一些基于主成分数量的"噪声"（模拟丢失细节）
            // 主成分数量越少，噪声越多
            const noiseLevel = Math.max(0, 0.2 - 0.01 * pcCount);

            return compressed.map(p => {
                return Math.max(0, Math.min(1, p + (Math.random() - 0.5) * noiseLevel));
            });
        },

        grayScale(value) {
            // 将0-1的值转换为灰度颜色
            const intensity = Math.floor(value * 255);
            return `rgb(${intensity}, ${intensity}, ${intensity})`;
        },

        // ============ 人脸识别相关 ============
        initFaceRecognition() {
            // 初始化特征脸网格
            this.initEigenfaces();

            // 初始化合成人脸
            this.updateSynthesizedFace();
        },

        initEigenfaces() {
            // 清除之前的可视化
            d3.select(this.$refs.eigenfacesGrid).selectAll("*").remove();

            const container = d3.select(this.$refs.eigenfacesGrid)
                .append("div")
                .attr("class", "eigenface-grid-container");

            // 创建5个模拟的特征脸
            for (let i = 0; i < 5; i++) {
                const eigenface = container.append("div")
                    .attr("class", "eigenface-item")
                    .style("width", "50px")
                    .style("height", "50px")
                    .style("margin", "5px")
                    .style("display", "inline-block");

                eigenface.append("svg")
                    .attr("width", 50)
                    .attr("height", 50)
                    .append("rect")
                    .attr("width", 50)
                    .attr("height", 50)
                    .attr("fill", "white")
                    .attr("stroke", "#ddd");

                // 为每个特征脸生成不同的模式
                const svg = eigenface.select("svg");
                this.drawEigenface(svg, i);

                eigenface.append("div")
                    .style("text-align", "center")
                    .style("font-size", "12px")
                    .text(`特征脸 ${i + 1}`);
            }
        },

        drawEigenface(svg, index) {
            // 绘制模拟的特征脸（简化为图案）
            // const width = 50;
            // const height = 50;

            switch (index) {
                case 0: // 整体明暗
                    svg.append("rect")
                        .attr("x", 5)
                        .attr("y", 5)
                        .attr("width", 40)
                        .attr("height", 40)
                        .attr("fill", "#888");
                    break;
                case 1: // 左右对比
                    svg.append("rect")
                        .attr("x", 5)
                        .attr("y", 5)
                        .attr("width", 20)
                        .attr("height", 40)
                        .attr("fill", "#666");
                    svg.append("rect")
                        .attr("x", 25)
                        .attr("y", 5)
                        .attr("width", 20)
                        .attr("height", 40)
                        .attr("fill", "#aaa");
                    break;
                case 2: // 上下对比
                    svg.append("rect")
                        .attr("x", 5)
                        .attr("y", 5)
                        .attr("width", 40)
                        .attr("height", 20)
                        .attr("fill", "#666");
                    svg.append("rect")
                        .attr("x", 5)
                        .attr("y", 25)
                        .attr("width", 40)
                        .attr("height", 20)
                        .attr("fill", "#aaa");
                    break;
                case 3: // 对角线
                    svg.append("polygon")
                        .attr("points", `5,5 45,5 5,45`)
                        .attr("fill", "#666");
                    svg.append("polygon")
                        .attr("points", `45,5 45,45 5,45`)
                        .attr("fill", "#aaa");
                    break;
                case 4: // 中心-外围
                    svg.append("circle")
                        .attr("cx", 25)
                        .attr("cy", 25)
                        .attr("r", 15)
                        .attr("fill", "#666");
                    svg.append("circle")
                        .attr("cx", 25)
                        .attr("cy", 25)
                        .attr("r", 7)
                        .attr("fill", "#aaa");
                    break;
            }
        },

        updateSynthesizedFace() {
            // 清除之前的可视化
            d3.select(this.$refs.synthesizedFace).selectAll("*").remove();

            // 创建SVG
            const width = 150;
            const height = 150;

            const svg = d3.select(this.$refs.synthesizedFace)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 绘制背景
            svg.append("rect")
                .attr("width", width)
                .attr("height", height)
                .attr("fill", "#f5f5f5");

            // 创建面部轮廓（椭圆）
            svg.append("ellipse")
                .attr("cx", width / 2)
                .attr("cy", height / 2)
                .attr("rx", 60)
                .attr("ry", 70)
                .attr("fill", "#ffd6b3");

            // 左眼
            const leftEyeX = width / 2 - 20 - this.faceWeights[1] * 5;
            const eyeY = height / 2 - 10 - this.faceWeights[2] * 5;
            const eyeSize = 10 + this.faceWeights[0] * 2;

            svg.append("ellipse")
                .attr("cx", leftEyeX)
                .attr("cy", eyeY)
                .attr("rx", eyeSize)
                .attr("ry", eyeSize * 0.6)
                .attr("fill", "white")
                .attr("stroke", "black");

            svg.append("circle")
                .attr("cx", leftEyeX + this.faceWeights[4] * 2)
                .attr("cy", eyeY)
                .attr("r", 3)
                .attr("fill", "black");

            // 右眼
            const rightEyeX = width / 2 + 20 + this.faceWeights[1] * 5;

            svg.append("ellipse")
                .attr("cx", rightEyeX)
                .attr("cy", eyeY)
                .attr("rx", eyeSize)
                .attr("ry", eyeSize * 0.6)
                .attr("fill", "white")
                .attr("stroke", "black");

            svg.append("circle")
                .attr("cx", rightEyeX + this.faceWeights[4] * 2)
                .attr("cy", eyeY)
                .attr("r", 3)
                .attr("fill", "black");

            // 嘴巴
            const mouthWidth = 40 + this.faceWeights[0] * 5;
            const mouthHeight = 5 + Math.abs(this.faceWeights[3]) * 5;
            const mouthY = height / 2 + 30 + this.faceWeights[2] * 3;

            svg.append("ellipse")
                .attr("cx", width / 2)
                .attr("cy", mouthY)
                .attr("rx", mouthWidth)
                .attr("ry", mouthHeight)
                .attr("fill", this.faceWeights[3] > 0 ? "#ff9999" : "#cc6666");
        },

        // ============ 基因表达分析相关 ============
        initGeneExpression() {
            // 生成模拟的基因表达数据
            this.generateGeneData();

            // 初始化可视化
            this.updateGeneVisualization();
        },

        generateGeneData() {
            // 生成模拟的基因表达数据
            // 创建3个聚类，模拟不同细胞类型或条件
            const numPoints = 100;
            this.geneData = [];

            // 类别标签和颜色
            const categories = [
                { name: "正常细胞", color: "#4CAF50" },
                { name: "癌细胞 A型", color: "#F44336" },
                { name: "癌细胞 B型", color: "#2196F3" }
            ];

            // 生成PC坐标（3个主成分）
            for (let i = 0; i < numPoints; i++) {
                // 随机选择一个类别
                const categoryIndex = Math.floor(Math.random() * 3);
                const category = categories[categoryIndex];

                // 根据类别生成主成分坐标（模拟聚类）
                let pc1, pc2, pc3;

                switch (categoryIndex) {
                    case 0: // 正常细胞
                        pc1 = this.randomNormal() * 1.5 - 3;
                        pc2 = this.randomNormal() * 1.5 + 2;
                        pc3 = this.randomNormal() * 1.5;
                        break;
                    case 1: // 癌细胞 A型
                        pc1 = this.randomNormal() * 1.5 + 3;
                        pc2 = this.randomNormal() * 1.5 - 1;
                        pc3 = this.randomNormal() * 1.5 + 2;
                        break;
                    case 2: // 癌细胞 B型
                        pc1 = this.randomNormal() * 1.5 + 1;
                        pc2 = this.randomNormal() * 1.5 - 3;
                        pc3 = this.randomNormal() * 1.5 - 2;
                        break;
                }

                this.geneData.push({
                    id: `gene_${i}`,
                    pc1: pc1,
                    pc2: pc2,
                    pc3: pc3,
                    category: category.name,
                    color: category.color
                });
            }
        },

        randomNormal() {
            // Box-Muller变换生成标准正态分布随机数
            const u1 = Math.random();
            const u2 = Math.random();

            return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        },

        updateGeneVisualization() {
            // 清除之前的可视化
            d3.select(this.$refs.geneVisualization).selectAll("*").remove();

            // 创建SVG
            const width = 500;
            const height = 400;
            const margin = { top: 40, right: 100, bottom: 60, left: 60 };

            const svg = d3.select(this.$refs.geneVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            const g = svg.append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            // 绘图区域大小
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 确定X和Y轴对应的主成分
            let xComponent, yComponent, xLabel, yLabel;

            switch (this.geneDimensions) {
                case 'pc1_pc2':
                    xComponent = 'pc1';
                    yComponent = 'pc2';
                    xLabel = '第一主成分 (33.5%)';
                    yLabel = '第二主成分 (24.2%)';
                    break;
                case 'pc1_pc3':
                    xComponent = 'pc1';
                    yComponent = 'pc3';
                    xLabel = '第一主成分 (33.5%)';
                    yLabel = '第三主成分 (15.8%)';
                    break;
                case 'pc2_pc3':
                    xComponent = 'pc2';
                    yComponent = 'pc3';
                    xLabel = '第二主成分 (24.2%)';
                    yLabel = '第三主成分 (15.8%)';
                    break;
            }

            // 创建比例尺
            const xExtent = d3.extent(this.geneData, d => d[xComponent]);
            const yExtent = d3.extent(this.geneData, d => d[yComponent]);

            // 添加一些边距
            const xPadding = (xExtent[1] - xExtent[0]) * 0.1;
            const yPadding = (yExtent[1] - yExtent[0]) * 0.1;

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - xPadding, xExtent[1] + xPadding])
                .range([0, plotWidth]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - yPadding, yExtent[1] + yPadding])
                .range([plotHeight, 0]);

            // 绘制X和Y轴
            g.append("g")
                .attr("transform", `translate(0,${plotHeight})`)
                .call(d3.axisBottom(xScale));

            g.append("g")
                .call(d3.axisLeft(yScale));

            // 添加轴标签
            g.append("text")
                .attr("x", plotWidth / 2)
                .attr("y", plotHeight + 40)
                .attr("text-anchor", "middle")
                .text(xLabel);

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -plotHeight / 2)
                .attr("y", -40)
                .attr("text-anchor", "middle")
                .text(yLabel);

            // 绘制数据点
            g.selectAll(".data-point")
                .data(this.geneData)
                .enter()
                .append("circle")
                .attr("class", "data-point")
                .attr("cx", d => xScale(d[xComponent]))
                .attr("cy", d => yScale(d[yComponent]))
                .attr("r", 5)
                .style("fill", d => this.showClusters ? d.color : "#69b3a2")
                .style("opacity", 0.7)
                .append("title")
                .text(d => `${d.id}\n${d.category}`);

            // 添加聚类椭圆（如果启用）
            if (this.showClusters) {
                // 获取不同类别
                const categories = [...new Set(this.geneData.map(d => d.category))];

                categories.forEach(category => {
                    // 获取该类别的点
                    const points = this.geneData.filter(d => d.category === category);

                    // 计算该类别在X和Y方向的均值和标准差
                    const xMean = d3.mean(points, d => d[xComponent]);
                    const yMean = d3.mean(points, d => d[yComponent]);
                    const xStd = Math.sqrt(d3.variance(points, d => d[xComponent]));
                    const yStd = Math.sqrt(d3.variance(points, d => d[yComponent]));

                    // 绘制椭圆（置信椭圆，2倍标准差）
                    const ellipsePath = this.calculateEllipsePath(
                        xScale(xMean),
                        yScale(yMean),
                        xScale(xMean + 2 * xStd) - xScale(xMean),
                        yScale(yMean) - yScale(yMean + 2 * yStd)
                    );

                    g.append("path")
                        .attr("d", ellipsePath)
                        .attr("stroke", points[0].color)
                        .attr("fill", "none")
                        .attr("stroke-width", 2)
                        .attr("stroke-dasharray", "5,5");
                });

                // 添加图例
                const legend = g.append("g")
                    .attr("transform", `translate(${plotWidth + 20}, 0)`);

                categories.forEach((category, i) => {
                    const categoryColor = this.geneData.find(d => d.category === category).color;

                    legend.append("circle")
                        .attr("cx", 10)
                        .attr("cy", 20 * i + 10)
                        .attr("r", 6)
                        .style("fill", categoryColor);

                    legend.append("text")
                        .attr("x", 25)
                        .attr("y", 20 * i + 15)
                        .text(category)
                        .style("font-size", "12px");
                });
            }

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("font-weight", "bold")
                .text("基因表达数据PCA可视化");
        },

        // calculateEllipsePath(cx, cy, rx, ry) {
        //     // 计算椭圆路径
        //     const path = d3.path();
        //     path.ellipse(cx, cy, rx, ry, 0, 0, 2 * Math.PI);
        //     return path.toString();
        // },
        calculateEllipsePath(cx, cy, rx, ry) {
            // 方法1：使用 SVG 椭圆参数方程（推荐）
            const points = [];
            const segments = 36; // 分段数，越多越平滑

            for (let i = 0; i <= segments; i++) {
                const angle = (i / segments) * 2 * Math.PI;
                const x = cx + rx * Math.cos(angle);
                const y = cy + ry * Math.sin(angle);
                points.push([x, y]);
            }

            // 构建 SVG path 的 "d" 属性
            let pathStr = `M ${points[0][0]},${points[0][1]}`;
            for (let i = 1; i < points.length; i++) {
                pathStr += ` L ${points[i][0]},${points[i][1]}`;
            }
            pathStr += " Z";

            return pathStr;


        },


        // ============ 案例分析相关 ============
        selectCase(index) {
            this.selectedCase = index;
        },

        checkCaseSelection() {
            this.caseAttempts++;

            // 正确答案是案例2（医学图像）和案例3（股票市场分析）
            // 但只需选择一个
            const correctAnswers = [2, 3];

            if (correctAnswers.includes(this.selectedCase)) {
                // 回答正确
                let responseText = "";
                if (this.selectedCase === 2) {
                    responseText = "医学图像确实是PCA的理想应用场景！医学图像具有高维度特性（1024x1024像素），通过PCA可以提取关键特征并压缩存储空间，同时保留肿瘤特征等关键信息。";
                } else {
                    responseText = "股票市场分析是PCA的理想应用场景！面对500支股票的长期历史数据，PCA可以帮助找出主要的市场驱动因素，降低维度，并构建更有效的投资组合。";
                }

                this.$refs.baseSegment.showResponse(
                    "选择正确！",
                    responseText,
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.caseAttempts >= 2) {
                    hint = "提示：考虑哪些案例具有高维度特性，且需要降维来发现潜在模式或节省存储空间。";
                }

                this.$refs.baseSegment.showResponse(
                    "选择不是最佳的",
                    `这个场景可能不是PCA最理想的应用场合。请再思考一下哪些场景更适合应用PCA。${hint}`,
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
        // 初始化各个应用场景的可视化
        this.initVisualizations();
    },
    beforeDestroy() {
        // 清理资源
        const containers = [
            this.$refs.compressedImage,
            this.$refs.eigenfacesGrid,
            this.$refs.synthesizedFace,
            this.$refs.geneVisualization
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
.applications-interactive {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.application-tabs {
    margin-bottom: 30px;
}

.application-content {
    padding: 15px;
}

/* 图像压缩样式 */
.image-compression {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    margin-bottom: 20px;
}

.original-image,
.compressed-image {
    text-align: center;
}

.image-container {
    width: 200px;
    height: 200px;
    border: 1px solid #ddd;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
}

.compression-controls {
    flex: 1;
    min-width: 200px;
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

/* 人脸识别样式 */
.face-recognition {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    margin-bottom: 20px;
}

.eigenfaces {
    flex: 1;
    min-width: 200px;
}

.eigenfaces-grid {
    margin-top: 15px;
    text-align: center;
}

.recognition-demo {
    flex: 2;
    min-width: 300px;
}

.weight-sliders {
    margin: 15px 0;
}

.weight-slider {
    margin-bottom: 10px;
}

.synthesized-face {
    width: 150px;
    height: 150px;
    margin: 20px auto;
    border: 1px solid #ddd;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 基因表达分析样式 */
.gene-analysis {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
}

.gene-visualization {
    width: 100%;
    height: 400px;
    margin-bottom: 20px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    display: flex;
    justify-content: center;
}

.analysis-controls {
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.cluster-toggle {
    margin-top: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* 应用说明 */
.application-explanation {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    border-left: 4px solid #409EFF;
}

/* 案例分析练习 */
.case-study-exercise {
    margin-top: 30px;
    padding: 20px;
    background-color: #ecf5ff;
    border-radius: 4px;
}

.case-descriptions {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 20px 0;
}

.case-card {
    flex: 1;
    min-width: 200px;
    cursor: pointer;
    transition: all 0.3s;
}

.case-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.case-card.is-selected {
    border: 2px solid #409EFF;
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.case-content h5 {
    margin-top: 0;
    color: #303133;
}

.check-case-button {
    margin-top: 20px;
}
</style>