<template>
    <div class="dataset-import-container">
        <el-card class="dataset-card">
            <div slot="header" class="card-header">
                <span>数据集导入</span>
                <el-button type="primary" size="small" :disabled="!selectedDataset" @click="importDataset">
                    导入选中数据集
                </el-button>
            </div>

            <el-tabs v-model="activeTab">
                <el-tab-pane label="经典数据集" name="classic">
                    <!-- 经典数据集选择区域 -->
                    <div class="dataset-grid">
                        <el-card v-for="dataset in classicDatasets" :key="dataset.id"
                            :class="['dataset-item', { selected: selectedDataset === dataset.id }]" shadow="hover"
                            @click.native="selectDataset(dataset.id)">
                            <div class="dataset-item-content">
                                <div class="dataset-icon">
                                    <i :class="dataset.icon"></i>
                                </div>
                                <div class="dataset-info">
                                    <h4>{{ dataset.name }}</h4>
                                    <p class="dataset-desc">{{ dataset.description }}</p>
                                    <el-tag size="mini">{{ dataset.samples }}个样本</el-tag>
                                    <el-tag size="mini" type="success">{{ dataset.features }}个特征</el-tag>
                                    <el-tag size="mini" type="warning">{{ dataset.classes }}个类别</el-tag>
                                </div>
                            </div>
                        </el-card>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </el-card>

        <!-- 数据集预览对话框 -->
        <el-dialog title="数据集预览" :visible.sync="previewVisible" width="70%">
            <div v-if="datasetPreview" class="dataset-preview">
                <div class="dataset-details">
                    <h3>{{ currentDatasetInfo.name }}</h3>
                    <p>{{ currentDatasetInfo.description }}</p>
                    <el-divider></el-divider>
                </div>

                <el-table :data="datasetPreview.data" border stripe height="400px">
                    <el-table-column type="index" width="50"></el-table-column>
                    <el-table-column v-for="(column, index) in datasetPreview.columns" :key="index" :prop="column.prop"
                        :label="column.label" width="150"></el-table-column>
                </el-table>

                <div class="dataset-stats">
                    <el-divider content-position="left">数据集统计信息</el-divider>
                    <el-row :gutter="20">
                        <el-col :span="8">
                            <el-statistic title="样本数量" :value="currentDatasetInfo.samples"></el-statistic>
                        </el-col>
                        <el-col :span="8">
                            <el-statistic title="特征数量" :value="currentDatasetInfo.features"></el-statistic>
                        </el-col>
                        <el-col :span="8">
                            <el-statistic title="类别数量" :value="currentDatasetInfo.classes"></el-statistic>
                        </el-col>
                    </el-row>
                </div>
            </div>

            <span slot="footer" class="dialog-footer">
                <el-button @click="previewVisible = false">取消</el-button>
                <el-button type="primary" @click="confirmImport">确认导入</el-button>
            </span>
        </el-dialog>

        <!-- 加载提示 -->
        <el-dialog title="数据集处理中" :visible.sync="loadingVisible" :close-on-click-modal="false"
            :close-on-press-escape="false" :show-close="false" width="30%">
            <div class="loading-content">
                <el-progress type="circle" :percentage="loadingProgress"></el-progress>
                <p>{{ loadingMessage }}</p>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import axios from '@/utils/flaskAxios';

