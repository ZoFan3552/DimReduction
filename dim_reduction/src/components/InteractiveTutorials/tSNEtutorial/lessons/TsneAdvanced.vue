<template>
    <div class="lesson-container">
        <h2>Lesson 6: Advanced t-SNE Techniques</h2>

        <div class="lesson-content">
            <p class="intro">
                在前面的课程中，我们已经掌握了t-SNE的基本原理和参数调整。本节将深入探讨t-SNE的高级应用技巧，
                包括处理大规模数据、不同初始化策略、以及t-SNE结果的解释注意事项。
            </p>

            <div class="section">
                <h3>大规模数据的t-SNE处理策略</h3>

                <div class="technique-card">
                    <h4>Barnes-Hut t-SNE</h4>
                    <p>
                        标准t-SNE的计算复杂度为O(N²)，这使得它在处理大型数据集时非常慢。Barnes-Hut近似算法将复杂度降低到O(N log N)，
                        使t-SNE能够处理更大规模的数据。
                    </p>
                    <div class="interactive-demo">
                        <div class="demo-controls">
                            <label>
                                数据规模:
                                <select v-model="dataSize" @change="updateBarnesHutDemo">
                                    <option value="1000">1,000点</option>
                                    <option value="5000">5,000点</option>
                                    <option value="10000">10,000点</option>
                                </select>
                            </label>
                            <label>
                                <input type="checkbox" v-model="useBarnesHut" @change="updateBarnesHutDemo">
                                启用Barnes-Hut加速
                            </label>
                        </div>
                        <div class="demo-visualization">
                            <canvas ref="barnesHutCanvas" width="500" height="300"></canvas>
                            <div v-if="isComputing" class="computing-overlay">
                                <div class="spinner"></div>
                                <p>计算中... 预计时间: {{ computationTimeEstimate }}</p>
                            </div>
                        </div>
                        <div class="performance-metrics">
                            <p>计算时间: {{ computationTime }}ms</p>
                            <p>内存使用: {{ memoryUsage }}MB</p>
                        </div>
                    </div>
                </div>

                <div class="technique-card">
                    <h4>降采样策略</h4>
                    <p>
                        对于超大规模数据集，可以先对数据进行降采样，在一个较小的代表性样本上运行t-SNE，
                        然后使用插值技术将剩余点映射到降维空间。
                    </p>
                    <div class="technique-visualization">
                        <!-- <img src="@/assets/tsne/downsampling_tsne.png" alt="降采样t-SNE示例"> -->
                        <p class="caption">
                            左图: 对10%数据进行t-SNE后，使用Nystrom方法将剩余90%数据映射到同一空间
                            右图: 对全量数据直接应用t-SNE的结果
                        </p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>初始化策略</h3>
                <p>
                    t-SNE算法对初始点位置敏感，不同的初始化可能导致不同的结果。以下是几种常用的初始化策略。
                </p>

                <div class="initialization-demo">
                    <div class="init-controls">
                        <label>选择初始化方法:</label>
                        <div class="radio-group">
                            <label>
                                <input type="radio" v-model="initMethod" value="random" @change="updateInitDemo">
                                随机初始化
                            </label>
                            <label>
                                <input type="radio" v-model="initMethod" value="pca" @change="updateInitDemo">
                                PCA初始化
                            </label>
                            <label>
                                <input type="radio" v-model="initMethod" value="spectral" @change="updateInitDemo">
                                谱嵌入初始化
                            </label>
                        </div>
                        <button @click="runMultipleInits" :disabled="isComputing">运行多次比较</button>
                    </div>

                    <div class="init-visualization">
                        <canvas ref="initCanvas" width="500" height="300"></canvas>
                    </div>

                    <div class="init-comparison" v-if="showMultipleInits">
                        <h4>不同初始化方法的比较</h4>
                        <div class="comparison-grid">
                            <div v-for="(result, index) in initResults" :key="index" class="comparison-item">
                                <p>{{ result.method }} 初始化</p>
                                <canvas :ref="`comparisonCanvas${index}`" width="250" height="200"></canvas>
                                <p>KL散度: {{ result.klDivergence.toFixed(4) }}</p>
                            </div>
                        </div>
                        <p class="analysis">
                            从上面的比较可以看出，PCA初始化通常比随机初始化收敛更快，并且往往能得到更低的KL散度。
                            对于某些数据集，谱嵌入初始化可能提供更好的起点，特别是当数据具有明显的流形结构时。
                        </p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>t-SNE结果解释的注意事项</h3>

                <div class="warning-card">
                    <h4>注意: t-SNE的常见误解</h4>
                    <ul>
                        <li>
                            <strong>簇大小无意义:</strong> t-SNE中簇的大小不反映原始空间中的方差或重要性
                        </li>
                        <li>
                            <strong>簇间距离模糊化:</strong> t-SNE关注局部结构，簇间的全局距离被扭曲
                        </li>
                        <li>
                            <strong>随机性影响:</strong> 不同运行可能产生不同结果，尤其是形状和旋转
                        </li>
                        <li>
                            <strong>密度保持有限:</strong> t-SNE不完全保持原始空间的点密度
                        </li>
                    </ul>
                </div>

                <div class="interpretation-examples">
                    <h4>案例分析: 合理与不合理的解释</h4>

                    <div class="example-card">
                        <h5>不合理解释示例</h5>
                        <!-- <img src="@/assets/tsne/misinterpretation.png" alt="t-SNE误解示例"> -->
                        <p class="incorrect">
                            "从t-SNE图中可以看出，蓝色簇比红色簇更紧密，说明蓝色类别的样本更相似；
                            而且两个簇之间的距离很大，表明这两类数据完全不同。"
                        </p>
                        <p class="correction">
                            <strong>为什么不对:</strong> t-SNE主要保留局部结构，簇的紧密程度和簇间距离在t-SNE结果中可能被夸大或缩小，
                            不能直接用于判断原始数据的整体相似性或类别差异程度。
                        </p>
                    </div>

                    <div class="example-card">
                        <h5>合理解释示例</h5>
                        <!-- <img src="@/assets/tsne/correct_interpretation.png" alt="t-SNE正确解释示例"> -->
                        <p class="correct">
                            "t-SNE结果显示数据形成了多个局部簇，表明数据可能包含多个子类或子结构。
                            特别是，标记为类别A的点分布在多个不同簇中，这可能意味着类别A在特征空间中不是线性可分的，
                            或者类别A本身包含多个子类型。"
                        </p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>t-SNE与其他降维方法的比较</h3>

                <div class="comparison-tool">
                    <div class="method-selector">
                        <label>选择要比较的方法:</label>
                        <div class="checkbox-group">
                            <label>
                                <input type="checkbox" v-model="showPCA" @change="updateComparisonView">
                                PCA
                            </label>
                            <label>
                                <input type="checkbox" v-model="showMDS" @change="updateComparisonView">
                                MDS
                            </label>
                            <label>
                                <input type="checkbox" v-model="showIsomap" @change="updateComparisonView">
                                Isomap
                            </label>
                            <label>
                                <input type="checkbox" v-model="showUMAP" @change="updateComparisonView">
                                UMAP
                            </label>
                            <label>
                                <input type="checkbox" v-model="showTSNE" @change="updateComparisonView" checked>
                                t-SNE
                            </label>
                        </div>
                    </div>

                    <div class="dataset-selector">
                        <label>选择数据集:</label>
                        <select v-model="comparisonDataset" @change="updateComparisonView">
                            <option value="mnist">MNIST数字</option>
                            <option value="swiss_roll">Swiss Roll</option>
                            <option value="s_curve">S曲线</option>
                        </select>
                    </div>

                    <div class="comparison-visualization">
                        <div v-if="isLoadingComparison" class="loading-overlay">
                            <div class="spinner"></div>
                            <p>生成比较结果...</p>
                        </div>
                        <div class="comparison-grid">
                            <div v-if="showPCA" class="comparison-item">
                                <h5>PCA</h5>
                                <canvas ref="pcaCanvas" width="250" height="200"></canvas>
                                <p>优点: 计算快速，保留全局方差</p>
                                <p>缺点: 仅捕获线性关系</p>
                            </div>
                            <div v-if="showMDS" class="comparison-item">
                                <h5>MDS</h5>
                                <canvas ref="mdsCanvas" width="250" height="200"></canvas>
                                <p>优点: 保留点间欧氏距离</p>
                                <p>缺点: 计算复杂度高</p>
                            </div>
                            <div v-if="showIsomap" class="comparison-item">
                                <h5>Isomap</h5>
                                <canvas ref="isomapCanvas" width="250" height="200"></canvas>
                                <p>优点: 捕获非线性流形结构</p>
                                <p>缺点: 对噪声敏感</p>
                            </div>
                            <div v-if="showUMAP" class="comparison-item">
                                <h5>UMAP</h5>
                                <canvas ref="umapCanvas" width="250" height="200"></canvas>
                                <p>优点: 速度快，保留全局结构</p>
                                <p>缺点: 参数调整复杂</p>
                            </div>
                            <div v-if="showTSNE" class="comparison-item">
                                <h5>t-SNE</h5>
                                <canvas ref="tsneComparisonCanvas" width="250" height="200"></canvas>
                                <p>优点: 优秀的局部结构保留</p>
                                <p>缺点: 全局结构可能失真</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="method-selection-guide">
                    <h4>降维方法选择指南</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>目标</th>
                                <th>推荐方法</th>
                                <th>说明</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>探索性数据分析</td>
                                <td>t-SNE, UMAP</td>
                                <td>优秀的聚类可视化能力</td>
                            </tr>
                            <tr>
                                <td>保留全局结构</td>
                                <td>PCA, UMAP</td>
                                <td>更好地保留全局距离关系</td>
                            </tr>
                            <tr>
                                <td>快速处理大数据</td>
                                <td>UMAP, PCA</td>
                                <td>计算效率高</td>
                            </tr>
                            <tr>
                                <td>发现非线性关系</td>
                                <td>t-SNE, UMAP, Isomap</td>
                                <td>能捕获复杂的非线性结构</td>
                            </tr>
                            <tr>
                                <td>后续机器学习</td>
                                <td>PCA, UMAP</td>
                                <td>更稳定，新数据可投影</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="practical-exercise">
                <h3>实践挑战</h3>
                <p>尝试以下高级应用挑战，巩固您对t-SNE的理解：</p>

                <div class="exercise-card">
                    <h4>挑战1: 优化超大数据集的t-SNE</h4>
                    <p>
                        使用提供的20,000样本数据集，尝试不同的策略来优化t-SNE计算，目标是在保持良好可视化效果的同时，
                        将计算时间控制在可接受范围内。
                    </p>
                    <button @click="startExercise(1)" :disabled="exerciseInProgress">开始挑战</button>
                </div>

                <div class="exercise-card">
                    <h4>挑战2: 多次t-SNE运行的稳定性分析</h4>
                    <p>
                        对同一数据集运行多次t-SNE（使用不同的随机种子），分析结果的稳定性和变异性。
                        尝试找出最稳定和最不稳定的数据特征。
                    </p>
                    <button @click="startExercise(2)" :disabled="exerciseInProgress">开始挑战</button>
                </div>
            </div>
        </div>


    </div>
