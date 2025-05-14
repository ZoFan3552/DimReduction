<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>7. UMAP参数详解</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 参数调整可视化 -->
            <div class="interaction-container">
                <h3>互动演示：参数效果可视化</h3>
                <p>调整以下参数滑块，观察它们如何影响UMAP在不同数据集上的降维结果。</p>

                <div class="parameter-controls">
                    <div class="parameter-item">
                        <span>邻居数量 (n_neighbors):</span>
                        <el-slider v-model="nNeighbors" :min="2" :max="100" :step="1"
                            @change="updateVisualization"></el-slider>
                        <div class="parameter-value">{{ nNeighbors }}</div>
                    </div>

                    <div class="parameter-item">
                        <span>最小距离 (min_dist):</span>
                        <el-slider v-model="minDist" :min="0" :max="1" :step="0.1"
                            @change="updateVisualization"></el-slider>
                        <div class="parameter-value">{{ minDist.toFixed(1) }}</div>
                    </div>

                    <div class="parameter-item">
                        <span>数据集:</span>
                        <el-radio-group v-model="datasetType" @change="changeDataset">
                            <el-radio label="blobs">多簇高斯分布</el-radio>
                            <el-radio label="spiral">螺旋数据</el-radio>
                            <el-radio label="moons">半月形数据</el-radio>
                        </el-radio-group>
                    </div>
                </div>

                <div class="visualizations">
                    <div class="visualization-panel">
                        <h4>原始数据</h4>
                        <div class="viz-container" ref="originalDataViz"></div>
                    </div>

                    <div class="visualization-panel">
                        <h4>UMAP投影结果</h4>
                        <div class="viz-container" ref="umapResultViz"></div>
                    </div>
                </div>

                <div class="parameter-explanation">
                    <h4>当前参数效果分析</h4>
                    <div v-html="currentParameterEffect"></div>
                </div>

                <!-- 参数推荐交互 -->
                <div class="recommendation-activity" v-if="!recommendationCompleted">
                    <h4>参数推荐练习</h4>
                    <p>根据您的观察，尝试为以下场景推荐合适的参数设置：</p>

                    <div class="scenario">
                        <p><strong>场景：</strong> 您有一个包含10,000个样本、100个特征的高维数据集，想要进行探索性的可视化分析，希望看到数据中的全局结构，包括大尺度的簇和可能的层次结构。
                        </p>

                        <div class="recommendation-form">
                            <div class="form-item">
                                <span>推荐的n_neighbors值范围：</span>
                                <el-radio-group v-model="recommendedNeighbors">
                                    <el-radio :label="1">5-15 (小)</el-radio>
                                    <el-radio :label="2">30-50 (中)</el-radio>
                                    <el-radio :label="3">80-100+ (大)</el-radio>
                                </el-radio-group>
                            </div>

                            <div class="form-item">
                                <span>推荐的min_dist值范围：</span>
                                <el-radio-group v-model="recommendedMinDist">
                                    <el-radio :label="1">0.0-0.1 (小)</el-radio>
                                    <el-radio :label="2">0.3-0.5 (中)</el-radio>
                                    <el-radio :label="3">0.7-1.0 (大)</el-radio>
                                </el-radio-group>
                            </div>

                            <div class="form-item">
                                <span>推荐的metric参数：</span>
                                <el-radio-group v-model="recommendedMetric">
                                    <el-radio :label="1">euclidean (欧几里得距离)</el-radio>
                                    <el-radio :label="2">manhattan (曼哈顿距离)</el-radio>
                                    <el-radio :label="3">correlation (相关系数距离)</el-radio>
                                </el-radio-group>
                            </div>

                            <el-button type="primary" @click="checkRecommendation" :disabled="!isRecommendationComplete"
                                class="submit-btn">
                                提交推荐
                            </el-button>
                        </div>
                    </div>
                </div>

                <!-- 回应部分 -->
                <div v-if="recommendationCompleted" class="response-container">
                    <el-alert :title="feedbackTitle" :type="allCorrect ? 'success' : 'info'"
                        :description="feedbackDescription" show-icon>
                    </el-alert>

                    <div v-if="!allCorrect" class="recommendation-results">
                        <h4>参数推荐结果分析：</h4>

                        <div v-if="!isNeighborsCorrect" class="param-feedback">
                            <p><strong>n_neighbors建议：</strong>
                                对于想要看到全局结构的大型数据集，中等或更大的n_neighbors值（30-50或更高）通常更合适。较大的n_neighbors会使算法关注更全局的结构，有助于发现大尺度的簇和层次结构。
                            </p>
                        </div>

                        <div v-if="!isMinDistCorrect" class="param-feedback">
                            <p><strong>min_dist建议：</strong>
                                对于探索性可视化，中等的min_dist值（0.3-0.5）通常是一个好的起点。这样既能保持簇分离，又不会使点过度聚集，便于观察层次结构。</p>
                        </div>

                        <div v-if="!isMetricCorrect" class="param-feedback">
                            <p><strong>metric建议：</strong> 对于一般的高维数据探索，euclidean（欧几里得距离）是一个标准选择。如果您不确定数据的特性，这是最安全的起点。</p>
                        </div>

                        <el-button type="info" @click="resetRecommendation" class="retry-btn">
                            重新选择
                        </el-button>
                    </div>

                    <div v-if="allCorrect || retries >= 1" class="next-section">
                        <p>🎉 您已完成UMAP参数部分！可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { marked } from 'marked';
