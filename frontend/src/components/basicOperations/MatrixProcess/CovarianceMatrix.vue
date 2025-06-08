<!-- Vue 2 Component for Enhanced Covariance Matrix Calculation -->
<template>
    <div class="covariance-matrix-container">
        <div class="header-section">
            <h3>协方差矩阵计算与可视化</h3>
            <p class="intro-text">协方差矩阵展示了数据特征之间的相关性强度。正值表示正相关，负值表示负相关，接近零表示无相关。</p>
        </div>

        <div v-if="loading" class="loading-indicator">
            <div class="spinner"></div>
            <span>计算中...</span>
        </div>

        <div v-if="error" class="error-message">
            <span>{{ error }}</span>
        </div>

        <div class="main-content">
            <div class="action-panel">
                <button class="calculate-btn" @click="calculateCovarianceMatrix" :disabled="!hasValidData()">
                    <span class="btn-icon">📊</span>
                    计算协方差矩阵
                </button>

                <div class="data-info" v-if="hasValidData()">
                    <div class="info-item">
                        <span class="info-label">特征数量:</span>
                        <span class="info-value">{{ getFeatureCount() }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">样本数量:</span>
                        <span class="info-value">{{ getSampleCount() }}</span>
                    </div>
                </div>
            </div>

            <div v-if="resultNode" class="result-section">
                <h4>计算结果</h4>

                <div class="visualization-container">
                    <div class="tabs">
                        <button :class="['tab-btn', { active: activeTab === 'matrix' }]" @click="activeTab = 'matrix'">
                            数值矩阵
                        </button>
                        <button :class="['tab-btn', { active: activeTab === 'heatmap' }]"
                            @click="activeTab = 'heatmap'">
                            热力图
                        </button>
                    </div>

                    <div class="tab-content">
                        <!-- 数值矩阵视图 -->
                        <div v-if="activeTab === 'matrix' && covarianceMatrix" class="matrix-container">
                            <table class="covariance-matrix">
                                <thead>
                                    <tr>
                                        <th class="corner-header">特征</th>
                                        <th v-for="(col, colIndex) in matrixColumns" :key="colIndex">{{
                                            nodeData["feature_names"][col] }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(row, rowIndex) in matrixColumns" :key="rowIndex">
                                        <td class="row-header">{{ nodeData["feature_names"][row] }}</td>
                                        <td v-for="(col, colIndex) in matrixColumns" :key="colIndex"
                                            :class="getCellClass(covarianceMatrix[rowIndex][colIndex])">
                                            {{ formatValue(covarianceMatrix[rowIndex][colIndex]) }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <!-- 热力图视图 -->
                        <div v-if="activeTab === 'heatmap' && covarianceMatrix" class="heatmap-container">
                            <div class="heatmap">
                                <div class="heatmap-row" v-for="(row, rowIndex) in covarianceMatrix" :key="rowIndex">
                                    <div class="row-label">{{ nodeData["feature_names"][rowIndex] }}</div>
                                    <div v-for="(value, colIndex) in row" :key="colIndex" class="heatmap-cell"
                                        :style="getHeatmapStyle(value)"
                                        :title="`${matrixColumns[rowIndex]}-${matrixColumns[colIndex]}: ${formatValue(value)}`">
                                    </div>
                                </div>
                                <div class="column-labels">
                                    <div class="empty-label"></div>
                                    <div class="column-label" v-for="(col, colIndex) in matrixColumns" :key="colIndex">
                                        {{ nodeData["feature_names"][col] }}
                                    </div>
                                </div>
                            </div>

                            <div class="color-scale">
                                <div class="scale-gradient"></div>
                                <div class="scale-labels">
                                    <span>强负相关</span>
                                    <span>无相关</span>
                                    <span>强正相关</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="interpretation-guide">
                    <h5>解读指南</h5>
                    <ul>
                        <li><span class="positive">正值 (红色)</span>: 两个特征正相关，一个增加，另一个也倾向于增加</li>
                        <li><span class="negative">负值 (蓝色)</span>: 两个特征负相关，一个增加，另一个倾向于减少</li>
                        <li><span class="neutral">接近零 (白色)</span>: 两个特征几乎无相关性</li>
                        <li>对角线上的值表示特征与自身的协方差，也就是方差，始终为正值</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '@/utils/flaskAxios'

export default {
    name: 'CovarianceMatrix',

    props: {
        // 节点数据，由父组件传递
        nodeData: {
            type: Object,
            default: () => (null)
        },
    },

    data() {
        return {
            loading: false,
            error: null,
            resultNode: null,
            matrixColumns: [],
            activeTab: 'matrix',  // 默认显示矩阵视图
            maxCovValue: 0        // 用于热力图颜色缩放
        }
    },

    computed: {
        // 获取协方差矩阵结果
        covarianceMatrix() {
            if (this.resultNode &&
                this.resultNode.computed &&
                this.resultNode.computed.covariance_matrix) {
                return this.resultNode.computed.covariance_matrix;
            }
            return null;
        }
    },

    methods: {
        // 检查数据集是否有效
        hasValidData() {
            return this.nodeData &&
                this.nodeData.dataset &&
                Array.isArray(this.nodeData.dataset) &&
                this.nodeData.dataset.length > 0;
        },

        // 获取特征数量
        getFeatureCount() {
            if (this.hasValidData() && this.nodeData.dataset[0]) {
                // 假设第一行包含所有特征
                return Object.keys(this.nodeData.dataset[0]).length;
            }
            return 0;
        },

        // 获取样本数量
        getSampleCount() {
            if (this.hasValidData()) {
                return this.nodeData.dataset.length;
            }
            return 0;
        },

        // 调用后端API计算协方差矩阵
        calculateCovarianceMatrix() {
            if (!this.hasValidData()) {
                this.error = '没有有效的数据集';
                return;
            }

            this.loading = true;
            this.error = null;

            // 准备请求数据
            const requestData = {
                nodeData: this.nodeData
            };

            // 调用后端API
            axios.post(`/api/calculate-covariance`, requestData)
                .then(response => {
                    if (!response.success) {
                        console.log(`协方差API请求失败`);
                    }
                    this.resultNode = response.node;

                    // 提取矩阵的列名
                    if (this.covarianceMatrix) {
                        this.extractMatrixColumns();
                        this.calculateMaxValue();
                    }

                    // 通知父组件计算结果
                    this.$emit('calculation-complete', this.resultNode);
                })
                .catch(error => {
                    console.error('计算协方差矩阵时出错:', error);
                    this.error = `计算失败: ${error.message}`;
                })
                .finally(() => {
                    this.loading = false;
                });
        },

        // 提取矩阵的列名
        extractMatrixColumns() {
            if (this.resultNode &&
                this.resultNode.computed &&
                this.resultNode.computed.featureNames) {
                this.matrixColumns = this.resultNode.computed.featureNames;
            } else if (this.covarianceMatrix) {
                // 如果没有提供特征名，使用默认的列名
                this.matrixColumns = Array.from(
                    { length: this.covarianceMatrix.length },
                    (_, i) => `特征 ${i + 1}`
                );
            }
        },

        // 计算最大协方差值用于热力图颜色缩放
        calculateMaxValue() {
            if (!this.covarianceMatrix) return;

            let max = 0;
            for (let row of this.covarianceMatrix) {
                for (let value of row) {
                    const absValue = Math.abs(value);
                    if (absValue > max) max = absValue;
                }
            }
            this.maxCovValue = max;
        },

        // 格式化矩阵值，保留4位小数
        formatValue(value) {
            if (value === null || value === undefined) return 'N/A';

            // 处理数值，保留4位小数
            return Number.isFinite(value) ? value.toFixed(4) : value.toString();
        },

        // 获取单元格的CSS类
        getCellClass(value) {
            if (value === null || value === undefined) return 'cell-na';

            if (value > 0) {
                return value > 0.5 ? 'cell-strong-positive' : 'cell-positive';
            } else if (value < 0) {
                return value < -0.5 ? 'cell-strong-negative' : 'cell-negative';
            }
            return 'cell-neutral';
        },

        // 获取热力图单元格的样式
        getHeatmapStyle(value) {
            if (value === null || value === undefined) return { backgroundColor: '#f0f0f0' };

            // 将值归一化到 [-1, 1] 范围
            const normalizedValue = this.maxCovValue ? (value / this.maxCovValue) : 0;

            // 生成颜色 - 蓝色为负相关，红色为正相关，白色为无相关
            let color;
            if (normalizedValue > 0) {
                // 从白色到红色
                const intensity = Math.min(Math.round(normalizedValue * 255), 255);
                color = `rgb(255, ${255 - intensity}, ${255 - intensity})`;
            } else {
                // 从白色到蓝色
                const intensity = Math.min(Math.round(Math.abs(normalizedValue) * 255), 255);
                color = `rgb(${255 - intensity}, ${255 - intensity}, 255)`;
            }

            return {
                backgroundColor: color
            };
        }
    }
}
</script>

<style scoped>
.covariance-matrix-container {
    margin: 20px 0;
    padding: 20px;
    border-radius: 8px;
    background-color: #ffffff;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header-section {
    margin-bottom: 20px;
    border-bottom: 1px solid #eaeaea;
    padding-bottom: 15px;
}

.header-section h3 {
    margin: 0 0 10px 0;
    color: #333;
    font-size: 1.5rem;
}

.intro-text {
    color: #666;
    font-size: 0.9rem;
    line-height: 1.4;
}

.main-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.action-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    margin-bottom: 10px;
}

.calculate-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    background-color: #4285f4;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 2px 5px rgba(66, 133, 244, 0.3);
}

.calculate-btn:hover {
    background-color: #3367d6;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(66, 133, 244, 0.4);
}

.calculate-btn:active {
    transform: translateY(0);
    box-shadow: 0 1px 3px rgba(66, 133, 244, 0.4);
}

.calculate-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
    box-shadow: none;
}

