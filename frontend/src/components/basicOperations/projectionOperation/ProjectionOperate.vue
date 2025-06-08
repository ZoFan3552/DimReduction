<template>
    <div class="projection-component">

        <!-- 无数据提示 -->
        <div v-if="!nodeData" class="no-data">
            <el-empty description="暂无数据，请先选择数据集节点"></el-empty>
        </div>

        <!-- 有数据时的主界面 -->
        <div v-else class="content">
            <!-- 矩阵选择 -->
            <el-card class="matrix-card" shadow="hover">
                <div slot="header" class="card-header">
                    <span>选择矩阵类型</span>
                    <el-tooltip content="不同矩阵的特征向量具有不同的投影意义" placement="top">
                        <i class="el-icon-info"></i>
                    </el-tooltip>
                </div>
                <el-radio-group v-model="selectedMatrix" @change="onMatrixChange">
                    <el-radio-button v-for="matrix in availableMatrices" :key="matrix.value" :label="matrix.value"
                        :disabled="!matrix.available">
                        <span>{{ matrix.label }}</span>
                        <el-badge v-if="matrix.available" :value="matrix.dimensions" class="matrix-badge" type="info" />
                        <el-tooltip v-else content="缺少该矩阵的特征向量和特征值数据" placement="top">
                            <i class="el-icon-warning-outline" style="color: #F56C6C; margin-left: 5px;"></i>
                        </el-tooltip>
                    </el-radio-button>
                </el-radio-group>

                <!-- 矩阵说明 -->
                <el-alert v-if="selectedMatrix && matrixDescription[selectedMatrix]"
                    :title="matrixDescription[selectedMatrix].title"
                    :description="matrixDescription[selectedMatrix].description" type="info" show-icon :closable="false"
                    style="margin-top: 20px"></el-alert>
            </el-card>

            <!-- 特征向量选择 -->
            <el-card v-if="selectedMatrix && currentEigenvectors.length > 0" class="eigenvector-card" shadow="hover">
                <div slot="header" class="card-header">
                    <span>特征向量选择</span>
                    <el-tag type="info" size="mini">{{ selectedMatrixLabel }}的特征向量</el-tag>
                </div>

                <!-- 特征值贡献率图表 -->
                <div class="eigenvalue-chart">
                    <div class="chart-title">特征值分布与贡献率</div>
                    <div class="chart-content">
                        <div v-for="(item, index) in eigenvalueContribution" :key="index" class="contribution-item">
                            <div class="contribution-bar">
                                <div class="bar-label">λ{{ index + 1 }}</div>
                                <div class="bar-container">
                                    <div class="bar-fill" :style="{
                                        width: item.percentage + '%',
                                        background: getBarGradient(item.percentage)
                                    }"></div>
                                    <span class="bar-value">{{ item.percentage.toFixed(2) }}%</span>
                                </div>
                            </div>
                            <div class="eigenvalue-info">
                                <span class="eigenvalue">特征值: {{ item.eigenvalue.toFixed(6) }}</span>
                                <span class="cumulative">累积: {{ item.cumulative.toFixed(2) }}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 特征向量选择表格 -->
                <el-table :data="currentEigenvectors" @selection-change="handleSelectionChange" style="margin-top: 20px"
                    ref="eigenvectorTable" row-key="index">
                    <el-table-column type="selection" width="55" align="center"></el-table-column>
                    <el-table-column prop="index" label="编号" width="80" align="center">
                        <template slot-scope="scope">
                            λ{{ scope.row.index + 1 }}
                        </template>
                    </el-table-column>
                    <el-table-column prop="eigenvalue" label="特征值" width="150" align="center">
                        <template slot-scope="scope">
                            {{ scope.row.eigenvalue.toFixed(6) }}
                        </template>
                    </el-table-column>
                    <el-table-column prop="contribution" label="贡献率" width="140" align="center">
                        <template slot-scope="scope">
                            <el-progress :percentage="scope.row.contribution" :format="format"
                                :color="getProgressColor(scope.row.contribution)"></el-progress>
                        </template>
                    </el-table-column>
                    <el-table-column prop="cumulative" label="累积贡献率" width="120" align="center">
                        <template slot-scope="scope">
                            {{ scope.row.cumulative.toFixed(2) }}%
                        </template>
                    </el-table-column>
                    <el-table-column label="特征向量预览" align="center">
                        <template slot-scope="scope">
                            <el-popover placement="bottom" width="300" trigger="hover">
                                <div class="eigenvector-preview">
                                    <div v-for="(value, idx) in scope.row.eigenvector.slice(0, 5)" :key="idx">
                                        v{{ idx + 1 }}: {{ value.toFixed(4) }}
                                    </div>
                                    <div v-if="scope.row.eigenvector.length > 5">...</div>
                                </div>
                                <el-button slot="reference" type="text" size="small">查看向量</el-button>
                            </el-popover>
                        </template>
                    </el-table-column>
                </el-table>

                <!-- 建议提示 -->
                <el-alert v-if="recommendedComponents > 0"
                    :title="`建议选择前 ${recommendedComponents} 个特征向量，可保留 ${recommendedCumulative.toFixed(2)}% 的信息`"
                    type="success" show-icon style="margin-top: 20px"></el-alert>
            </el-card>

            <!-- 参数设置 -->
            <el-card v-if="selectedEigenvectors.length > 0" class="parameter-card" shadow="hover">
                <div slot="header" class="card-header">
                    <span>投影参数设置</span>
                </div>
                <el-form :model="projectionParams" label-width="120px">
                    <el-form-item label="标准化数据">
                        <el-switch v-model="projectionParams.standardize"></el-switch>
                        <el-tooltip content="建议开启，使不同量纲的特征具有可比性" placement="right">
                            <i class="el-icon-info" style="margin-left: 10px"></i>
                        </el-tooltip>
                    </el-form-item>
                    <el-form-item label="输出维度">
                        <el-input-number v-model="projectionParams.outputDimension" :min="1"
                            :max="selectedEigenvectors.length" :step="1"></el-input-number>
                        <span class="dimension-hint">最多可选择 {{ selectedEigenvectors.length }} 维</span>
                    </el-form-item>
                </el-form>
            </el-card>

            <!-- 操作按钮 -->
            <div class="operation-buttons">
                <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
                <el-button type="primary" @click="handleProject" icon="el-icon-s-promotion"
                    :disabled="selectedEigenvectors.length === 0" :loading="loading">
                    执行投影
                </el-button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '@/utils/flaskAxios';