import * as d3 from 'd3';

// 设置渲染器以支持数学公式
import 'katex/dist/katex.min.css';
// import katex from 'katex';
import katex from 'katex';
// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}


export default {
    name: 'Section7Parameters',
    data() {
        return {
            markdownContent: `
## UMAP参数详解

UMAP算法的灵活性很大程度上源于其多样的参数设置，这些参数使得算法可以适应不同类型的数据和不同的分析目标。理解这些参数的作用对于有效使用UMAP至关重要。

### 主要参数及其影响

#### 1. n_neighbors

**定义**：要考虑的每个点的最近邻数量。

**影响**：
- 控制关注**局部**还是**全局**结构的平衡
- 较小的值（如5-15）：关注非常局部的结构，可能会丢失全局模式
- 较大的值（如30-100）：保留更多全局结构，但可能会模糊局部细节
- 默认值通常为15，这在大多数情况下是一个合理的平衡

**适用场景**：
- 如果您想看到细粒度的局部关系，使用较小的值
- 如果您关注数据的全局布局和大尺度结构，使用较大的值
- 对于非常大的数据集，较大的值可能更稳定

#### 2. min_dist

**定义**：控制嵌入中点的紧密程度的参数。

**影响**：
- 较小的值（如0.0-0.1）：点聚集更紧密，聚类更紧凑
- 较大的值（如0.5-1.0）：点分布更均匀，聚类更分散
- 默认值通常为0.1

**适用场景**：
- 如果您想要紧凑、分离良好的聚类，使用较小的值
- 如果您想要更均匀分布的点，方便观察点之间的关系，使用较大的值
- 对于探索性分析，通常从中等值（如0.1-0.5）开始是合理的

#### 3. n_components

**定义**：目标嵌入的维度。

**影响**：
- 通常设置为2或3以便可视化
- 更高的维度可以保留更多信息，但难以直接可视化
- 默认值为2

**适用场景**：
- 对于可视化目的，使用2或3
- 如果是作为其他算法的预处理步骤，可以使用更高的维度
- 作为特征提取时，可以尝试不同维度并评估下游任务性能

#### 4. metric

**定义**：用于测量原始空间中点之间距离的度量。

**影响**：
- 不同的度量捕捉数据中不同类型的关系
- 常用选项包括：euclidean（欧几里得）、manhattan（曼哈顿）、cosine（余弦）、correlation（相关性）等
- 默认值为euclidean

**适用场景**：
- 对于一般数值数据，euclidean通常是合理的起点
- 对于文本或文档数据，cosine或correlation可能更合适
- 对于基因表达数据，correlation通常更有意义
- 对于二进制或计数数据，可以考虑使用hamming、jaccard或dice

#### 5. random_state

**定义**：随机数生成器的种子。

**影响**：
- 设置固定的随机种子使结果可重现
- 不同的种子可能产生略有不同的结果
- 默认为None（使用当前随机状态）

**适用场景**：
- 如果需要结果可重现，设置一个固定值
- 对于生产环境或正式报告，建议使用固定种子
- 对于探索分析，可以尝试不同种子，观察结果的稳健性

#### 6. n_epochs

**定义**：优化嵌入的训练轮数。

**影响**：
- 更多轮数通常产生更好的结果，但需要更长时间
- 默认值根据数据集大小自动设置
- 对于较大的数据集，可能需要手动减少以加快计算

**适用场景**：
- 对于小型数据集，可以使用默认值或增加轮数
- 对于大型数据集，可能需要减少轮数以平衡质量和速度
- 如果结果看起来不稳定，可以尝试增加轮数

### 参数调优策略

调整UMAP参数时，建议的工作流程是：

1. **从默认值开始**：UMAP的默认参数在大多数情况下表现良好
2. **关注主要参数**：首先调整n_neighbors和min_dist这两个最关键的参数
3. **考虑数据特性**：根据数据类型选择适当的metric
4. **迭代调优**：尝试不同的参数组合，观察结果
5. **验证结果**：如果可能，使用标记数据或领域知识验证结果的合理性

在下面的互动演示中，您可以亲自调整这些参数，观察它们如何影响不同类型数据的降维结果。
      `,
            nNeighbors: 15,
            minDist: 0.1,
            datasetType: 'blobs',
            datasets: {},
            recommendedNeighbors: null,
            recommendedMinDist: null,
            recommendedMetric: null,
            recommendationCompleted: false,
            allCorrect: false,
            isNeighborsCorrect: false,
            isMinDistCorrect: false,
            isMetricCorrect: false,
            retries: 0,
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
        },
        currentParameterEffect() {
            let effect = '<p>';

            // n_neighbors影响分析
            if (this.nNeighbors <= 10) {
                effect += '<strong>n_neighbors = ' + this.nNeighbors + '（较小）</strong>：当前值较小，算法更关注非常局部的结构。您可能会观察到更多细粒度的局部关系，但可能会丢失一些全局模式。在螺旋或半月形数据上，这可能导致结构断裂。';
            } else if (this.nNeighbors >= 50) {
                effect += '<strong>n_neighbors = ' + this.nNeighbors + '（较大）</strong>：当前值较大，算法更关注全局结构。您会看到更平滑的结果，但可能会丢失一些局部细节。在多簇数据上，这可能导致簇边界变得模糊。';
            } else {
                effect += '<strong>n_neighbors = ' + this.nNeighbors + '（中等）</strong>：当前值适中，在局部和全局结构之间取得了平衡。对于大多数数据集，这通常是一个良好的起点。';
            }

            effect += '</p><p>';

            // min_dist影响分析
            if (this.minDist <= 0.1) {
                effect += '<strong>min_dist = ' + this.minDist.toFixed(1) + '（较小）</strong>：当前值较小，导致点聚集更紧密。簇会显得更紧凑，这有助于识别清晰的群组，但如果值过小，可能会导致过度拥挤，难以区分局部结构。';
            } else if (this.minDist >= 0.7) {
                effect += '<strong>min_dist = ' + this.minDist.toFixed(1) + '（较大）</strong>：当前值较大，导致点分布更均匀。簇会显得更分散，这有助于观察点之间的相对位置，但可能会使簇边界变得不那么明显。';
            } else {
                effect += '<strong>min_dist = ' + this.minDist.toFixed(1) + '（中等）</strong>：当前值适中，提供了簇紧凑性和点分散度之间的平衡。对于探索性分析，这通常是一个良好的选择。';
            }

            effect += '</p><p>';

            // 数据集特定影响
            switch (this.datasetType) {
                case 'blobs':
                    effect += '<strong>多簇高斯分布数据</strong>：这种数据集包含明显分离的簇，UMAP通常能很好地保留这种结构。较大的n_neighbors可能会使簇边界变得模糊，而较小的min_dist会使簇看起来更紧凑。';
                    break;
                case 'spiral':
                    effect += '<strong>螺旋数据</strong>：这种数据具有连续的非线性结构。较小的n_neighbors有助于保留局部连续性，但可能会断裂结构；较大的n_neighbors可以保持整体形状，但可能会扭曲细节。';
                    break;
                case 'moons':
                    effect += '<strong>半月形数据</strong>：这种数据具有弯曲的边界。一个平衡的n_neighbors值有助于保留形状，而较小的min_dist可以使边界更清晰。';
                    break;
            }

            effect += '</p>';

            return effect;
        },
        isRecommendationComplete() {
            return this.recommendedNeighbors !== null &&
                this.recommendedMinDist !== null &&
                this.recommendedMetric !== null;
        },
        feedbackTitle() {
            return this.allCorrect ?
                '参数推荐正确！' :
                '参数推荐结果分析';
        },
        feedbackDescription() {
            if (this.allCorrect) {
                return '您成功推荐了适合该场景的参数设置！这些参数将有助于显示大数据集中的全局结构和层次关系。';
            } else {
                return '您的部分推荐可能不是该场景的最佳选择。请查看下面的详细解释。';
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(7);
        }

        // 初始化数据集
        this.generateDatasets();

        // 初始化可视化
        this.$nextTick(() => {
            this.initVisualizations();
        });
    },
    methods: {
        generateDatasets() {
            // 生成三种不同类型的2D数据集

            // 1. 多簇高斯分布数据
            const blobsData = [];
            const blobCenters = [
                [100, 100], [250, 100], [100, 250], [250, 250]
            ];
            const colors = ["#F56C6C", "#E6A23C", "#409EFF", "#67C23A"];

            for (let c = 0; c < blobCenters.length; c++) {
                const center = blobCenters[c];
                const color = colors[c];

                for (let i = 0; i < 50; i++) {
                    blobsData.push({
                        x: center[0] + (Math.random() - 0.5) * 60,
                        y: center[1] + (Math.random() - 0.5) * 60,
                        cluster: c,
                        color: color
                    });
                }
            }

            // 2. 螺旋数据
            const spiralData = [];
            const numSpirals = 2;
            const pointsPerSpiral = 100;

            for (let s = 0; s < numSpirals; s++) {
                for (let i = 0; i < pointsPerSpiral; i++) {
                    const t = 1.5 * Math.PI * i / pointsPerSpiral;
                    const r = 10 + 100 * i / pointsPerSpiral;
                    const x = 175 + r * Math.cos(t + s * Math.PI);
                    const y = 175 + r * Math.sin(t + s * Math.PI);

                    spiralData.push({
                        x: x,
                        y: y,
                        cluster: s,
                        color: s === 0 ? "#F56C6C" : "#409EFF"
                    });
                }
            }

            // 3. 半月形数据
            const moonsData = [];
            const numMoons = 2;
            const pointsPerMoon = 100;

            for (let m = 0; m < numMoons; m++) {
                for (let i = 0; i < pointsPerMoon; i++) {
                    const t = Math.PI * i / pointsPerMoon;
                    const sign = m === 0 ? 1 : -1;
                    const offset = m === 0 ? 0 : 25;

                    const x = 175 + sign * 100 * Math.cos(t);
                    const y = 175 + 50 * Math.sin(t) + offset;

                    // 添加一些噪声
                    const noiseX = (Math.random() - 0.5) * 20;
                    const noiseY = (Math.random() - 0.5) * 20;

                    moonsData.push({
                        x: x + noiseX,
                        y: y + noiseY,
                        cluster: m,
                        color: m === 0 ? "#F56C6C" : "#409EFF"
                    });
                }
            }

            // 存储数据集
            this.datasets = {
                blobs: blobsData,
                spiral: spiralData,
                moons: moonsData
            };
        },

        initVisualizations() {
            // 初始化可视化
            this.updateVisualization();
        },

        updateVisualization() {
            // 更新原始数据和UMAP结果可视化
            this.updateOriginalDataViz();
            this.updateUmapResultViz();
        },

        updateOriginalDataViz() {
            const width = this.$refs.originalDataViz.clientWidth;
            const height = 300;

            // 清除现有SVG
            d3.select(this.$refs.originalDataViz).selectAll("*").remove();

            const svg = d3.select(this.$refs.originalDataViz)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 获取当前数据集
            const data = this.datasets[this.datasetType];

            // 创建比例尺
            const xExtent = d3.extent(data, d => d.x);
            const yExtent = d3.extent(data, d => d.y);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - 10, xExtent[1] + 10])
                .range([30, width - 30]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - 10, yExtent[1] + 10])
                .range([height - 30, 30]);

            // 绘制点
            svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 5)
                .attr("fill", d => d.color)
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5);

            // 添加坐标轴
            const xAxis = d3.axisBottom(xScale).ticks(5);
            const yAxis = d3.axisLeft(yScale).ticks(5);

            svg.append("g")
                .attr("transform", `translate(0, ${height - 30})`)
                .call(xAxis);

            svg.append("g")
                .attr("transform", `translate(30, 0)`)
                .call(yAxis);

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .attr("font-size", "12px")
                .attr("font-weight", "bold")
                .text("原始二维数据");
        },

        updateUmapResultViz() {
            const width = this.$refs.umapResultViz.clientWidth;
            const height = 300;

            // 清除现有SVG
            d3.select(this.$refs.umapResultViz).selectAll("*").remove();

            const svg = d3.select(this.$refs.umapResultViz)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 获取当前数据集并模拟UMAP结果
            const data = this.datasets[this.datasetType];
            const umapResult = this.simulateUmap(data, this.nNeighbors, this.minDist);

            // 创建比例尺
            const xExtent = d3.extent(umapResult, d => d.x);
            const yExtent = d3.extent(umapResult, d => d.y);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - (xExtent[1] - xExtent[0]) * 0.1,
                xExtent[1] + (xExtent[1] - xExtent[0]) * 0.1])
                .range([30, width - 30]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - (yExtent[1] - yExtent[0]) * 0.1,
                yExtent[1] + (yExtent[1] - yExtent[0]) * 0.1])
                .range([height - 30, 30]);

            // 绘制点
            svg.selectAll("circle")
                .data(umapResult)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 5)
                .attr("fill", d => d.color)
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5);

            // 添加坐标轴
            const xAxis = d3.axisBottom(xScale).ticks(5);
            const yAxis = d3.axisLeft(yScale).ticks(5);

            svg.append("g")
                .attr("transform", `translate(0, ${height - 30})`)
                .call(xAxis);

            svg.append("g")
                .attr("transform", `translate(30, 0)`)
                .call(yAxis);

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .attr("font-size", "12px")
                .attr("font-weight", "bold")
                .text("UMAP降维结果");

            // 添加参数信息
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", height - 5)
                .attr("text-anchor", "middle")
                .attr("font-size", "10px")
                .text(`n_neighbors=${this.nNeighbors}, min_dist=${this.minDist.toFixed(1)}`);
        },

        simulateUmap(data, nNeighbors, minDist) {
            // 注意：这只是一个UMAP效果的简化模拟，不是真正的UMAP算法
            // 真正的UMAP实现要复杂得多

            // 根据数据类型和参数调整模拟效果
            let result = [];

            // 复制原始数据点
            data.forEach(d => {
                result.push({
                    ...d,
                    x: 0,
                    y: 0
                });
            });

            const clusterScale = 1.0 - minDist * 0.7; // min_dist越大，簇越分散
            const noiseLevel = 0.6 + (nNeighbors / 100) * 0.4; // n_neighbors越大，结果越平滑

            switch (this.datasetType) {
                case 'blobs':
                    {
                        // 高斯簇 - 调整簇的分离度和紧凑度
                        const blobCenters = [
                            [-8, -8], [8, -8], [-8, 8], [8, 8]
                        ];

                        result.forEach(d => {
                            const center = blobCenters[d.cluster];
                            const angle = Math.random() * Math.PI * 2;
                            const dist = Math.random() * 5 * clusterScale;

                            d.x = center[0] + Math.cos(angle) * dist + (Math.random() - 0.5) * noiseLevel;
                            d.y = center[1] + Math.sin(angle) * dist + (Math.random() - 0.5) * noiseLevel;
                        });

                        break;
                    }

                case 'spiral':
                    // 螺旋 - 调整螺旋的保留程度
                    result.forEach(d => {
                        // 基于原始数据的位置，但保留螺旋形状
                        const originalX = d.x - 175;
                        const originalY = d.y - 175;
                        const angle = Math.atan2(originalY, originalX);
                        const r = Math.sqrt(originalX * originalX + originalY * originalY);

                        // 大的n_neighbors会使螺旋的分离不那么明显
                        const spiralFactor = 1.0 - (nNeighbors / 100) * 0.5;

                        d.x = r / 50 * Math.cos(angle) * spiralFactor * (d.cluster === 0 ? -1 : 1);
                        d.y = r / 50 * Math.sin(angle) * spiralFactor;

                        // 添加一些噪声
                        d.x += (Math.random() - 0.5) * noiseLevel;
                        d.y += (Math.random() - 0.5) * noiseLevel;
                    });
                    break;

                case 'moons':
                    // 半月形 - 调整形状的保留程度
                    result.forEach(d => {
                        const sign = d.cluster === 0 ? 1 : -1;

                        // 计算相对位置
                        const relX = d.x - 175;
                        const relY = d.y - 175 - (d.cluster === 0 ? 0 : 25);

                        // 计算角度位置
                        const angle = Math.atan2(relY, relX * sign);

                        // 大的n_neighbors会使形状更平滑
                        const shapeFactor = 1.0 - (nNeighbors / 100) * 0.5;

                        d.x = sign * Math.cos(angle) * 5 * shapeFactor;
                        d.y = Math.sin(angle) * 5 * shapeFactor - (d.cluster === 0 ? 0 : 2);

                        // 添加一些噪声
                        d.x += (Math.random() - 0.5) * noiseLevel * 0.5;
                        d.y += (Math.random() - 0.5) * noiseLevel * 0.5;
                    });
                    break;
            }

            // min_dist影响点之间的最小距离
            const scaleFactor = 1.5 + minDist * 2; // min_dist越大，点分布越分散
            result.forEach(d => {
                d.x *= scaleFactor;
                d.y *= scaleFactor;
            });

            return result;
        },

        changeDataset() {
            this.updateVisualization();
        },

        checkRecommendation() {
            this.recommendationCompleted = true;

            // 检查每个参数的正确性
            this.isNeighborsCorrect = this.recommendedNeighbors === 3; // 大n_neighbors最适合全局结构
            this.isMinDistCorrect = this.recommendedMinDist === 2;    // 中等min_dist平衡了紧凑性和分散性
            this.isMetricCorrect = this.recommendedMetric === 1;      // euclidean是一般数据的标准选择

            this.allCorrect = this.isNeighborsCorrect && this.isMinDistCorrect && this.isMetricCorrect;

            if (this.allCorrect || ++this.retries >= 1) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },

        resetRecommendation() {
            this.recommendationCompleted = false;
            this.recommendedNeighbors = null;
            this.recommendedMinDist = null;
            this.recommendedMetric = null;
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    }
}
</script>

