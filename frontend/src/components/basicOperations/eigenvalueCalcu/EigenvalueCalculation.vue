<template>
    <div class="eigen-solver-container">
        <el-card class="eigen-solver-card" shadow="hover">
            <div slot="header" class="header">
                <h3>矩阵特征值和特征向量计算</h3>
            </div>

            <div v-if="!nodeData" class="no-data">
                <el-alert title="未选择数据节点" type="info" description="请先选择包含矩阵数据的节点" show-icon
                    :closable="false"></el-alert>
            </div>

            <div v-else-if="!hasMatrices" class="no-matrices">
                <el-alert title="未找到可用矩阵" type="warning" description="所选节点中没有可用于计算特征值和特征向量的矩阵" show-icon
                    :closable="false"></el-alert>
            </div>

            <div v-else class="solver-content">
                <el-form ref="form" :model="form" label-width="150px">
                    <el-form-item label="计算类型">
                        <el-radio-group v-model="form.calculationType" @change="radio_changed">
                            <el-radio label="single">单矩阵特征值/特征向量</el-radio>
                            <el-radio label="generalized">广义特征值/特征向量</el-radio>
                        </el-radio-group>
                    </el-form-item>

                    <!-- 单矩阵计算选项 -->
                    <template v-if="form.calculationType === 'single'">
                        <el-form-item label="选择矩阵">
                            <el-select v-model="form.singleMatrix" placeholder="请选择矩阵">
                                <el-option v-for="matrix in availableMatrices" :key="matrix.value" :label="matrix.label"
                                    :value="matrix.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </template>

                    <!-- 广义特征值计算选项 -->
                    <template v-else>
                        <el-form-item label="矩阵A">
                            <el-select v-model="form.matrixA" placeholder="请选择矩阵A">
                                <el-option v-for="matrix in availableMatrices" :key="matrix.value" :label="matrix.label"
                                    :value="matrix.value">
                                </el-option>
                            </el-select>
                        </el-form-item>

                        <el-form-item label="矩阵B">
                            <el-select v-model="form.matrixB" placeholder="请选择矩阵B">
                                <el-option v-for="matrix in availableMatrices" :key="matrix.value" :label="matrix.label"
                                    :value="matrix.value">
                                </el-option>
                            </el-select>
                        </el-form-item>

                        <el-form-item>
                            <el-tooltip
                                content="常用组合：A=between_class_scatter_matrix, B=within_class_scatter_matrix (LDA算法)"
                                placement="top">
                                <el-button type="text" icon="el-icon-info">常用组合提示</el-button>
                            </el-tooltip>
                        </el-form-item>
                    </template>

                    <el-form-item>
                        <el-button type="primary" @click="calculateEigen" :loading="loading"
                            :disabled="!isFormValid">计算</el-button>
                        <el-button @click="resetForm">重置</el-button>
                    </el-form-item>
                </el-form>

                <!-- 计算结果预览 -->
                <div v-if="hasResults" class="results-preview">
                    <el-divider content-position="center">计算结果预览</el-divider>

                    <el-tabs type="border-card">
                        <el-tab-pane label="特征值">
                            <div class="result-table">
                                <el-table :data="eigenvaluesTable" stripe style="width: 100%" height="250">
                                    <el-table-column prop="index" label="索引" width="80"></el-table-column>
                                    <el-table-column prop="value" label="特征值"></el-table-column>
                                </el-table>
                            </div>
                        </el-tab-pane>

                        <el-tab-pane label="特征向量">
                            <div class="result-table">
                                <el-table :data="eigenvectorsTable" stripe style="width: 100%" height="250">
                                    <el-table-column prop="index" label="索引" width="80"></el-table-column>
                                    <el-table-column v-for="(col, index) in eigenvectorColumns" :key="index"
                                        :prop="'v' + index" :label="'V' + index">
                                    </el-table-column>
                                </el-table>
                            </div>
                        </el-tab-pane>
                    </el-tabs>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import axios from '@/utils/calculatorAxios';

