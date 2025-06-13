<!-- LDAMatrixCalculator.vue -->
<template>
    <div class="lda-matrix-calculator">
        <el-card class="main-card" shadow="hover">
            <div slot="header" class="header">
                <h2>线性判别分析 (LDA) 矩阵计算</h2>
            </div>

            <div v-if="!isDataAvailable" class="no-data">
                <el-alert title="数据不足" type="warning" description="请确保提供了有效的数据集，包含目标变量和特征。" show-icon :closable="false">
                </el-alert>
            </div>

            <div v-else class="calculator-content">
                <!-- 矩阵选择部分 -->
                <el-tabs v-model="activeTab" type="border-card">
                    <!-- 类内散度矩阵选项卡 -->
                    <el-tab-pane label="类内散度矩阵" name="withinClass">
                        <el-card class="formula-card">
                            <div class="formula-header">类内散度矩阵 (Within-Class Scatter Matrix)</div>
                            <div class="formula" ref="withinClassFormula"></div>

                            <div class="formula-description" v-html="renderedHtml1"></div>
                        </el-card>

                        <el-form :model="withinClassParams" label-width="100px" class="params-form">
                            <el-form-item label="正则化参数">
                                <el-tooltip content="添加小的正则化参数可以提高矩阵的稳定性" placement="top">
                                    <el-slider v-model="withinClassParams.regularization" :step="0.01" :min="0" :max="1"
                                        show-input></el-slider>
                                </el-tooltip>
                            </el-form-item>

                            <el-form-item>
                                <el-button type="primary" @click="calculateMatrix('within')" :loading="calculating">
                                    计算类内散度矩阵
                                </el-button>
                            </el-form-item>
                        </el-form>
                    </el-tab-pane>

                    <!-- 类间散度矩阵选项卡 -->
                    <el-tab-pane label="类间散度矩阵" name="betweenClass">
                        <el-card class="formula-card">
                            <div class="formula-header">类间散度矩阵 (Between-Class Scatter Matrix)</div>
                            <div class="formula" ref="betweenClassFormula"></div>

                            <div class="formula-description" v-html="renderedHtml2"></div>
                        </el-card>

                        <el-form :model="betweenClassParams" label-width="100px" class="params-form">
                            <el-form-item label="类别权重">
                                <el-radio-group v-model="betweenClassParams.weightType">
                                    <el-radio label="equal">均等权重</el-radio>
                                    <el-radio label="proportional">按类别比例</el-radio>
                                </el-radio-group>
                            </el-form-item>

                            <el-form-item>
                                <el-button type="primary" @click="calculateMatrix('between')" :loading="calculating">
                                    计算类间散度矩阵
                                </el-button>
                            </el-form-item>
                        </el-form>
                    </el-tab-pane>
                </el-tabs>

                <!-- 数据信息显示部分 -->
                <el-card class="data-info-card" shadow="hover">
                    <div slot="header" class="data-info-header">
                        <span>数据集信息</span>
                    </div>
                    <div class="data-info-content">
                        <el-descriptions :column="2" border>
                            <el-descriptions-item label="样本数量">{{ datasetInfo.sampleCount }}</el-descriptions-item>
                            <el-descriptions-item label="特征数量">{{ datasetInfo.featureCount }}</el-descriptions-item>
                            <el-descriptions-item label="类别数量">{{ datasetInfo.classCount }}</el-descriptions-item>
                            <el-descriptions-item label="特征名称">
                                <el-tag v-for="(feature, index) in featureList.slice(0, 3)" :key="index" size="small"
                                    style="margin-right: 5px">
                                    {{ feature }}
                                </el-tag>
                                <el-tag v-if="featureList.length > 3" size="small" type="info">+{{ featureList.length -
                                    3 }}</el-tag>
                            </el-descriptions-item>
                        </el-descriptions>
                    </div>
                </el-card>

                <!-- 计算结果显示部分 -->
                <el-card v-if="result" class="result-card" shadow="hover">
                    <div slot="header" class="result-header">
                        <span>计算结果</span>
                        <el-button size="mini" type="text" @click="clearResult">清除</el-button>
                    </div>
                    <div class="result-content">
                        <h4>{{ result.type === 'within' ? '类内散度矩阵' : '类间散度矩阵' }}</h4>
                        <div class="matrix-display">
                            <el-table :data="matrixToTableData(result.matrix)" border style="width: 100%"
                                :max-height="300" size="mini">
                                <el-table-column v-for="(col, index) in matrixColumns" :key="index" :prop="col.prop"
                                    :label="col.label" width="80">
                                </el-table-column>
                            </el-table>
                        </div>
                        <div class="matrix-stats">
                            <p><strong>矩阵秩:</strong> {{ result.stats.rank }}</p>
                            <p><strong>行列式值:</strong> {{ result.stats.determinant.toExponential(4) }}</p>
                            <p><strong>特征值:</strong>
                                <template v-for="(val, index) in result.stats.eigenvalues.slice(0, 3)">
                                    <!-- 添加 :key 到内部实际渲染的元素 -->
                                    <span :key="index">
                                        {{ val.toExponential(4) }}
                                        <span v-if="index < Math.min(2, result.stats.eigenvalues.length - 1)">, </span>
                                    </span>
                                </template>
                                <span v-if="result.stats.eigenvalues.length > 3">...</span>
                            </p>
                        </div>
                    </div>
                </el-card>
            </div>
        </el-card>
    </div>
