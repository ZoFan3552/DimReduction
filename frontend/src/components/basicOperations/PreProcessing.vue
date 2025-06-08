<!-- SimpleDataPreprocessing.vue -->
<template>
    <div class="preprocessing-container">
        <div v-if="!nodeData" class="no-data-tip">
            <el-empty description="暂无数据">
                <!-- <el-button type="primary" @click="$emit('upload-data')">上传数据集</el-button> -->
            </el-empty>
        </div>
        <div v-else>
            <div class="header-container">
                <h3>数据集预处理</h3>

            </div>

            <div class="dataset-info" v-if="hasData">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-card shadow="hover" class="info-card">
                            <div slot="header">
                                <span>数据集大小</span>
                            </div>
                            <div class="info-content">
                                <i class="el-icon-s-data"></i>
                                <span>{{ datasetSize }} 条记录</span>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" class="info-card">
                            <div slot="header">
                                <span>特征数量</span>
                            </div>
                            <div class="info-content">
                                <i class="el-icon-s-grid"></i>
                                <span>{{ featureCount }} 个特征</span>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" class="info-card">
                            <div slot="header">
                                <span>标签类别</span>
                            </div>
                            <div class="info-content">
                                <i class="el-icon-collection-tag"></i>
                                <span>{{ labelCount }} 个类别</span>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </div>

            <!-- 基础预处理选项 -->
            <div class="preprocessing-options">
                <el-card shadow="hover">
                    <div slot="header">
                        <span>预处理选项</span>
                        <el-tooltip content="对数据进行预处理以提高模型性能" placement="top">
                            <i class="el-icon-question" style="margin-left: 8px; color: #909399;"></i>
                        </el-tooltip>
                    </div>

                    <el-form :model="options" label-width="120px" size="small">
                        <!-- 空缺值处理 -->
                        <el-form-item label="空缺值处理">
                            <el-select v-model="options.missingValues" placeholder="选择处理方式">
                                <el-option label="不处理" value="none"></el-option>
                                <el-option label="删除包含空缺值的行" value="drop_rows"></el-option>
                                <el-option label="使用均值填充" value="fill_mean"></el-option>
                                <el-option label="使用中位数填充" value="fill_median"></el-option>
                                <el-option label="使用众数填充" value="fill_mode"></el-option>
                                <el-option label="使用0填充" value="fill_zero"></el-option>
                            </el-select>
                            <div class="option-description">处理数据集中的缺失值</div>
                        </el-form-item>

                        <!-- 异常值处理 -->
                        <el-form-item label="异常值处理">
                            <el-select v-model="options.outliers" placeholder="选择处理方式">
                                <el-option label="不处理" value="none"></el-option>
                                <el-option label="删除异常值（IQR方法）" value="remove_iqr"></el-option>
                                <el-option label="删除异常值（Z分数法）" value="remove_zscore"></el-option>
                                <el-option label="用边界值替换" value="clip"></el-option>
                            </el-select>
                            <div class="option-description">处理数据集中的离群点</div>
                        </el-form-item>

                        <!-- 标准化/归一化 -->
                        <el-form-item label="特征缩放">
                            <el-select v-model="options.scaling" placeholder="选择处理方式">
                                <el-option label="不处理" value="none"></el-option>
                                <el-option label="标准化 (Z-Score)" value="standardization"></el-option>
                                <el-option label="归一化 (Min-Max)" value="normalization"></el-option>
                                <el-option label="稳健缩放" value="robust"></el-option>
                                <el-option label="最大绝对值缩放" value="max_abs"></el-option>
                            </el-select>
                            <div class="option-description">调整特征的尺度以便于模型训练</div>
                        </el-form-item>

                        <!-- 特征处理 -->
                        <el-form-item label="特征处理">
                            <el-checkbox-group v-model="options.featureProcess">
                                <el-checkbox label="remove_constant">移除常数特征</el-checkbox>
                                <el-checkbox label="remove_duplicates">移除重复行</el-checkbox>
                            </el-checkbox-group>
                            <div class="option-description">清理数据集中不必要的特征和行</div>
                        </el-form-item>
                    </el-form>
                    <div class="action-buttons">
                        <el-button type="success" size="small" :disabled="!hasData || processing"
                            @click="applyPreprocessing" :loading="processing" icon="el-icon-check">
                            应用
                        </el-button>
                        <el-button type="info" size="small" @click="resetOptions" icon="el-icon-refresh-left">
                            重置
                        </el-button>
                    </div>
                </el-card>
            </div>



            <!-- 结果预览 -->
            <div v-if="hasData && lastProcessedResult" class="result-preview">
                <el-card shadow="hover">
                    <div slot="header">
                        <span>预处理结果</span>
                        <el-tag type="success" size="small" style="margin-left: 10px;">已完成</el-tag>
                    </div>

                    <el-row :gutter="20">
                        <el-col :span="12">
                            <h4>处理前数据统计</h4>
                            <div class="stats-list">
                                <div class="stats-item">
                                    <span class="stats-label">数据量:</span>
                                    <span class="stats-value">{{ lastProcessedResult.before.rows }} 行</span>
                                </div>
                                <div class="stats-item">
                                    <span class="stats-label">特征数:</span>
                                    <span class="stats-value">{{ lastProcessedResult.before.cols }} 个</span>
                                </div>
                                <div class="stats-item">
                                    <span class="stats-label">缺失值:</span>
                                    <span class="stats-value">{{ lastProcessedResult.before.missing_values || 0 }}
                                        个</span>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="12">
                            <h4>处理后数据统计</h4>
                            <div class="stats-list">
                                <div class="stats-item">
                                    <span class="stats-label">数据量:</span>
                                    <span class="stats-value">{{ lastProcessedResult.after.rows }} 行</span>
                                </div>
                                <div class="stats-item">
                                    <span class="stats-label">特征数:</span>
                                    <span class="stats-value">{{ lastProcessedResult.after.cols }} 个</span>
                                </div>
                                <div class="stats-item">
                                    <span class="stats-label">缺失值:</span>
                                    <span class="stats-value">{{ lastProcessedResult.after.missing_values || 0 }}
                                        个</span>
                                </div>
                            </div>
                        </el-col>
                    </el-row>

                    <div class="processing-summary">
                        <h4>应用的处理</h4>
                        <el-tag v-for="(process, index) in lastProcessedResult.applied_processes" :key="index"
                            size="small" style="margin-right: 8px; margin-bottom: 8px;">
                            {{ process }}
                        </el-tag>
                    </div>
                </el-card>
            </div>

            <!-- 处理错误信息 -->
            <div v-if="processingError" class="processing-error">
                <el-alert :title="processingError" type="error" show-icon :closable="false">
                </el-alert>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '@/utils/flaskAxios';