export default {
    name: 'DatasetImportPanel',
    props: {
        // 当前节点ID，用于更新树状图
        nodeId: {
            type: String,
            default: '1'  // 默认为根节点
        }
    },
    data() {
        return {
            activeTab: 'classic',
            selectedDataset: null,
            uploadedFile: null,
            classicDatasets: [
                {
                    id: 'iris',
                    name: '鸢尾花数据集 (Iris)',
                    description: '包含三种鸢尾花的四个特征：萼片长度、萼片宽度、花瓣长度和花瓣宽度',
                    samples: 150,
                    features: 4,
                    classes: 3,
                    icon: 'el-icon-cherry'
                },
                {
                    id: 'wine',
                    name: '红酒数据集 (Wine)',
                    description: '使用化学分析确定葡萄酒的产地，包含13个特征',
                    samples: 178,
                    features: 13,
                    classes: 3,
                    icon: 'el-icon-goblet-full'
                },
                {
                    id: 'breast_cancer',
                    name: '乳腺癌数据集 (Breast Cancer)',
                    description: '威斯康星乳腺癌诊断数据集，包含肿瘤细胞的形状特征',
                    samples: 569,
                    features: 30,
                    classes: 2,
                    icon: 'el-icon-first-aid-kit'
                },

                {
                    id: 'mnist_small',
                    name: 'MNIST手写数字(小样本)',
                    description: '手写数字数据集的小样本版本，包含28x28像素的手写数字图像',
                    samples: 2000,
                    features: 784,
                    classes: 10,
                    icon: 'el-icon-edit'
                },
            ],
            previewVisible: false,
            loadingVisible: false,
            loadingProgress: 0,
            loadingMessage: '加载数据集中...',
            datasetPreview: null,
            currentDatasetInfo: {}
        };
    },
    methods: {
        // 选择经典数据集
        selectDataset(datasetId) {
            this.selectedDataset = datasetId;
        },

        // 导入选中的经典数据集
        importDataset() {
            if (!this.selectedDataset) return;

            this.loadingVisible = true;
            this.loadingProgress = 0;
            this.loadingMessage = '正在获取数据集...';

            // 模拟加载进度
            const interval = setInterval(() => {
                this.loadingProgress += 10;
                if (this.loadingProgress >= 90) {
                    clearInterval(interval);
                }
            }, 200);



            // 获取数据集预览
            axios.get(`/api/dataset/${this.selectedDataset}/preview`)
                .then(response => {
                    // console.log("数据集get1");
                    clearInterval(interval);
                    this.loadingProgress = 100;
                    this.loadingMessage = '数据加载完成！';

                    // 设置当前数据集信息
                    this.currentDatasetInfo = this.classicDatasets.find(d => d.id === this.selectedDataset);
                    console.log("数据集get", response);
                    // 准备预览数据
                    this.preparePreviewData(response);

                    setTimeout(() => {
                        this.loadingVisible = false;
                        this.previewVisible = true;
                    }, 500);
                })
                .catch(error => {
                    clearInterval(interval);
                    this.loadingVisible = false;
                    this.$message.error('获取数据集失败: ' + (error.response?.data?.message || error.message));
                });
        },

        // 处理上传文件
        handleUpload(options) {
            const file = options.file;

            // 检查文件类型
            const isCSV = file.type === 'text/csv';
            const isExcel =
                file.type === 'application/vnd.ms-excel' ||
                file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';

            if (!isCSV && !isExcel) {
                this.$message.error('只支持CSV或Excel文件!');
                return;
            }

            // 保存上传的文件信息
            this.uploadedFile = file;
            this.$message.success('文件上传成功，可以点击导入按钮进行导入');
        },

        // 导入上传的数据集
        importUploadedDataset() {
            if (!this.uploadedFile) return;

            this.loadingVisible = true;
            this.loadingProgress = 0;
            this.loadingMessage = '正在解析上传的数据集...';

            // 创建表单数据
            const formData = new FormData();
            formData.append('file', this.uploadedFile);

            // 模拟加载进度
            const interval = setInterval(() => {
                this.loadingProgress += 5;
                if (this.loadingProgress >= 90) {
                    clearInterval(interval);
                }
            }, 100);

            // 发送文件到后端
            axios.post('/api/dataset/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
                .then(response => {
                    clearInterval(interval);
                    this.loadingProgress = 100;
                    this.loadingMessage = '数据解析完成！';

                    // 设置自定义数据集信息
                    const data = response.data;
                    this.currentDatasetInfo = {
                        id: 'custom',
                        name: this.uploadedFile.name,
                        description: '用户上传的自定义数据集',
                        samples: data.samples,
                        features: data.features,
                        classes: data.classes,
                        icon: 'el-icon-upload'
                    };

                    // 准备预览数据
                    this.preparePreviewData(data);

                    setTimeout(() => {
                        this.loadingVisible = false;
                        this.previewVisible = true;
                    }, 500);
                })
                .catch(error => {
                    clearInterval(interval);
                    this.loadingVisible = false;
                    this.$message.error('处理数据集失败: ' + (error.response?.data?.message || error.message));
                });
        },

        // 准备预览数据
        preparePreviewData(data) {
            // 构建表格列
            const columns = data.feature_names.map((name, index) => ({
                prop: `feature_${index}`,
                label: name
            }));

            // 添加目标列
            columns.push({
                prop: 'target',
                label: '目标分类'
            });

            // 构建表格数据
            const tableData = data.samples.map((sample, i) => {
                const row = {};
                sample.forEach((value, j) => {
                    row[`feature_${j}`] = value;
                });
                row.target = data.targets[i];
                return row;
            });

            // 限制预览最多显示100行
            this.datasetPreview = {
                columns: columns,
                data: tableData.slice(0, 100)
            };
        },

        // 确认导入数据集
        confirmImport() {
            this.previewVisible = false;
            this.loadingVisible = true;
            this.loadingProgress = 0;
            this.loadingMessage = '正在导入数据集到降维流程...';

            // 准备导入请求数据
            // const requestData = {
            //     nodeId: this.nodeId,
            //     datasetId: this.selectedDataset || 'custom',
            //     type: this.selectedDataset ? 'classic' : 'custom',
            //     fileName: this.uploadedFile ? this.uploadedFile.name : null
            // };

            // 模拟加载进度
            const interval = setInterval(() => {
                this.loadingProgress += 5;
                if (this.loadingProgress >= 90) {
                    clearInterval(interval);
                }
            }, 100);

            // 发送请求到后端
            axios.get(`/api/dataset/${this.selectedDataset}`)
                .then(response => {
                    clearInterval(interval);
                    this.loadingProgress = 100;
                    this.loadingMessage = '数据集导入成功！';

                    setTimeout(() => {
                        this.loadingVisible = false;
                        console.log("接受到数据集进行导入0", response)
                        // 通知父组件更新树状图
                        this.$emit('datasetImported', response);

                        this.$message.success('1数据集已成功导入到降维流程中1');

                        // 重置选择状态
                        this.selectedDataset = null;
                        this.uploadedFile = null;
                    }, 500);
                })
                .catch(error => {
                    clearInterval(interval);
                    this.loadingVisible = false;
                    this.$message.error('导入数据集失败: ' + (error.response?.data?.message || error.message));
                });
        }
    }
};
</script>

<style scoped>
.dataset-import-container {
    width: 100%;
}

.dataset-card {
    margin-bottom: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dataset-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
    margin-top: 20px;
}

.dataset-item {
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid #e8e8e8;
}

.dataset-item.selected {
    border: 2px solid #409EFF;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dataset-item-content {
    display: flex;
    align-items: flex-start;
}

.dataset-icon {
    font-size: 32px;
    margin-right: 16px;
    color: #409EFF;
}

.dataset-info {
    flex: 1;
}

.dataset-info h4 {
    margin-top: 0;
    margin-bottom: 8px;
}

.dataset-desc {
    font-size: 12px;
    color: #606266;
    margin-bottom: 8px;
    line-height: 1.4;
}

.dataset-info .el-tag {
    margin-right: 5px;
}

.upload-area {
    width: 100%;
    padding: 20px 0;
}

.loading-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.loading-content p {
    margin-top: 16px;
    color: #606266;
}

.uploaded-file-info {
    margin-top: 20px;
}

.dataset-details {
    margin-bottom: 20px;
}

.dataset-details h3 {
    margin-top: 0;
}

.dataset-stats {
    margin-top: 20px;
}

/* Fix for el-upload drag area */
:deep(.el-upload-dragger) {
    width: 100%;
}
</style>