export default {
    name: 'EigenSolver',
    props: {
        nodeData: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            form: {
                calculationType: 'single',
                singleMatrix: '',
                matrixA: '',
                matrixB: ''
            },
            loading: false,
            results: null
        };
    },
    computed: {
        availableMatrices() {
            if (!this.nodeData || !this.nodeData.computed) return [];

            const matrices = [];
            const computed = this.nodeData.computed;

            if (computed.covariance_matrix) {
                matrices.push({
                    label: '协方差矩阵 (Covariance Matrix)',
                    value: 'covariance_matrix'
                });
            }

            if (computed.within_class_scatter_matrix) {
                matrices.push({
                    label: '类内散度矩阵 (Within-class Scatter Matrix)',
                    value: 'within_class_scatter_matrix'
                });
            }

            if (computed.between_class_scatter_matrix) {
                matrices.push({
                    label: '类间散度矩阵 (Between-class Scatter Matrix)',
                    value: 'between_class_scatter_matrix'
                });
            }

            return matrices;
        },
        hasMatrices() {
            return this.availableMatrices.length > 0;
        },
        isFormValid() {
            if (this.form.calculationType === 'single') {
                return !!this.form.singleMatrix;
            } else {
                return !!this.form.matrixA && !!this.form.matrixB;
            }
        },
        hasResults() {
            return !!this.results;
        },
        eigenvaluesTable() {
            if (!this.results || !this.results.eigenvalues) return [];

            return this.results.eigenvalues.map((value, index) => ({
                index: index + 1,
                value: value.toFixed(6)
            }));
        },
        eigenvectorsTable() {
            if (!this.results || !this.results.eigenvectors) return [];

            const eigenvectors = this.results.eigenvectors;
            const rows = [];

            for (let i = 0; i < eigenvectors.length; i++) {
                const row = { index: i + 1 };
                for (let j = 0; j < eigenvectors[i].length; j++) {
                    row['v' + j] = eigenvectors[i][j].toFixed(6);
                }
                rows.push(row);
            }

            return rows;
        },
        eigenvectorColumns() {
            if (!this.results || !this.results.eigenvectors || this.results.eigenvectors.length === 0) {
                return [];
            }
            return new Array(this.results.eigenvectors[0].length);
        }
    },
    methods: {
        radio_changed() {
            this.results = null;
        },
        calculateEigen() {
            if (!this.isFormValid) return;

            this.loading = true;

            // 构建请求数据
            const requestData = {
                node_data: this.nodeData,
                calculation_type: this.form.calculationType
            };

            if (this.form.calculationType === 'single') {
                requestData.matrix_name = this.form.singleMatrix;
            } else {
                requestData.matrix_a_name = this.form.matrixA;
                requestData.matrix_b_name = this.form.matrixB;
            }

            // 发送请求到后端
            axios.post('/api/calculate-eigen', requestData)
                .then(response => {
                    this.results = {
                        eigenvalues: response.eigenvalues,
                        eigenvectors: response.eigenvectors
                    };

                    // 发送更新后的节点数据到父组件
                    this.$emit('analysis-complete', response.new_node);

                    this.$message({
                        message: '特征值和特征向量计算成功',
                        type: 'success'
                    });
                })
                .catch(error => {
                    console.error('计算特征值和特征向量时出错:', error);
                    this.$message.error('计算失败: ' + (error.response?.error || '未知错误'));
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        resetForm() {
            this.form = {
                calculationType: 'single',
                singleMatrix: '',
                matrixA: '',
                matrixB: ''
            };
            this.results = null;
        }
    }
};
</script>

<style scoped>
.eigen-solver-container {
    padding: 20px;
}

.eigen-solver-card {
    max-width: 900px;
    margin: 0 auto;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header h3 {
    margin: 0;
    color: #409EFF;
}

.no-data,
.no-matrices {
    padding: 20px 0;
}

.solver-content {
    padding: 10px 0;
}

.results-preview {
    margin-top: 30px;
}

.result-table {
    margin: 15px 0;
}

.el-divider__text {
    background-color: #f5f7fa;
    color: #409EFF;
    font-weight: bold;
}
</style>