export default {
    name: 'ProjectionComponent',
    props: {
        nodeData: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            selectedMatrix: '',
            selectedEigenvectors: [],
            projectionParams: {
                standardize: true,
                outputDimension: 2
            },
            loading: false,
            matrixDescription: {
                'covariance': {
                    title: '协方差矩阵',
                    description: '描述变量之间的相关性，其特征向量指向数据方差最大的方向。适合用于PCA主成分分析，实现无监督的数据降维。'
                },
                'within_class_scatter': {
                    title: '类内散度矩阵',
                    description: '衡量同一类别内部数据的分散程度。其特征向量描述了类别内部的主要变化方向。'
                },
                'between_class_scatter': {
                    title: '类间散度矩阵',
                    description: '衡量不同类别之间的差异程度。其特征向量指向最能区分不同类别的方向，适合用于LDA线性判别分析。'
                },
                'lda': {
                    title: 'LDA广义特征值分解',
                    description: '通过求解类间散度矩阵和类内散度矩阵的广义特征值问题得到的特征向量。直接提供了LDA的最优投影方向，能够最大化类间距离同时最小化类内距离。'
                }
            }
        }
    },
    computed: {
        // 获取可用的矩阵列表
        availableMatrices() {
            if (!this.nodeData?.computed) return []

            const matrices = [
                {
                    value: 'covariance',
                    label: '协方差矩阵',
                    key: 'covariance',
                    eigenvectors: 'covariance_eigenvectors',
                    eigenvalues: 'covariance_eigenvalues'
                },
                {
                    value: 'within_class_scatter',
                    label: '类内散度矩阵',
                    key: 'within_class_scatter',
                    eigenvectors: 'within_class_scatter_eigenvectors',
                    eigenvalues: 'within_class_scatter_eigenvalues'
                },
                {
                    value: 'between_class_scatter',
                    label: '类间散度矩阵',
                    key: 'between_class_scatter',
                    eigenvectors: 'between_class_scatter_eigenvectors',
                    eigenvalues: 'between_class_scatter_eigenvalues'
                },
                {
                    value: 'lda',
                    label: 'LDA广义特征向量',
                    key: 'lda',
                    eigenvectors: 'lda_eigenvectors',
                    eigenvalues: 'lda_eigenvalues'
                }
            ]

            return matrices.map(matrix => {
                const hasData = this.nodeData.computed[matrix.eigenvectors] &&
                    this.nodeData.computed[matrix.eigenvalues]

                // 正确获取特征向量维度（列向量）
                const dimensions = hasData ?
                    (this.nodeData.computed[matrix.eigenvectors][0] ?
                        this.nodeData.computed[matrix.eigenvectors].length : 0) : 0

                return {
                    ...matrix,
                    available: hasData,
                    dimensions
                }
            })
        },

        // 获取当前选中矩阵的标签
        selectedMatrixLabel() {
            const matrix = this.availableMatrices.find(m => m.value === this.selectedMatrix)
            return matrix ? matrix.label : ''
        },

        // 获取当前选中矩阵的特征向量和特征值
        currentEigenvectors() {
            if (!this.selectedMatrix || !this.nodeData?.computed) return []

            const matrix = this.availableMatrices.find(m => m.value === this.selectedMatrix)
            if (!matrix) return []

            const eigenvectors = this.nodeData.computed[matrix.eigenvectors]
            const eigenvalues = this.nodeData.computed[matrix.eigenvalues]

            if (!eigenvectors || !eigenvalues) return []

            // 计算贡献率
            const totalEigenvalue = eigenvalues.reduce((sum, val) => sum + Math.abs(val), 0)
            let cumulative = 0

            // 转置特征向量矩阵处理 - 现在正确处理列向量作为特征向量
            const transposedEigenvectors = this.transposeMatrix(eigenvectors)

            return eigenvalues.map((eigenvalue, index) => {
                const contribution = totalEigenvalue > 0 ? (Math.abs(eigenvalue) / totalEigenvalue) * 100 : 0
                cumulative += contribution
                return {
                    index,
                    eigenvalue,
                    // 使用转置后的特征向量
                    eigenvector: transposedEigenvectors[index] || [],
                    contribution,
                    cumulative
                }
            }).sort((a, b) => Math.abs(b.eigenvalue) - Math.abs(a.eigenvalue))
        },

        // 特征值贡献率可视化数据
        eigenvalueContribution() {
            return this.currentEigenvectors.map(item => ({
                eigenvalue: item.eigenvalue,
                percentage: item.contribution,
                cumulative: item.cumulative
            }))
        },

        // 推荐选择的特征向量数量
        recommendedComponents() {
            const index = this.currentEigenvectors.findIndex(item => item.cumulative >= 85)
            return index === -1 ? Math.min(3, this.currentEigenvectors.length) : index + 1
        },

        recommendedCumulative() {
            if (this.recommendedComponents > 0 && this.recommendedComponents <= this.currentEigenvectors.length) {
                return this.currentEigenvectors[this.recommendedComponents - 1].cumulative
            }
            return 0
        }
    },
    methods: {
        // 矩阵转置函数 - 将列向量转为行向量
        transposeMatrix(matrix) {
            if (!matrix || !matrix.length) return []

            const rows = matrix.length
            const cols = matrix[0].length

            // 初始化结果矩阵
            const result = new Array(cols)
            for (let i = 0; i < cols; i++) {
                result[i] = new Array(rows)
            }

            // 执行转置
            for (let i = 0; i < rows; i++) {
                for (let j = 0; j < cols; j++) {
                    result[j][i] = matrix[i][j]
                }
            }

            return result
        },

        // 矩阵切换处理
        onMatrixChange() {
            this.selectedEigenvectors = []
            this.$refs.eigenvectorTable?.clearSelection()
        },

        // 特征向量选择变化处理
        handleSelectionChange(selection) {
            this.selectedEigenvectors = selection
            console.log("特征向量变化", this.selectedEigenvectors)
            this.projectionParams.outputDimension = Math.min(selection.length, this.projectionParams.outputDimension)
        },

        // 获取进度条颜色
        getProgressColor(percentage) {
            if (percentage >= 30) return '#67C23A'
            if (percentage >= 10) return '#E6A23C'
            return '#F56C6C'
        },

        // 获取条形图渐变色
        getBarGradient(percentage) {
            if (percentage >= 30) {
                return 'linear-gradient(90deg, #67C23A, #85CE61)'
            } else if (percentage >= 10) {
                return 'linear-gradient(90deg, #E6A23C, #F0C78A)'
            }
            return 'linear-gradient(90deg, #F56C6C, #F89898)'
        },

        // 格式化进度条显示
        format(percentage) {
            return `${percentage.toFixed(1)}%`
        },

        // 重置操作
        handleReset() {
            this.selectedMatrix = ''
            this.selectedEigenvectors = []
            this.projectionParams = {
                standardize: true,
                outputDimension: 2
            }
            this.$refs.eigenvectorTable?.clearSelection()
        },

        // 执行投影
        async handleProject() {
            if (this.selectedEigenvectors.length === 0) {
                this.$message.warning('请选择至少一个特征向量')
                return
            }

            this.loading = true
            try {
                // 获取当前选择的矩阵类型信息
                const matrixInfo = this.availableMatrices.find(m => m.value === this.selectedMatrix)

                // 准备发送到后端的数据
                const requestData = {
                    matrix_type: this.selectedMatrix,
                    matrix_label: this.selectedMatrixLabel,
                    // 将选中的特征向量转换回列向量形式发送给后端
                    eigenvectors: this.selectedEigenvectors.map(item => {
                        // 获取原始列向量
                        const colIndex = item.index
                        const originalMatrix = this.nodeData.computed[matrixInfo.eigenvectors]
                        const colVector = []

                        // 从原始矩阵中提取列向量
                        for (let i = 0; i < originalMatrix.length; i++) {
                            colVector.push(originalMatrix[i][colIndex])
                        }

                        return colVector
                    }),
                    eigenvalues: this.selectedEigenvectors.map(item => item.eigenvalue),
                    standardize: this.projectionParams.standardize,
                    outputDimension: this.projectionParams.outputDimension,
                    nodeData: this.nodeData
                }

                // 调用后端API
                const response = await axios.post('/api/projection', requestData);

                if (response.success) {
                    this.$message.success('投影成功')
                    this.$emit('projection-complete', response.node)
                } else {
                    this.$message.error(response.message || '投影失败')
                }
            } catch (error) {
                console.error('投影失败:', error)
                this.$message.error('投影操作失败，请重试')
            } finally {
                this.loading = false
            }
        }
    },
    watch: {
        nodeData: {
            handler(newVal) {
                if (newVal && !this.selectedMatrix) {
                    // 自动选择第一个可用的矩阵
                    const firstAvailable = this.availableMatrices.find(m => m.available)
                    if (firstAvailable) {
                        this.selectedMatrix = firstAvailable.value
                    }
                }
            },
            immediate: true
        }
    }
}
</script>