</template>

<script>
import katex from 'katex';
import 'katex/dist/katex.min.css';
import axios from '@/utils/calculatorAxios';

export default {
    name: 'LDAMatrixCalculator',
    props: {
        nodeData: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            activeTab: 'withinClass',
            calculating: false,
            withinClassParams: {
                regularization: 0.01
            },
            betweenClassParams: {
                weightType: 'proportional'
            },
            result: null,
            matrixColumns: [],
            rawHtml1: `
        <p>类内散度矩阵表示每个类内的样本散布情况，它是各个类内散度矩阵的和。其中：</p>
        <ul>
            <li>\\(S_W\\) 是类内散度矩阵</li>
            <li>\\(S_i\\) 是第i个类的散度矩阵</li>
            <li>\\(x\\) 是样本向量</li>
            <li>\\(\\mu_i\\) 是第i个类的均值向量</li>
            <li>\\(c\\) 是类别总数</li>
        </ul>`,
            rawHtml2: `
        <p>类间散度矩阵表示各个类别之间的分散程度，它是各个类的均值与总体均值之差的加权和。其中：</p>
        <ul>
            <li>\\(S_B\\) 是类间散度矩阵</li>
            <li>\\(n_i\\) 是第i个类的样本数</li>
            <li>\\(\\mu_i\\) 是第i个类的均值向量</li>
            <li>\\(\\mu\\) 是所有样本的均值向量</li>
            <li>\\(c\\) 是类别总数</li>
        </ul>`
        };
    },
    computed: {
        renderedHtml1() {
            // 简单解析行内公式 \( ... \) -> 用 KaTeX 渲染
            return this.rawHtml1.replace(/\\\((.+?)\\\)/g, (_, expr) =>
                katex.renderToString(expr, { throwOnError: false })
            );
        },
        renderedHtml2() {
            // 简单解析行内公式 \( ... \) -> 用 KaTeX 渲染
            return this.rawHtml2.replace(/\\\((.+?)\\\)/g, (_, expr) =>
                katex.renderToString(expr, { throwOnError: false })
            );
        },
        isDataAvailable() {
            return this.nodeData &&
                this.nodeData.dataset &&
                this.nodeData.dataset.length > 0 &&
                this.nodeData.feature_names &&
                this.nodeData.feature_names.length > 0 &&
                this.nodeData.target &&
                this.nodeData.target.length > 0;
        },
        datasetInfo() {
            if (!this.isDataAvailable) {
                return {
                    sampleCount: 0,
                    featureCount: 0,
                    classCount: 0
                };
            }

            // 计算类别数量（唯一的目标值数量）
            const uniqueClasses = [...new Set(this.nodeData.target)];

            return {
                sampleCount: this.nodeData.dataset.length,
                featureCount: this.nodeData.feature_names.length,
                classCount: uniqueClasses.length
            };
        },
        featureList() {
            return this.isDataAvailable ? this.nodeData.feature_names : [];
        }
    },
    mounted() {
        this.renderFormulas();
    },
    watch: {
        nodeData: {
            handler() {
                this.clearResult();
                this.$nextTick(() => {
                    this.renderFormulas();
                });
            },
            deep: true
        }
    },
    methods: {
        renderFormulas() {

            // 渲染类内散度矩阵公式
            if (this.$refs.withinClassFormula) {
                katex.render(
                    '\\Large S_W = \\sum_{i=1}^{c} S_i = \\sum_{i=1}^{c} \\sum_{x \\in C_i} (x - \\mu_i)(x - \\mu_i)^T',
                    this.$refs.withinClassFormula,
                    { displayMode: true }
                );
            }


            // 渲染类间散度矩阵公式
            if (this.$refs.betweenClassFormula) {
                katex.render(
                    '\\Large S_B = \\sum_{i=1}^{c} n_i (\\mu_i - \\mu)(\\mu_i - \\mu)^T',
                    this.$refs.betweenClassFormula,
                    { displayMode: true }
                );
            }
        },
        calculateMatrix(type) {
            if (!this.isDataAvailable) {
                this.$message.error('数据不足，无法计算');
                return;
            }

            this.calculating = true;

            // 准备要发送到后端的数据
            const requestData = {
                nodeData: this.nodeData,
                matrixType: type,
                parameters: type === 'within' ? this.withinClassParams : this.betweenClassParams
            };

            // 发送请求到后端
            axios.post('/api/calculate-lda-matrix', requestData)
                .then(response => {
                    const newNode = response;

                    // 更新计算结果
                    if (type === 'within') {
                        this.result = {
                            type: 'within',
                            matrix: newNode.computed.within_class_scatter_matrix,
                            stats: newNode.computed.withinClassStats
                        };
                    } else {
                        this.result = {
                            type: 'between',
                            matrix: newNode.computed.between_class_scatter_matrix,
                            stats: newNode.computed.betweenClassStats
                        };
                    }

                    // 创建表格的列
                    this.generateMatrixColumns(this.result.matrix[0].length);

                    // 通知父组件新节点已创建
                    this.$emit('applyLDAdivergence', newNode);

                    this.$message.success('矩阵计算成功');
                })
                .catch(error => {
                    console.error('计算出错:', error);
                    this.$message.error('计算失败: ' + (error.response?.message || error.message));
                })
                .finally(() => {
                    this.calculating = false;
                });
        },
        generateMatrixColumns(columnCount) {
            // 为矩阵表格创建动态列
            this.matrixColumns = [
                { prop: 'row', label: '' } // 行索引列
            ];

            for (let i = 0; i < columnCount; i++) {
                this.matrixColumns.push({
                    prop: 'col' + i,
                    label: 'X' + (i + 1)
                });
            }
        },
        matrixToTableData(matrix) {
            // 将矩阵转换为表格数据格式
            return matrix.map((row, rowIndex) => {
                const tableRow = { row: 'X' + (rowIndex + 1) };

                row.forEach((val, colIndex) => {
                    tableRow['col' + colIndex] = val.toFixed(4);
                });

                return tableRow;
            });
        },
        clearResult() {
            this.result = null;
        }
    }
};
</script>

<style scoped>
.lda-matrix-calculator {
    margin: 20px;
}

.main-card {
    margin-bottom: 20px;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header h2 {
    margin: 0;
    color: #409EFF;
}

.no-data {
    padding: 20px 0;
}

.calculator-content {
    margin-top: 20px;
}

.formula-card {
    margin-bottom: 20px;
    background-color: #f8f9fa;
}

.formula-header {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #409EFF;
}

.formula {
    background-color: white;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
    margin-bottom: 15px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.formula-description {
    margin-top: 15px;
    font-size: 14px;
    color: #606266;
}

.formula-description ul {
    padding-left: 20px;
}

.params-form {
    background-color: white;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.data-info-card {
    margin-top: 20px;
}

.data-info-header {
    font-weight: bold;
    color: #409EFF;
}

.result-card {
    margin-top: 20px;
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: #409EFF;
}

.matrix-display {
    margin: 15px 0;
    overflow-x: auto;
}

.matrix-stats {
    margin-top: 15px;
    color: #606266;
    font-size: 14px;
}
</style>