<style scoped>
.el-slider {
    width: 100%;
}

.section-container {
    margin-bottom: 40px;
}

.section-card {
    margin-bottom: 20px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.markdown-content {
    margin-bottom: 30px;
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.parameter-controls {
    margin-bottom: 20px;
}

.parameter-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    flex-wrap: wrap;
}

.parameter-item span {
    width: 170px;
    margin-right: 15px;
}

.parameter-value {
    width: 50px;
    text-align: right;
    margin-left: 15px;
    color: #606266;
}

.visualizations {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 20px 0;
}

.visualization-panel {
    flex: 1;
    min-width: 300px;
}

.visualization-panel h4 {
    text-align: center;
    margin-bottom: 10px;
}

.viz-container {
    width: 100%;
    height: 300px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
    background-color: white;
}

.parameter-explanation {
    margin: 20px 0;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.recommendation-activity {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px dashed #dcdfe6;
}

.scenario {
    margin-top: 15px;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.recommendation-form {
    margin-top: 20px;
}

.form-item {
    margin-bottom: 15px;
}

.form-item span {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
}

.form-item .el-radio-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-left: 20px;
}

.submit-btn {
    margin-top: 20px;
}

.response-container {
    margin-top: 20px;
}

.recommendation-results {
    margin-top: 20px;
    padding: 15px;
    background-color: #f2f6fc;
    border-radius: 4px;
}

.param-feedback {
    margin-bottom: 15px;
}

.retry-btn {
    margin-top: 15px;
}

.next-section {
    margin-top: 20px;
    text-align: center;
}

/* 全局样式适配 */
:deep(h2) {
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    margin-top: 20px;
}

:deep(blockquote) {
    border-left: 4px solid #409EFF;
    padding-left: 15px;
    color: #606266;
    margin: 20px 0;
}

:deep(p) {
    line-height: 1.6;
}

:deep(strong) {
    color: #409EFF;
}

:deep(ul),
:deep(ol) {
    padding-left: 20px;
    line-height: 1.6;
}
</style>