.btn-icon {
    font-size: 1.1rem;
}

.data-info {
    display: flex;
    gap: 20px;
}

.info-item {
    display: flex;
    gap: 5px;
    align-items: center;
    background-color: #f5f8ff;
    padding: 6px 12px;
    border-radius: 4px;
}

.info-label {
    font-size: 0.85rem;
    color: #666;
}

.info-value {
    font-weight: 600;
    color: #333;
}

.loading-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 20px;
    justify-content: center;
    color: #666;
}

.spinner {
    width: 24px;
    height: 24px;
    border: 3px solid rgba(66, 133, 244, 0.3);
    border-radius: 50%;
    border-top-color: #4285f4;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.error-message {
    padding: 12px 15px;
    background-color: #ffebee;
    color: #c62828;
    border-radius: 6px;
    margin-bottom: 15px;
    font-size: 0.9rem;
}

.result-section {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #eaeaea;
}

.result-section h4 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #333;
    font-size: 1.2rem;
}

.visualization-container {
    margin-bottom: 20px;
}

.tabs {
    display: flex;
    gap: 2px;
    margin-bottom: 15px;
    border-bottom: 1px solid #ddd;
}

.tab-btn {
    padding: 8px 16px;
    background-color: #f0f0f0;
    border: none;
    cursor: pointer;
    font-size: 0.9rem;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    transition: all 0.2s;
}

