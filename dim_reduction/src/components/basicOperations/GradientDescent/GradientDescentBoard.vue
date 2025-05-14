<template>
    <div class="gradient-descent-container">
        <el-alert v-if="!nodeData" title="请先选择节点" type="warning" :closable="false" show-icon>
        </el-alert>

        <div v-else>
            <el-card class="algorithm-card">
                <div slot="header">
                    <span>梯度下降算法选择</span>
                </div>
                <el-tabs v-model="activeTab" @tab-click="handleTabClick">
                    <el-tab-pane label="t-SNE梯度下降" name="tsne">
                        <div class="formula-card">
                            <h3>t-SNE 成本函数</h3>
                            <div ref="tsne_cost_formula" class="formula"></div>
                            <h3>t-SNE 梯度函数</h3>
                            <div ref="tsne_gradient_formula" class="formula"></div>
                            <div class="description">
                                t-SNE使用t分布来模拟低维相似度，相比SNE能够更好地保留局部结构。
                            </div>
                        </div>
                    </el-tab-pane>

                    <el-tab-pane label="SNE梯度下降" name="sne">
                        <div class="formula-card">
                            <h3>SNE 成本函数</h3>
                            <div ref="sne_cost_formula" class="formula"></div>
                            <h3>SNE 梯度函数</h3>
                            <div ref="sne_gradient_formula" class="formula"></div>
                            <div class="description">
                                SNE使用高斯分布来模拟低维相似度，通过KL散度最小化高维和低维相似度矩阵之间的差异。
                            </div>
                        </div>
                    </el-tab-pane>

                    <el-tab-pane label="UMAP梯度下降" name="umap">
                        <div class="formula-card">
                            <h3>UMAP 成本函数</h3>
                            <div ref="umap_cost_formula" class="formula"></div>
                            <h3>UMAP 梯度函数</h3>
                            <div ref="umap_gradient_formula" class="formula"></div>
                            <div class="description">
                                UMAP基于黎曼几何和代数拓扑，相比t-SNE具有更快的收敛速度和更好的全局结构保留能力。
                            </div>
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </el-card>

            <el-card class="parameter-card">
                <div slot="header">
                    <span>参数配置</span>
                </div>

                <div class="optimization-formula-card">
                    <h3>梯度下降更新公式</h3>
                    <div ref="gradient_descent_formula" class="formula"></div>
                    <h3>动量梯度下降更新公式</h3>
                    <div ref="momentum_formula" class="formula"></div>
                    <div class="description">
                        <ul>
                            <li><b>学习率(η)</b>：控制每次更新的步长大小。过大可能导致发散，过小则收敛缓慢。</li>
                            <li><b>动量(α)</b>：加速收敛并帮助跳出局部最小值。通常设置为0.5~0.9之间。</li>
                            <li><b>迭代次数</b>：算法运行的总步数，足够大以确保收敛。</li>
                            <li><b>记录间隔</b>：每隔多少步记录一次状态，用于可视化算法进展。</li>
                        </ul>
                    </div>
                </div>

                <el-form ref="form" :model="parameters" label-width="120px">
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-form-item label="迭代次数">
                                <el-input-number v-model="parameters.iterations" :min="100" :max="5000"
                                    :step="100"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="学习率">
                                <el-input-number v-model="parameters.learning_rate" :min="10" :max="1000" :step="10"
                                    :precision="0"></el-input-number>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-form-item label="动量">
                                <el-input-number v-model="parameters.momentum" :min="0" :max="1" :step="0.1"
                                    :precision="1"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="记录间隔">
                                <el-input-number v-model="parameters.recording_interval" :min="1" :max="100"
                                    :step="1"></el-input-number>
                                <div class="hint">每隔多少次迭代记录一次状态</div>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row v-if="activeTab === 'tsne' || activeTab === 'sne'">
                        <el-col :span="12">
                            <el-form-item label="困惑度">
                                <el-input-number v-model="parameters.perplexity" :min="5" :max="50"
                                    :step="5"></el-input-number>
                                <div class="hint">t-SNE/SNE的邻居数量参数</div>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row v-if="activeTab === 'umap'">
                        <el-col :span="12">
                            <el-form-item label="邻居数量">
                                <el-input-number v-model="parameters.n_neighbors" :min="5" :max="50"
                                    :step="5"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="最小距离">
                                <el-input-number v-model="parameters.min_dist" :min="0.01" :max="0.99" :step="0.01"
                                    :precision="2"></el-input-number>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>

                <div class="data-check">
                    <el-alert v-if="!dataCheck.hasHighSimilarity && needsHighSimilarity" title="警告：缺少高维相似度矩阵，无法进行计算"
                        type="error" :closable="false" show-icon>
                    </el-alert>
                    <el-alert v-if="!dataCheck.hasLowSimilarity && needsLowSimilarity" title="警告：缺少低维相似度矩阵，无法进行计算"
                        type="error" :closable="false" show-icon>
                    </el-alert>
                    <el-alert v-if="!dataCheck.hasDataset" title="警告：缺少低维数据集，无法进行计算" type="error" :closable="false"
                        show-icon>
                    </el-alert>
                </div>

                <div class="form-actions">
                    <el-button type="primary" @click="runGradientDescent" :disabled="!canRunAlgorithm"
                        :loading="isLoading">
                        运行梯度下降
                    </el-button>
                </div>
            </el-card>

            <el-card v-if="iterationData.length > 0" class="visualization-card">
                <div slot="header">
                    <span>可视化</span>
                </div>

                <!-- 可视化类型选择(卡片式) -->
                <el-tabs v-model="visualizationMode" @tab-click="handleVisualizationChange" type="card">
                    <el-tab-pane label="散点图" name="scatter"></el-tab-pane>
                    <el-tab-pane label="成本函数曲线" name="cost"></el-tab-pane>
                    <el-tab-pane label="梯度范数曲线" name="gradient"></el-tab-pane>
                </el-tabs>

                <!-- 散点图迭代控制 -->
                <div v-if="visualizationMode === 'scatter'" class="iteration-controls">
                    <div class="slider-container">
                        <span class="slider-label">迭代进度：</span>
                        <div class="navigation-buttons">
                            <el-button size="mini" icon="el-icon-arrow-left" @click="previousIteration"
                                :disabled="iterationSlider <= 0">
                                上一步
                            </el-button>
                            <span class="iteration-display">{{ formatIterationTooltip(iterationSlider) }}</span>
                            <el-button size="mini" icon="el-icon-arrow-right" @click="nextIteration"
                                :disabled="iterationSlider >= iterationData.length - 1">
                                下一步
                            </el-button>
                        </div>
                    </div>
                    <div class="slider-wrapper">
                        <el-slider v-model="iterationSlider" :min="0" :max="iterationData.length - 1"
                            :format-tooltip="formatIterationTooltip" @input="updateVisualization" :show-tooltip="true">
                        </el-slider>
                    </div>
                </div>

                <div ref="visualization" class="visualization-container"></div>
            </el-card>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import katex from 'katex';