<style scoped>
.projection-component {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    display: flex;
    align-items: center;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px 8px 0 0;
    margin-bottom: 20px;
    font-size: 18px;
    font-weight: bold;
}

.header i {
    margin-right: 10px;
    font-size: 24px;
}

.no-data {
    text-align: center;
    padding: 60px 20px;
    background: #f5f7fa;
    border-radius: 8px;
}

.content {
    padding: 0 20px 20px;
}

.el-card {
    margin-bottom: 20px;
    border-radius: 8px;
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.matrix-card {
    background: #fafafa;
}

.el-radio-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.el-radio-button {
    margin-right: 0;
}

.matrix-badge {
    margin-left: 8px;
}



.eigenvalue-chart {
    margin-bottom: 20px;
    padding: 20px;
    background: #f5f7fa;
    border-radius: 8px;
}

.chart-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #303133;
}

.contribution-item {
    margin-bottom: 15px;
}

.contribution-bar {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
}

.bar-label {
    width: 50px;
    font-weight: bold;
    color: #606266;
}

.bar-container {
    flex: 1;
    height: 24px;
    background: #e4e7ed;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 12px;
    transition: width 0.3s ease;
}

.bar-value {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #303133;
    font-size: 12px;
    font-weight: bold;
}

.eigenvalue-info {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #909399;
    margin-left: 50px;
    padding: 0 10px;
}

.eigenvalue {
    color: #606266;
}

.cumulative {
    color: #409eff;
}

.eigenvector-preview {
    font-family: monospace;
    font-size: 12px;
    line-height: 1.8;
}

.dimension-hint {
    margin-left: 15px;
    color: #909399;
    font-size: 12px;
}

.operation-buttons {
    text-align: center;
    margin-top: 30px;
}

.el-button {
    margin: 0 10px;
}
</style>