.tab-btn:hover {
    background-color: #e0e0e0;
}

.tab-btn.active {
    background-color: #4285f4;
    color: white;
}

.tab-content {
    min-height: 300px;
}

/* 数值矩阵样式 */
.matrix-container {
    overflow-x: auto;
    margin-top: 10px;
}

.covariance-matrix {
    border-collapse: collapse;
    width: 100%;
    font-size: 0.9rem;
}

.covariance-matrix th,
.covariance-matrix td {
    border: 1px solid #e0e0e0;
    padding: 10px;
    text-align: right;
}

.covariance-matrix th {
    background-color: #f5f5f5;
    font-weight: 600;
    color: #555;
}

.corner-header {
    background-color: #eaeaea;
}

.row-header {
    background-color: #f5f5f5;
    font-weight: 600;
    text-align: left;
    color: #555;
}

/* 设置单元格颜色 */
.cell-strong-positive {
    background-color: rgba(255, 0, 0, 0.2);
    font-weight: 600;
    color: #c62828;
}

.cell-positive {
    background-color: rgba(255, 0, 0, 0.1);
    color: #ef5350;
}

.cell-neutral {
    background-color: rgba(0, 0, 0, 0.03);
    color: #757575;
}

.cell-negative {
    background-color: rgba(0, 0, 255, 0.1);
    color: #3f51b5;
}

.cell-strong-negative {
    background-color: rgba(0, 0, 255, 0.2);
    font-weight: 600;
    color: #1a237e;
}

.cell-na {
    background-color: #f0f0f0;
    color: #9e9e9e;
}

/* 热力图样式 */
.heatmap-container {
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.heatmap {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.heatmap-row {
    display: flex;
    align-items: center;
    height: 30px;
    margin: 2px 0;
}

.row-label {
    width: 100px;
    padding-right: 10px;
    text-align: right;
    font-size: 0.85rem;
    color: #555;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.heatmap-cell {
    width: 30px;
    height: 30px;
    margin: 0 2px;
    transition: transform 0.2s;
}

.heatmap-cell:hover {
    transform: scale(1.1);
    z-index: 1;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.column-labels {
    display: flex;
    margin-top: 5px;
}

.empty-label {
    width: 100px;
}

.column-label {
    width: 30px;
    margin: 0 2px;
    text-align: center;
    font-size: 0.8rem;
    color: #555;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    transform: rotate(-45deg);
    transform-origin: top left;
    position: relative;
    left: 15px;
    top: 10px;
}

.color-scale {
    margin-top: 20px;
    padding: 10px;
    border-radius: 4px;
    background-color: #f5f5f5;
}

.scale-gradient {
    height: 20px;
    background: linear-gradient(to right, rgb(0, 0, 255), rgb(255, 255, 255), rgb(255, 0, 0));
    border-radius: 2px;
}

.scale-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 5px;
    font-size: 0.8rem;
    color: #666;
}

/* 解释指南样式 */
.interpretation-guide {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f8ff;
    border-radius: 6px;
    border-left: 4px solid #4285f4;
}

.interpretation-guide h5 {
    margin-top: 0;
    margin-bottom: 10px;
    color: #333;
    font-size: 1rem;
}

.interpretation-guide ul {
    margin: 0;
    padding-left: 20px;
}

.interpretation-guide li {
    margin-bottom: 5px;
    font-size: 0.9rem;
    color: #555;
}

.positive {
    color: #c62828;
    font-weight: 500;
}

.negative {
    color: #1a237e;
    font-weight: 500;
}

.neutral {
    color: #757575;
    font-weight: 500;
}

@media (max-width: 768px) {
    .action-panel {
        flex-direction: column;
        align-items: flex-start;
    }

    .data-info {
        flex-direction: column;
        gap: 10px;
    }
}
</style>