</template>

<script>
import * as d3 from 'd3';
// import TSNE from 'tsne-js';
// import { loadDataset, generateSyntheticData } from '@/utils/dataLoader';
// import { runPCA, runMDS, runIsomap, runUMAP } from '@/utils/dimensionReduction';

export default {
    name: 'Lesson6TsneAdvanced',
    data() {
        return {
            // Barnes-Hut演示相关
            dataSize: '5000',
            useBarnesHut: true,
            computationTime: 0,
            computationTimeEstimate: '< 1分钟',
            memoryUsage: 0,
            isComputing: false,

            // 初始化策略相关
            initMethod: 'pca',
            showMultipleInits: false,
            initResults: [],

            // 降维方法比较相关
            showPCA: true,
            showMDS: false,
            showIsomap: false,
            showUMAP: true,
            showTSNE: true,
            comparisonDataset: 'mnist',
            isLoadingComparison: false,

            // 练习相关
            exerciseInProgress: false,
            currentExercise: null
        };
    },
    mounted() {
        this.initializeBarnesHutDemo();
        this.initializeInitDemo();
        this.updateComparisonView();
    },
    methods: {
        async initializeBarnesHutDemo() {
            // this.isComputing = true;

            // try {
            //     // 生成合成数据或加载示例数据
            //     const numPoints = parseInt(this.dataSize);
            //     const data = await generateSyntheticData('gaussian_clusters', numPoints);

            //     const startTime = performance.now();

            //     // 运行t-SNE（使用或不使用Barnes-Hut加速）
            //     const tsne = new TSNE({
            //         dim: 2,
            //         perplexity: 30,
            //         earlyExaggeration: 12,
            //         learningRate: 200,
            //         nIter: 250,
            //         metric: 'euclidean',
            //         // 配置Barnes-Hut参数
            //         theta: this.useBarnesHut ? 0.5 : 0.0 // 0表示精确计算，>0启用Barnes-Hut
            //     });

            //     tsne.init({
            //         data: data,
            //         type: 'dense'
            //     });

            //     // 运行t-SNE
            //     tsne.run();

            //     const endTime = performance.now();
            //     this.computationTime = Math.round(endTime - startTime);

            //     // 模拟内存使用计算
            //     this.memoryUsage = Math.round((numPoints * numPoints * 8) / (1024 * 1024) * (this.useBarnesHut ? 0.2 : 1));

            //     // 可视化结果
            //     const embedding = tsne.getOutputScaled();
            //     this.visualizeResult(embedding, this.$refs.barnesHutCanvas);
            // } catch (error) {
            //     console.error('Barnes-Hut演示错误:', error);
            // } finally {
            //     this.isComputing = false;
            // }
        },

        updateBarnesHutDemo() {
            // 更新计算时间估计
            const numPoints = parseInt(this.dataSize);
            if (numPoints <= 5000) {
                this.computationTimeEstimate = this.useBarnesHut ? '< 30秒' : '< 1分钟';
            } else {
                this.computationTimeEstimate = this.useBarnesHut ? '< 2分钟' : '5-10分钟';
            }

            this.initializeBarnesHutDemo();
        },

        async initializeInitDemo() {
            // this.isComputing = true;

            // try {
            //     // 加载数据
            //     const { data, labels } = await loadDataset('mnist', 1000);

            //     // 根据选择的初始化方法运行t-SNE
            //     let initialY;
            //     if (this.initMethod === 'pca') {
            //         // 使用PCA进行初始化
            //         initialY = await runPCA(data, 2);
            //     } else if (this.initMethod === 'spectral') {
            //         // 使用谱嵌入初始化
            //         // 这里简化实现，实际应使用专门的谱嵌入库
            //         const tempResult = await runPCA(data, 2); // 临时用PCA代替
            //         initialY = tempResult.map(p => [p[0] * 1.2, p[1] * 0.8]); // 略微变形以区分
            //     } else {
            //         // 随机初始化不需要预计算
            //         initialY = null;
            //     }

            //     // 运行t-SNE
            //     const tsne = new TSNE({
            //         dim: 2,
            //         perplexity: 30,
            //         earlyExaggeration: 12,
            //         learningRate: 200,
            //         nIter: 300,
            //         metric: 'euclidean'
            //     });

            //     tsne.init({
            //         data: data,
            //         type: 'dense',
            //         // 如果有预计算的初始位置，则使用它
            //         Y: initialY
            //     });

            //     // 运行t-SNE
            //     tsne.run();

            //     // 获取结果并可视化
            //     const embedding = tsne.getOutputScaled();

            //     // 使用D3为不同类别着色
            //     this.visualizeResultWithLabels(embedding, labels, this.$refs.initCanvas);
            // } catch (error) {
            //     console.error('初始化演示错误:', error);
            // } finally {
            //     this.isComputing = false;
            // }
        },

        updateInitDemo() {
            this.initializeInitDemo();
        },

        async runMultipleInits() {
            // this.isComputing = true;
            // this.showMultipleInits = true;
            // this.initResults = [];

            // try {
            //     // 加载数据
            //     const { data, labels } = await loadDataset('mnist', 1000);

            //     // 运行三种不同的初始化方法
            //     const methods = ['random', 'pca', 'spectral'];

            //     for (const method of methods) {
            //         let initialY;

            //         if (method === 'pca') {
            //             initialY = await runPCA(data, 2);
            //         } else if (method === 'spectral') {
            //             // 简化实现
            //             const tempResult = await runPCA(data, 2);
            //             initialY = tempResult.map(p => [p[0] * 1.2, p[1] * 0.8]);
            //         } else {
            //             initialY = null;
            //         }

            //         // 运行t-SNE
            //         const tsne = new TSNE({
            //             dim: 2,
            //             perplexity: 30,
            //             earlyExaggeration: 12,
            //             learningRate: 200,
            //             nIter: 300,
            //             metric: 'euclidean'
            //         });

            //         tsne.init({
            //             data: data,
            //             type: 'dense',
            //             Y: initialY
            //         });

            //         // 运行t-SNE
            //         tsne.run();

            //         // 获取结果
            //         const embedding = tsne.getOutputScaled();

            //         // 计算KL散度（从tsne实例获取）
            //         const klDivergence = tsne.getKL ? tsne.getKL() : Math.random() * 0.5 + 0.1; // 模拟值

            //         this.initResults.push({
            //             method: method.charAt(0).toUpperCase() + method.slice(1),
            //             embedding: embedding,
            //             labels: labels,
            //             klDivergence: klDivergence
            //         });
            //     }

            //     // 在下一个tick绘制结果，确保DOM已更新
            //     this.$nextTick(() => {
            //         this.initResults.forEach((result, index) => {
            //             const canvas = this.$refs[`comparisonCanvas${index}`][0];
            //             this.visualizeResultWithLabels(result.embedding, result.labels, canvas);
            //         });
            //     });
            // } catch (error) {
            //     console.error('多次初始化比较错误:', error);
            // } finally {
            //     this.isComputing = false;
            // }
        },

        async updateComparisonView() {
            // this.isLoadingComparison = true;

            // try {
            //     // 加载选定的数据集
            //     const { data, labels } = await loadDataset(this.comparisonDataset, 1000);

            //     // 为每个选定的方法运行降维
            //     if (this.showPCA) {
            //         const pcaResult = await runPCA(data, 2);
            //         this.$nextTick(() => {
            //             this.visualizeResultWithLabels(pcaResult, labels, this.$refs.pcaCanvas);
            //         });
            //     }

            //     if (this.showMDS) {
            //         const mdsResult = await runMDS(data, 2);
            //         this.$nextTick(() => {
            //             this.visualizeResultWithLabels(mdsResult, labels, this.$refs.mdsCanvas);
            //         });
            //     }

            //     if (this.showIsomap) {
            //         const isomapResult = await runIsomap(data, 2);
            //         this.$nextTick(() => {
            //             this.visualizeResultWithLabels(isomapResult, labels, this.$refs.isomapCanvas);
            //         });
            //     }

            //     if (this.showUMAP) {
            //         const umapResult = await runUMAP(data, 2);
            //         this.$nextTick(() => {
            //             this.visualizeResultWithLabels(umapResult, labels, this.$refs.umapCanvas);
            //         });
            //     }

            //     if (this.showTSNE) {
            //         // 运行t-SNE
            //         const tsne = new TSNE({
            //             dim: 2,
            //             perplexity: 30,
            //             earlyExaggeration: 12,
            //             learningRate: 200,
            //             nIter: 300,
            //             metric: 'euclidean'
            //         });

            //         tsne.init({
            //             data: data,
            //             type: 'dense'
            //         });

            //         tsne.run();

            //         const tsneResult = tsne.getOutputScaled();
            //         this.$nextTick(() => {
            //             this.visualizeResultWithLabels(tsneResult, labels, this.$refs.tsneComparisonCanvas);
            //         });
            //     }
            // } catch (error) {
            //     console.error('降维方法比较错误:', error);
            // } finally {
            //     this.isLoadingComparison = false;
            // }
        },

        visualizeResult(embedding, canvas) {
            const ctx = canvas.getContext('2d');
            const width = canvas.width;
            const height = canvas.height;

            // 清空画布
            ctx.clearRect(0, 0, width, height);

            // 计算缩放比例，使点分布在画布上
            const xExtent = d3.extent(embedding, d => d[0]);
            const yExtent = d3.extent(embedding, d => d[1]);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - 5, xExtent[1] + 5])
                .range([30, width - 30]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - 5, yExtent[1] + 5])
                .range([30, height - 30]);

            // 绘制数据点
            embedding.forEach(d => {
                const x = xScale(d[0]);
                const y = yScale(d[1]);

                ctx.beginPath();
                ctx.arc(x, y, 3, 0, 2 * Math.PI);
                ctx.fillStyle = '#3498db';
                ctx.fill();
            });
        },

        visualizeResultWithLabels(embedding, labels, canvas) {
            const ctx = canvas.getContext('2d');
            const width = canvas.width;
            const height = canvas.height;

            // 清空画布
            ctx.clearRect(0, 0, width, height);

            // 计算缩放比例，使点分布在画布上
            const xExtent = d3.extent(embedding, d => d[0]);
            const yExtent = d3.extent(embedding, d => d[1]);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - 5, xExtent[1] + 5])
                .range([30, width - 30]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - 5, yExtent[1] + 5])
                .range([30, height - 30]);

            // 为不同类别定义颜色
            const colors = d3.scaleOrdinal(d3.schemeCategory10);

            // 绘制数据点
            embedding.forEach((d, i) => {
                const x = xScale(d[0]);
                const y = yScale(d[1]);

                ctx.beginPath();
                ctx.arc(x, y, 3, 0, 2 * Math.PI);

                // 如果有标签，使用标签为点着色
                if (labels && labels.length > 0) {
                    ctx.fillStyle = colors(labels[i]);
                } else {
                    ctx.fillStyle = '#3498db';
                }

                ctx.fill();
            });
        },

        async startExercise(exerciseId) {
            this.exerciseInProgress = true;
            this.currentExercise = exerciseId;

            // 实际实现中这里可以打开专门的练习页面或者显示练习指导
            alert(`练习${exerciseId}即将开始！实际项目中这里应该跳转到专门的练习环境。`);

            this.exerciseInProgress = false;
        },

        previousLesson() {
            this.$router.push('/lesson5');
        },

        nextLesson() {
            this.$router.push('/lesson7');
        }
    }
};
</script>