import 'katex/dist/katex.min.css';

export default {
    name: 'GradientDescentVisualizer',
    props: {
        nodeData: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            activeTab: 'tsne',
            parameters: {
                iterations: 1000,
                learning_rate: 200,
                momentum: 0.8,
                perplexity: 30,
                n_neighbors: 15,
                min_dist: 0.1,
                recording_interval: 10
            },
            isLoading: false,
            chart: null,
            iterationData: [],
            visualizationMode: 'scatter',
            iterationSlider: 0,
            formulas: {
                tsne: {
                    cost: '\\mathcal{C} = \\sum_i \\sum_j p_{ij} \\log\\frac{p_{ij}}{q_{ij}}',
                    gradient: '\\frac{\\partial \\mathcal{C}}{\\partial y_i} = 4 \\sum_j (p_{ij} - q_{ij}) (y_i - y_j) (1 + ||y_i - y_j||^2)^{-1}'
                },
                sne: {
                    cost: '\\mathcal{C} = \\sum_i \\sum_j p_{ij} \\log\\frac{p_{ij}}{q_{ij}}',
                    gradient: '\\frac{\\partial \\mathcal{C}}{\\partial y_i} = 2 \\sum_j (p_{ij} - q_{ij}) (y_i - y_j)'
                },
                umap: {
                    cost: '\\mathcal{C} = \\sum_{i < j} [p_{ij} \\log(p_{ij} \\sigma(d(y_i, y_j))) + (1 - p_{ij})\\log(1 - p_{ij}\\sigma(d(y_i, y_j)))]',
                    gradient: '\\frac{\\partial \\mathcal{C}}{\\partial y_i} = \\sum_j \\frac{\\partial \\mathcal{C}}{\\partial d(y_i, y_j)} \\frac{\\partial d(y_i, y_j)}{\\partial y_i}'
                },
                optimization: {
                    gradient_descent: 'y^{(t+1)} = y^{(t)} - \\eta \\nabla \\mathcal{C}(y^{(t)})',
                    momentum: 'v^{(t+1)} = \\alpha v^{(t)} - \\eta \\nabla \\mathcal{C}(y^{(t)}) \\\\ y^{(t+1)} = y^{(t)} + v^{(t+1)}'
                }
            }
        };
    },
    computed: {
        dataCheck() {
            if (!this.nodeData) {
                return {
                    hasHighSimilarity: false,
                    hasLowSimilarity: false,
                    hasDataset: false
                };
            }

            const computed = this.nodeData.computed || {};
            const hasHighSimilarity = !!computed.high_similarity_matrix;
            const hasLowSimilarity = !!computed.low_similarity_matrix;
            const hasDataset = Array.isArray(this.nodeData.dataset) && this.nodeData.dataset.length > 0;

            return {
                hasHighSimilarity,
                hasLowSimilarity,
                hasDataset
            };
        },
        needsHighSimilarity() {
            // All these algorithms need high similarity matrix
            return true;
        },
        needsLowSimilarity() {
            // For gradient descent, low similarity is usually computed during the process
            return false;
        },
        canRunAlgorithm() {
            if (!this.nodeData) return false;

            if (this.needsHighSimilarity && !this.dataCheck.hasHighSimilarity) return false;
            if (this.needsLowSimilarity && !this.dataCheck.hasLowSimilarity) return false;
            if (!this.dataCheck.hasDataset) return false;

            return true;
        }
    },
    watch: {
        activeTab() {
            this.$nextTick(() => {
                this.renderFormulas();
            });
        },
        nodeData: {
            handler() {
                this.$nextTick(() => {
                    this.renderFormulas();
                });
            },
            deep: true
        }
    },
    mounted() {
        this.$nextTick(() => {
            this.renderFormulas();
        });
    },
    methods: {
        // 处理可视化类型切换
        handleVisualizationChange() {
            this.$nextTick(() => {
                this.updateVisualization();
            });
        },

        // 移动到上一个迭代步骤
        previousIteration() {
            if (this.iterationSlider > 0) {
                this.iterationSlider--;
                this.updateVisualization();
            }
        },

        // 移动到下一个迭代步骤
        nextIteration() {
            if (this.iterationSlider < this.iterationData.length - 1) {
                this.iterationSlider++;
                this.updateVisualization();
            }
        },

        renderFormulas() {
            if (!this.nodeData) return;

            const tabs = ['tsne', 'sne', 'umap'];

            tabs.forEach(tab => {
                const costEl = this.$refs[`${tab}_cost_formula`];
                const gradientEl = this.$refs[`${tab}_gradient_formula`];

                if (costEl) {
                    katex.render(this.formulas[tab].cost, costEl, {
                        throwOnError: false,
                        displayMode: true
                    });
                }

                if (gradientEl) {
                    katex.render(this.formulas[tab].gradient, gradientEl, {
                        throwOnError: false,
                        displayMode: true
                    });
                }
            });

            // 渲染梯度下降和动量公式
            const gradientDescentEl = this.$refs.gradient_descent_formula;
            const momentumEl = this.$refs.momentum_formula;

            if (gradientDescentEl) {
                katex.render(this.formulas.optimization.gradient_descent, gradientDescentEl, {
                    throwOnError: false,
                    displayMode: true
                });
            }

            if (momentumEl) {
                katex.render(this.formulas.optimization.momentum, momentumEl, {
                    throwOnError: false,
                    displayMode: true
                });
            }
        },
        handleTabClick() {
            // Reset iteration data when algorithm changes
            this.iterationData = [];
            this.iterationSlider = 0;

            if (this.chart) {
                this.chart.dispose();
                this.chart = null;
            }
        },
        formatIterationTooltip(value) {
            // 防御性检查，确保值有效且存在相应的迭代数据
            if (value === null || value === undefined ||
                !this.iterationData ||
                !this.iterationData[value] ||
                this.iterationData[value].iteration === undefined) {
                return '迭代数据不可用';
            }
            return `迭代 ${this.iterationData[value].iteration}`;
        },
        async runGradientDescent() {
            if (!this.canRunAlgorithm) return;

            this.isLoading = true;

            try {
                // Prepare data for the backend
                const requestData = {
                    algorithm: this.activeTab,
                    parameters: this.parameters,
                    node: this.nodeData
                };

                // Call the backend API
                const response = await axios.post('http://localhost:5000/api/gradient_descent', requestData);

                // Handle the response
                if (response.data && response.data.success) {
                    this.iterationData = response.data.iterations || [];
                    this.iterationSlider = this.iterationData.length - 1;

                    // Emit the updated node data to parent component
                    this.$emit('gradient-updated', response.data.node);

                    // Update visualization
                    this.$nextTick(() => {
                        this.updateVisualization();
                    });

                    this.$message.success('梯度下降计算完成');
                } else {
                    this.$message.error(response.data.message || '计算失败');
                }
            } catch (error) {
                console.error('Gradient descent error:', error);
                this.$message.error('计算过程中发生错误');
            } finally {
                this.isLoading = false;
            }
        },
        updateVisualization() {
            if (!this.iterationData.length) return;

            if (this.chart) {
                this.chart.dispose();
            }

            this.chart = echarts.init(this.$refs.visualization);

            if (this.visualizationMode === 'scatter') {
                this.renderScatterPlot();
            } else if (this.visualizationMode === 'cost') {
                this.renderCostCurve();
            } else if (this.visualizationMode === 'gradient') {
                this.renderGradientNormCurve();
            }
        },
        renderScatterPlot() {
            if (!this.iterationData.length) return;

            const currentIteration = this.iterationData[this.iterationSlider];
            if (!currentIteration || !currentIteration.embedding) return;

            // 获取标签数据（如果存在）
            const targetLabels = this.nodeData.target || [];
            const hasLabels = targetLabels.length > 0;

            // 准备散点图数据
            const data = currentIteration.embedding.map((point, index) => {
                // 如果有标签数据，则使用标签作为类别
                const category = hasLabels ? targetLabels[index] : 0;
                return {
                    value: point,
                    name: `点 ${index + 1}`,
                    category: category,
                    // 存储索引用于获取类别名称
                    dataIndex: index
                };
            });

            // 确定需要多少种不同的颜色
            const uniqueCategories = hasLabels ?
                [...new Set(targetLabels)].sort((a, b) => a - b) : [0];

            // 获取类别名称（如果有）
            const categoryNames = this.nodeData.target_names || uniqueCategories.map(c => `类别 ${c}`);

            // 为每个类别创建一个系列
            const series = uniqueCategories.map(category => {
                const categoryData = data.filter(item => item.category === category);
                return {
                    name: categoryNames[uniqueCategories.indexOf(category)],
                    type: 'scatter',
                    data: categoryData,
                    symbolSize: 10
                };
            });

            // 如果没有标签数据，则使用单一系列
            if (!hasLabels) {
                series[0].name = '数据点';
            }

            const option = {
                // 启用大数据量优化
                large: true,
                largeThreshold: 500,
                // 关闭动画
                animation: false,
                title: {
                    text: `${this.getAlgorithmName()} - 迭代 ${currentIteration.iteration}`,
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function (params) {
                        const categoryName = hasLabels ?
                            categoryNames[uniqueCategories.indexOf(params.data.category)] : '未分类';
                        return `${params.name}<br/>类别: ${categoryName}<br/>坐标: (${params.value[0].toFixed(2)}, ${params.value[1].toFixed(2)})`;
                    }
                },
                legend: {
                    data: hasLabels ? categoryNames : ['数据点'],
                    orient: 'vertical',
                    right: 10,
                    top: 'center'
                },
                xAxis: {
                    type: 'value',
                    scale: true,
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                yAxis: {
                    type: 'value',
                    scale: true,
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                series: series
            };

            this.chart.setOption(option);
        },
        renderCostCurve() {
            if (!this.iterationData.length) return;

            const iterations = this.iterationData.map(data => data.iteration);
            const costs = this.iterationData.map(data => data.cost);

            const option = {
                title: {
                    text: `${this.getAlgorithmName()} - 成本函数曲线`,
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        return `迭代: ${params[0].value[0]}<br/>成本: ${params[0].value[1].toFixed(4)}`;
                    }
                },
                xAxis: {
                    type: 'category',
                    data: iterations,
                    name: '迭代次数'
                },
                yAxis: {
                    type: 'value',
                    name: '成本值',
                    scale: true
                },
                series: [{
                    data: iterations.map((iter, index) => [iter, costs[index]]),
                    type: 'line',
                    smooth: true,
                    lineStyle: {
                        width: 2,
                        color: '#5470c6'
                    },
                    itemStyle: {
                        color: '#5470c6'
                    }
                }]
            };

            this.chart.setOption(option);
        },
        renderGradientNormCurve() {
            if (!this.iterationData.length) return;

            const iterations = this.iterationData.map(data => data.iteration);
            const gradientNorms = this.iterationData.map(data => data.gradient_norm || 0);

            const option = {
                title: {
                    text: `${this.getAlgorithmName()} - 梯度范数曲线`,
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        return `迭代: ${params[0].value[0]}<br/>梯度范数: ${params[0].value[1].toFixed(4)}`;
                    }
                },
                xAxis: {
                    type: 'category',
                    data: iterations,
                    name: '迭代次数'
                },
                yAxis: {
                    type: 'value',
                    name: '梯度范数',
                    scale: true
                },
                series: [{
                    data: iterations.map((iter, index) => [iter, gradientNorms[index]]),
                    type: 'line',
                    smooth: true,
                    lineStyle: {
                        width: 2,
                        color: '#91cc75'
                    },
                    itemStyle: {
                        color: '#91cc75'
                    }
                }]
            };

            this.chart.setOption(option);
        },
        getAlgorithmName() {
            const names = {
                'tsne': 't-SNE',
                'sne': 'SNE',
                'umap': 'UMAP'
            };

            return names[this.activeTab] || this.activeTab.toUpperCase();
        }
    }
};
</script>

