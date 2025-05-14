<template>
    <div class="node-detail-container" v-if="nodeData">
        <el-card class="node-info-card">
            <div slot="header" class="card-header">
                <span>节点基本信息</span>
            </div>
            <div class="info-item">
                <span class="label">节点ID：</span>
                <span class="value">{{ nodeData.id }}</span>
            </div>
            <div class="info-item">
                <span class="label">操作类型：</span>
                <span class="value">{{ nodeData.operation }}</span>
            </div>
            <div class="info-item">
                <span class="label">选中状态：</span>
                <el-tag size="small" :type="nodeData.selected ? 'success' : 'info'">
                    {{ nodeData.selected ? '已选中' : '未选中' }}
                </el-tag>
            </div>
        </el-card>

        <el-card class="node-info-card" v-if="nodeData.parameters && Object.keys(nodeData.parameters).length > 0">
            <div slot="header" class="card-header">
                <span>参数信息</span>
            </div>
            <el-descriptions :column="1" border>
                <el-descriptions-item v-for="(value, key) in nodeData.parameters" :key="key" :label="key">
                    {{ value }}
                </el-descriptions-item>
            </el-descriptions>
        </el-card>

        <el-card class="node-info-card" v-if="nodeData.feature_names && Object.keys(nodeData.feature_names).length > 0">
            <div slot="header" class="card-header">
                <span>特征信息</span>
            </div>
            <el-descriptions :column="1" border>
                <el-descriptions-item v-for="(value, key) in nodeData.feature_names" :key="key" :label="key">
                    {{ value }}
                </el-descriptions-item>
            </el-descriptions>
        </el-card>

        <el-card class="node-info-card" v-if="hasComputedData">
            <div slot="header" class="card-header">
                <span>计算结果</span>
            </div>

            <!-- 特征值展示 -->
            <div v-if="nodeData.computed.eigenvalues" class="computed-section">
                <h3>特征值</h3>
                <div class="eigenvalues-container">
                    <div v-for="(value, index) in nodeData.computed.eigenvalues" :key="'eigen-' + index"
                        class="eigenvalue-item">
                        <el-tooltip :content="`λ${index + 1} = ${value}`" placement="top">
                            <div class="eigenvalue-bar" :style="{ width: getEigenValueWidth(value) + '%' }">
                                <span>λ{{ index + 1 }}: {{ value.toFixed(4) }}</span>
                            </div>
                        </el-tooltip>
                    </div>
                </div>
            </div>

            <!-- 特征向量展示 -->
            <div v-if="nodeData.computed.eigenvectors" class="computed-section">
                <h3>特征向量</h3>
                <el-table :data="formatEigenvectors" border stripe style="width: 100%">
                    <el-table-column label="向量" width="80">
                        <template slot-scope="scope">
                            向量 {{ scope.$index + 1 }}
                        </template>
                    </el-table-column>
                    <el-table-column v-for="(_, colIndex) in nodeData.computed.eigenvectors[0]" :key="'col-' + colIndex"
                        :label="`维度 ${colIndex + 1}`">
                        <template slot-scope="scope">
                            {{ scope.row[colIndex].toFixed(4) }}
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <!-- 协方差矩阵展示 -->
            <div v-if="nodeData.computed.covariance" class="computed-section">
                <h3>协方差矩阵</h3>
                <div class="matrix-controls">
                    <el-checkbox v-model="showCovarianceValues">显示具体数值</el-checkbox>
                    <el-select v-model="covarianceDisplayLimit" placeholder="显示范围" size="small"
                        style="width: 120px; margin-left: 10px;">
                        <el-option label="全部" :value="0"></el-option>
                        <el-option label="前10行/列" :value="10"></el-option>
                        <el-option label="前20行/列" :value="20"></el-option>
                        <el-option label="前50行/列" :value="50"></el-option>
                        <el-option label="前100行/列" :value="100"></el-option>
                    </el-select>
                </div>
                <div class="matrix-visualization">
                    <div class="heatmap-container">
                        <div v-for="(row, rowIndex) in limitedCovarianceMatrix" :key="'cov-row-' + rowIndex"
                            class="heatmap-row">
                            <div v-for="(value, colIndex) in row" :key="'cov-cell-' + rowIndex + '-' + colIndex"
                                class="heatmap-cell"
                                :style="getHeatMapStyle(value, getMaxAbsValueInMatrix(limitedCovarianceMatrix))"
                                :title="`(${rowIndex}, ${colIndex}): ${value}`">
                                <span v-if="showCovarianceValues">{{ value.toFixed(1) }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="matrix-info" v-if="isCovarianceTruncated">
                        <el-alert title="注意：矩阵过大，仅显示部分数据" type="info" :closable="false" size="small"></el-alert>
                    </div>
                    <div class="color-scale">
                        <div class="scale-label">低</div>
                        <div class="scale-gradient"></div>
                        <div class="scale-label">高</div>
                    </div>
                </div>
            </div>

            <!-- 相似度矩阵展示 -->
            <div v-if="nodeData.computed.high_similarity_matrix" class="computed-section">
                <h3>相似度矩阵</h3>
                <div class="matrix-controls">
                    <el-checkbox v-model="showSimilarityValues">显示具体数值</el-checkbox>
                    <el-select v-model="similarityDisplayLimit" placeholder="显示范围" size="small"
                        style="width: 120px; margin-left: 10px;">
                        <el-option label="全部" :value="0"></el-option>
                        <el-option label="前10行/列" :value="10"></el-option>
                        <el-option label="前20行/列" :value="20"></el-option>
                        <el-option label="前50行/列" :value="50"></el-option>
                        <el-option label="前100行/列" :value="100"></el-option>
                    </el-select>
                </div>
                <div class="matrix-visualization">
                    <div class="heatmap-container">
                        <div v-for="(row, rowIndex) in limitedSimilarityMatrix" :key="'sim-row-' + rowIndex"
                            class="heatmap-row">
                            <div v-for="(value, colIndex) in row" :key="'sim-cell-' + rowIndex + '-' + colIndex"
                                class="heatmap-cell" :style="getHeatMapStyle(value, 1, true)"
                                :title="`(${rowIndex}, ${colIndex}): ${value}`">
                                <span v-if="showSimilarityValues">{{ value.toFixed(1) }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="matrix-info" v-if="isSimilarityTruncated">
                        <el-alert title="注意：矩阵过大，仅显示部分数据" type="info" :closable="false" size="small"></el-alert>
                    </div>
                    <div class="color-scale">
                        <div class="scale-label">0</div>
                        <div class="scale-gradient similarity-gradient"></div>
                        <div class="scale-label">1</div>
                    </div>
                </div>
            </div>

            <!-- 方差展示 -->
            <div v-if="nodeData.computed.variance" class="computed-section">
                <h3>方差</h3>
                <div class="variance-container">
                    <el-progress v-for="(value, index) in nodeData.computed.variance" :key="'var-' + index"
                        :percentage="Math.min(value * 20, 100)" :format="() => value.toFixed(4)" :stroke-width="20"
                        :color="getVarianceColor(index)">
                        <span slot="prefix" class="variance-label">维度 {{ index + 1 }}:</span>
                    </el-progress>
                </div>
            </div>

            <!-- 累计方差解释率展示 -->
            <div v-if="nodeData.computed.explained_variance_ratio" class="computed-section">
                <h3>累计方差解释率</h3>
                <div class="explained-variance-chart">
                    <el-progress v-for="(value, index) in getCumulativeExplainedVariance()" :key="'exp-var-' + index"
                        :percentage="value * 100" :format="() => (value * 100).toFixed(2) + '%'" :stroke-width="20"
                        :color="getVarianceColor(index, true)">
                        <span slot="prefix" class="variance-label">前 {{ index + 1 }} 个维度:</span>
                    </el-progress>
                </div>
            </div>

            <!-- 其他任何计算结果的展示 -->
            <div v-if="hasOtherComputedData" class="computed-section">
                <h3>其他计算结果</h3>
                <el-descriptions :column="1" border>
                    <el-descriptions-item v-for="(value, key) in otherComputedData" :key="key"
                        :label="formatLabel(key)">
                        <span v-if="isNumeric(value)">{{ Number(value).toFixed(4) }}</span>
                        <span v-else>{{ value }}</span>
                    </el-descriptions-item>
                </el-descriptions>
            </div>
        </el-card>

        <el-card class="node-info-card" v-if="nodeData.children && nodeData.children.length > 0">
            <div slot="header" class="card-header">
                <span>子节点信息</span>
            </div>
            <div class="children-info">
                <el-tag v-for="child in nodeData.children" :key="child.id" type="info" effect="plain" size="medium"
                    class="child-tag">
                    ID: {{ child.id }} - {{ child.operation || '未定义操作' }}
                </el-tag>
            </div>
        </el-card>
    </div>
    <div v-else class="empty-state">
        <el-empty description="暂无节点数据"></el-empty>
    </div>
</template>

<script>
export default {
    name: 'NodeDetail',
    props: {
        nodeData: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            // 矩阵展示控制
            showCovarianceValues: false,
            showSimilarityValues: false,
            covarianceDisplayLimit: 20,
            similarityDisplayLimit: 20,
        }
    },
    computed: {
        hasComputedData() {
            return this.nodeData && this.nodeData.computed && Object.keys(this.nodeData.computed).length > 0;
        },
        hasOtherComputedData() {
            if (!this.hasComputedData) return false;

            // 排除已经特殊处理的计算结果
            const specialKeys = ['eigenvalues', 'eigenvectors', 'covariance', 'high_similarity_matrix', 'low_similarity_matrix', 'variance', 'explained_variance_ratio'];
            return Object.keys(this.nodeData.computed).some(key => !specialKeys.includes(key));
        },
        otherComputedData() {
            if (!this.hasComputedData) return {};

            const specialKeys = ['eigenvalues', 'eigenvectors', 'covariance', 'high_similarity_matrix', 'low_similarity_matrix', 'variance', 'explained_variance_ratio'];
            const result = {};

            Object.keys(this.nodeData.computed).forEach(key => {
                if (!specialKeys.includes(key)) {
                    result[key] = this.nodeData.computed[key];
                }
            });

            return result;
        },
        formatEigenvectors() {
            if (!this.nodeData?.computed?.eigenvectors) return [];
            return this.nodeData.computed.eigenvectors.map(vector => [...vector]);
        },
        // 限制矩阵显示大小
        limitedCovarianceMatrix() {
            if (!this.nodeData?.computed?.covariance) return [];

            const matrix = this.nodeData.computed.covariance;
            if (this.covarianceDisplayLimit === 0 || matrix.length <= this.covarianceDisplayLimit) {
                return matrix;
            }

            // 截取前N行和N列
            return matrix.slice(0, this.covarianceDisplayLimit).map(row => row.slice(0, this.covarianceDisplayLimit));
        },
        limitedSimilarityMatrix() {
            if (!this.nodeData?.computed?.high_similarity_matrix) return [];

            const matrix = this.nodeData.computed.high_similarity_matrix;
            if (this.similarityDisplayLimit === 0 || matrix.length <= this.similarityDisplayLimit) {
                return matrix;
            }

            // 截取前N行和N列
            return matrix.slice(0, this.similarityDisplayLimit).map(row => row.slice(0, this.similarityDisplayLimit));
        },
        isCovarianceTruncated() {
            return this.nodeData?.computed?.covariance &&
                this.covarianceDisplayLimit > 0 &&
                this.nodeData.computed.covariance.length > this.covarianceDisplayLimit;
        },
        isSimilarityTruncated() {
            return this.nodeData?.computed?.high_similarity_matrix &&
                this.similarityDisplayLimit > 0 &&
                this.nodeData.computed.high_similarity_matrix.length > this.similarityDisplayLimit;
        }
    },
    methods: {
        formatLabel(key) {
            // 将下划线转换为空格，并将首字母大写
            return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
        },
        isNumeric(value) {
            return !isNaN(parseFloat(value)) && isFinite(value);
        },
        getMaxAbsValueInMatrix(matrix) {
            let max = 0;
            for (const row of matrix) {
                for (const value of row) {
                    const absValue = Math.abs(value);
                    if (absValue > max) {
                        max = absValue;
                    }
                }
            }
            return max;
        },
        getHeatMapStyle(value, maxValue, isNormalized = false) {
            let intensity;

            if (isNormalized) {
                // 对于相似度矩阵 (0-1)
                intensity = value;
            } else {
                // 对于协方差矩阵等
                const absValue = Math.abs(value);
                intensity = maxValue === 0 ? 0 : absValue / maxValue;
            }

            // 热图颜色
            let color;
            if (isNormalized) {
                // 相似度矩阵使用蓝色渐变
                const blueIntensity = Math.floor(255 * intensity);
                color = `rgb(${255 - blueIntensity}, ${255 - blueIntensity}, 255)`;
            } else if (value >= 0) {
                // 正值使用红色
                const redIntensity = Math.floor(200 * intensity) + 55;
                color = `rgb(${redIntensity}, ${Math.floor(55 + (200 - intensity * 200))}, ${Math.floor(55 + (100 - intensity * 100))})`;
            } else {
                // 负值使用蓝色
                const blueIntensity = Math.floor(200 * intensity) + 55;
                color = `rgb(${Math.floor(55 + (100 - intensity * 100))}, ${Math.floor(55 + (100 - intensity * 100))}, ${blueIntensity})`;
            }

            return {
                backgroundColor: color,
                color: intensity > 0.7 ? '#ffffff' : '#000000'
            };
        },
        getEigenValueWidth(value) {
            if (!this.nodeData?.computed?.eigenvalues) return 0;
            const maxEigenvalue = Math.max(...this.nodeData.computed.eigenvalues);
            return maxEigenvalue === 0 ? 0 : (value / maxEigenvalue) * 100;
        },
        getVarianceColor(index, isExplained = false) {
            // 为不同维度使用不同颜色
            const colors = [
                '#409EFF', // 主要蓝色
                '#67C23A', // 成功绿色
                '#E6A23C', // 警告黄色
                '#F56C6C', // 危险红色
                '#909399', // 信息灰色
            ];

            // 为累计方差使用渐变色
            if (isExplained) {
                return {
                    '0%': '#409EFF',
                    '100%': '#67C23A'
                };
            }

            return colors[index % colors.length];
        },
        getCumulativeExplainedVariance() {
            if (!this.nodeData?.computed?.explained_variance_ratio) return [];

            const result = [];
            let sum = 0;

            for (const value of this.nodeData.computed.explained_variance_ratio) {
                sum += value;
                result.push(sum);
            }

            return result;
        }
    }
}
</script>

<style scoped>
.node-detail-container {
    height: 100%;
    padding: 15px;
    max-width: 100%;
    overflow-y: auto;
}

.node-info-card {
    margin-bottom: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
}

.info-item {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
}

.label {
    font-weight: bold;
    margin-right: 8px;
    min-width: 80px;
}

.computed-section {
    margin-bottom: 25px;
}

.computed-section h3 {
    font-size: 16px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #EBEEF5;
    color: #409EFF;
}

.matrix-visualization {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 15px;
}

.matrix-controls {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.matrix-info {
    margin: 10px 0;
    width: 100%;
}

.heatmap-container {
    display: flex;
    flex-direction: column;
    border: 1px solid #EBEEF5;
    margin-bottom: 10px;
    max-height: 400px;
    max-width: 100%;
    overflow: auto;
}

.heatmap-row {
    display: flex;
}

.heatmap-cell {
    width: 25px;
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
}

.heatmap-cell:hover {
    transform: scale(1.05);
    z-index: 1;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
}

.color-scale {
    display: flex;
    align-items: center;
    margin-top: 5px;
}

.scale-label {
    font-size: 12px;
    color: #606266;
    margin: 0 5px;
}

.scale-gradient {
    width: 200px;
    height: 10px;
    background: linear-gradient(to right, #F56C6C, #E6A23C, #67C23A);
}

.similarity-gradient {
    background: linear-gradient(to right, #FFFFFF, #409EFF);
}

.eigenvalues-container {
    margin-bottom: 15px;
}

.eigenvalue-item {
    margin-bottom: 8px;
}

.eigenvalue-bar {
    background-color: #409EFF;
    color: white;
    height: 30px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    border-radius: 4px;
    min-width: 60px;
    transition: width 0.3s;
}

.variance-container {
    margin-top: 15px;
}

.variance-label {
    margin-right: 10px;
    min-width: 80px;
    display: inline-block;
    text-align: right;
}

.explained-variance-chart {
    margin-top: 15px;
}

.children-info {
    display: flex;
    flex-wrap: wrap;
}

.child-tag {
    margin: 5px;
}

.empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
}
</style>