<style scoped>
.lesson-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h2 {
    color: #2c3e50;
    margin-bottom: 25px;
    text-align: center;
}

.lesson-content {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.intro {
    font-size: 1.1em;
    line-height: 1.6;
}

.section {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    margin-bottom: 30px;
}

.section h3 {
    color: #2c3e50;
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e0e0e0;
}

.technique-card,
.example-card,
.exercise-card {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.interactive-demo,
.technique-visualization {
    margin: 15px 0;
}

.demo-controls,
.init-controls {
    margin-bottom: 15px;
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: center;
}

.demo-visualization,
.init-visualization {
    position: relative;
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow: hidden;
    margin: 15px 0;
}

canvas {
    display: block;
    background-color: white;
    width: 100%;
    height: auto;
}

.computing-overlay,
.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.spinner {
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.performance-metrics {
    display: flex;
    justify-content: space-between;
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 4px;
    margin-top: 10px;
}

.technique-visualization img {
    max-width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.caption {
    font-size: 0.9em;
    color: #666;
    text-align: center;
    margin-top: 5px;
}

.radio-group,
.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
}

.radio-group label,
.checkbox-group label {
    display: flex;
    align-items: center;
    gap: 5px;
}

.init-comparison {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px dashed #ddd;
}

.comparison-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.comparison-item {
    text-align: center;
}

.comparison-item p {
    margin: 5px 0;
    font-size: 0.9em;
}

.analysis {
    background-color: #f0f8ff;
    padding: 15px;
    border-radius: 4px;
    border-left: 4px solid #3498db;
}

.warning-card {
    background-color: #fff5f5;
    border-left: 4px solid #e74c3c;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 4px;
}

.warning-card ul {
    padding-left: 20px;
    margin: 10px 0;
}

.warning-card li {
    margin-bottom: 8px;
}

.interpretation-examples {
    margin-top: 20px;
}

.example-card h5 {
    margin-top: 0;
    color: #2c3e50;
}

.example-card img {
    max-width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin: 10px 0;
}

.incorrect {
    color: #e74c3c;
    font-style: italic;
}

.correction {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 4px;
    margin-top: 10px;
}

.correct {
    color: #27ae60;
}

.method-selector,
.dataset-selector {
    margin-bottom: 15px;
}

.method-selection-guide {
    margin-top: 30px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
}

table th,
table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

table th {
    background-color: #f8f9fa;
}

table tr:nth-child(even) {
    background-color: #f8f9fa;
}

.practical-exercise {
    margin-top: 40px;
}

.exercise-card h4 {
    margin-top: 0;
    color: #2c3e50;
}

.exercise-card button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.exercise-card button:hover {
    background-color: #2980b9;
}

.exercise-card button:disabled {
    background-color: #bdc3c7;
    cursor: not-allowed;
}

.navigation-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 40px;
}

.navigation-buttons button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.navigation-buttons button:hover {
    background-color: #2980b9;
}

@media (max-width: 768px) {
    .comparison-grid {
        grid-template-columns: 1fr;
    }

    .effect-examples {
        flex-direction: column;
    }

    .demo-controls,
    .init-controls {
        flex-direction: column;
        align-items: flex-start;
    }

    .radio-group,
    .checkbox-group {
        flex-direction: column;
    }
}
</style>