<style scoped>
.gradient-descent-container {
    padding: 20px;
}

.algorithm-card,
.parameter-card,
.visualization-card {
    margin-bottom: 20px;
}

.formula-card,
.optimization-formula-card {
    padding: 10px;
    border-radius: 4px;
    background-color: #f9f9f9;
    margin-bottom: 15px;
}

.formula {
    margin: 15px 0;
    overflow-x: auto;
}

.description {
    color: #606266;
    font-size: 14px;
    margin-top: 10px;
}

.description ul {
    padding-left: 20px;
    margin-top: 10px;
}

.description li {
    margin-bottom: 8px;
}

.hint {
    font-size: 12px;
    color: #909399;
    margin-top: 5px;
}

.form-actions {
    margin-top: 20px;
    text-align: right;
}

.visualization-container {
    width: 100%;
    height: 400px;
}

.data-check {
    margin: 15px 0;
}

.slider-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.slider-label {
    margin-right: 10px;
    min-width: 80px;
    font-weight: bold;
}

.slider-wrapper {
    width: 100%;
    padding: 0 15px;
    margin-bottom: 20px;
}

.iteration-display {
    min-width: 100px;
    text-align: center;
    font-weight: bold;
    margin: 0 10px;
}

.iteration-controls {
    margin: 15px 0;
}

.navigation-buttons {
    display: flex;
    align-items: center;
    margin-left: auto;
}
</style>