export default {
    name: 'SimpleDataPreprocessing',
    props: {
        nodeData: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            processing: false,
            options: {
                missingValues: 'fill_mean',
                outliers: 'none',
                scaling: 'none',
                featureProcess: ['remove_constant']
            },
            defaultOptions: {
                missingValues: 'fill_mean',
                outliers: 'none',
                scaling: 'none',
                featureProcess: ['remove_constant']
            },
            lastProcessedResult: null,
            processingError: null
        };
    },
    computed: {
        hasData() {
            return this.nodeData &&
                this.nodeData.dataset &&
                this.nodeData.dataset.length > 0;
        },
        datasetSize() {
            return this.hasData ? this.nodeData.dataset.length : 0;
        },
        featureCount() {
            if (!this.hasData || !this.nodeData.dataset || this.nodeData.dataset.length === 0) return 0;
            return this.nodeData.dataset[0].length;
        },
        labelCount() {
            if (!this.hasData || !this.nodeData.target) return 0;
            const uniqueLabels = [...new Set(this.nodeData.target)];
            return uniqueLabels.length;
        }
    },
    methods: {
        resetOptions() {
            this.options = JSON.parse(JSON.stringify(this.defaultOptions));

            this.$message({
                message: '已重置预处理选项',
                type: 'info'
            });
        },
        applyPreprocessing() {
            if (!this.hasData || this.processing) return;

            this.processing = true;
            this.processingError = null;

            // 构建请求数据
            // eslint-disable-next-line no-unused-vars
            const { children, ...nodeDataWithoutChildren } = this.nodeData;
            const requestData = {
                nodeData: nodeDataWithoutChildren,
                options: { ...this.options }
            };

            // 记录处理前的统计信息
            const beforeStats = {
                rows: this.datasetSize,
                cols: this.featureCount,
                missing_values: this.countMissingValues()
            };

            // 发送预处理请求到Flask后端
            axios.post('/api/preprocess', requestData)
                .then(response => {
                    console.log("预处理返回的结果", response);
                    if (response && response.success) {
                        // 处理成功
                        const newNodeData = response.node;

                        // 更新处理结果信息
                        this.lastProcessedResult = {
                            before: beforeStats,
                            after: {
                                rows: newNodeData.dataset.length,
                                cols: newNodeData.dataset[0].length,
                                missing_values: this.countMissingValues(newNodeData)
                            },
                            applied_processes: this.getAppliedProcesses()
                        };

                        // 通知父组件更新节点
                        this.$emit('applyPreprocessing', newNodeData);

                        this.$message({
                            message: '数据预处理成功',
                            type: 'success'
                        });
                    } else {
                        // 处理失败
                        this.processingError = response.error || '预处理失败，请检查数据和选项';

                        this.$message({
                            message: this.processingError,
                            type: 'error'
                        });
                    }
                })
                .catch(error => {
                    // 处理请求错误
                    this.processingError = `请求错误: ${error.message || '未知错误'}`;

                    this.$message({
                        message: this.processingError,
                        type: 'error'
                    });
                })
                .finally(() => {
                    this.processing = false;
                });
        },
        countMissingValues(data = null) {
            // 计算数据集中的缺失值数量
            // 注意：这里假设缺失值表示为null或undefined，根据实际情况可能需要调整
            const dataToCheck = data || this.nodeData;
            if (!dataToCheck || !dataToCheck.dataset) return 0;

            let missingCount = 0;
            dataToCheck.dataset.forEach(row => {
                row.forEach(value => {
                    if (value === null || value === undefined) {
                        missingCount++;
                    }
                });
            });

            return missingCount;
        },
        getAppliedProcesses() {
            // 获取应用的预处理步骤描述
            const processes = [];

            // 空缺值处理
            if (this.options.missingValues !== 'none') {
                const missingValuesMap = {
                    'drop_rows': '删除包含空缺值的行',
                    'fill_mean': '均值填充空缺值',
                    'fill_median': '中位数填充空缺值',
                    'fill_mode': '众数填充空缺值',
                    'fill_zero': '零值填充空缺值'
                };
                processes.push(missingValuesMap[this.options.missingValues]);
            }

            // 异常值处理
            if (this.options.outliers !== 'none') {
                const outliersMap = {
                    'remove_iqr': '使用IQR方法移除异常值',
                    'remove_zscore': '使用Z分数法移除异常值',
                    'clip': '将异常值限制在合理范围内'
                };
                processes.push(outliersMap[this.options.outliers]);
            }

            // 特征缩放
            if (this.options.scaling !== 'none') {
                const scalingMap = {
                    'standardization': '标准化(Z-Score)',
                    'normalization': '归一化(Min-Max)',
                    'robust': '稳健缩放',
                    'max_abs': '最大绝对值缩放'
                };
                processes.push(scalingMap[this.options.scaling]);
            }

            // 特征处理
            if (this.options.featureProcess.includes('remove_constant')) {
                processes.push('移除常数特征');
            }

            if (this.options.featureProcess.includes('remove_duplicates')) {
                processes.push('移除重复行');
            }

            return processes;
        }
    }
};
</script>

<style scoped>
.preprocessing-container {
    width: 100%;
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 4px;
    max-height: 90vh;
    overflow-y: auto;
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.header-container h3 {
    margin: 0;
    color: #303133;
    font-size: 18px;
}

.action-buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
    /* 水平居中 */
}

.no-data-tip {
    height: 250px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 20px;
}

.dataset-info {
    margin-bottom: 20px;
}

.info-card {
    margin-bottom: 20px;
}

.info-content {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

.info-content i {
    margin-right: 8px;
    font-size: 20px;
    color: #409EFF;
}

.preprocessing-options {
    margin-bottom: 20px;
}

.option-description {
    margin-top: 5px;
    color: #909399;
    font-size: 12px;
}

.result-preview {
    margin-top: 20px;
}

.stats-list {
    margin-bottom: 15px;
}

.stats-item {
    margin-bottom: 8px;
    display: flex;
}

.stats-label {
    font-weight: bold;
    width: 80px;
}

.stats-value {
    color: #606266;
}

.processing-summary {
    margin-top: 15px;
    border-top: 1px solid #EBEEF5;
    padding-top: 15px;
}

.processing-summary h4 {
    margin-top: 0;
    margin-bottom: 10px;
}

.processing-error {
    margin-top: 20px;
}

h4 {
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 14px;
    color: #303133;
}

/* 自定义滚动条样式 */
.preprocessing-container::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

.preprocessing-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.preprocessing-container::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.preprocessing-container::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
</style>