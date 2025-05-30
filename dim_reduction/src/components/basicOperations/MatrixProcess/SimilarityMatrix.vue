<template>
    <div class="similarity-calculator-container">
        <el-card class="calculator-card">
            <div slot="header" class="header">
                <h2>相似度矩阵计算</h2>
                <el-tooltip content="通过选择不同的相似度计算公式对数据集进行处理" placement="top">
                    <i class="el-icon-question"></i>
                </el-tooltip>
            </div>

            <el-form ref="form" :model="formData" label-width="120px" label-position="top">
                <el-form label-position="top" label-width="100px">
                    <el-form-item label="选择相似度计算类型">
                        <el-radio-group v-model="similarityType">
                            <el-radio label="high">高维相似度计算</el-radio>
                            <el-radio label="low">低维相似度计算</el-radio>
                        </el-radio-group>
                    </el-form-item>
                </el-form>
                <!-- 选择相似度计算方法 - 平铺展示所有公式 -->
                <el-form-item label="相似度计算公式">
                    <div class="formula-grid">
                        <el-card v-for="(formula, index) in filteredFormulas" :key="formula.name"
                            :class="['formula-card', formData.selectedFormula === formula.name ? 'selected' : '']"
                            shadow="hover" @click.native="selectFormula(formula.name)">
                            <div class="formula-header">
                                <span class="formula-number">公式 {{ index + 1 }}</span>
                                <el-radio v-model="formData.selectedFormula" :label="formula.name"></el-radio>
                            </div>
                            <div class="formula-expression" v-html="formula.expression"></div>
                        </el-card>
                    </div>
                </el-form-item>

                <!-- 动态参数设置区域 -->
                <div v-if="formData.selectedFormula">
                    <h3>参数设置</h3>
                    <el-form-item v-for="param in currentFormulaParams" :key="param.name" :label="param.label">
                        <el-tooltip :content="param.description" placement="right">
                            <el-input-number v-if="param.type === 'number'" v-model="formData.parameters[param.name]"
                                :min="param.min" :max="param.max" :step="param.step" :precision="param.precision || 2">
                            </el-input-number>
                            <el-input v-else-if="param.type === 'text'" v-model="formData.parameters[param.name]">
                            </el-input>
                            <el-select v-else-if="param.type === 'select'" v-model="formData.parameters[param.name]"
                                :placeholder="'请选择' + param.label">
                                <el-option v-for="option in param.options" :key="option.value" :label="option.label"
                                    :value="option.value">
                                </el-option>
                            </el-select>
                        </el-tooltip>
                    </el-form-item>
                </div>

                <!-- 源数据节点信息显示 -->
                <el-form-item label="数据源节点">
                    <el-alert v-if="nodeData" :title="`节点ID: ${nodeData.id}`" type="info" :closable="false" show-icon>
                        <div>
                            操作类型: {{ nodeData.operation }}
                            <div v-if="nodeData.dataset">
                                <el-tag size="mini" type="success">数据量: {{ nodeData.dataset.length || 0 }} 行</el-tag>
                            </div>
                        </div>
                    </el-alert>
                    <el-alert v-else title="暂无源数据节点" type="warning" :closable="false" show-icon>
                        请确保父组件提供了有效的数据节点
                    </el-alert>
                </el-form-item>

                <!-- 提交按钮 -->
                <el-form-item>
                    <el-button type="primary" @click="calculateSimilarity" :loading="loading"
                        :disabled="!formData.selectedFormula || !hasValidSourceData">
                        计算相似度矩阵
                    </el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </el-form>

            <!-- 结果展示区域 -->
            <div v-if="resultNode" class="result-section">
                <el-divider content-position="left">计算结果</el-divider>
                <el-alert title="计算成功" type="success" :closable="false" show-icon>
                    <template slot="title">
                        计算成功: 创建了新的节点 (ID: {{ resultNode.id }})
                    </template>
                    <div>
                        使用公式: {{ getFormulaDisplay(formData.selectedFormula) }}
                        <el-tag size="mini" type="info">相似度矩阵尺寸: {{ matrixSize }}</el-tag>
                    </div>
                </el-alert>

                <!-- 矩阵可视化 -->
                <div class="matrix-visualization">
                    <h4>相似度矩阵可视化:</h4>
                    <div ref="heatmapContainer" class="heatmap-container"></div>
                </div>

                <div class="matrix-preview">
                    <h4>相似度矩阵预览 (前5x5):</h4>
                    <el-table v-if="matrixPreview.length > 0" :data="matrixPreview" border size="mini"
                        class="matrix-table" :show-header="false">
                        <el-table-column v-for="(_, index) in matrixPreview[0]" :key="index" :prop="String(index)"
                            min-width="60">
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import axios from '@/utils/flaskAxios';
import 'katex/dist/katex.min.css';
import katex from 'katex';

export default {
    name: 'SimilarityMatrixCalculator',
    props: {
        // 源数据节点（可能为null）
        nodeData: {
            type: Object,
            default: null
        },
        // 后端API地址
        // apiUrl: {
        //     type: String,
        //     default: 'http://localhost:5000/calculate-similarity'
        // }
    },
    data() {
        return {
            formData: {
                selectedFormula: '',
                parameters: {}
            },
            similarityType: 'high',
            loading: false,
            resultNode: null,
            matrixPreview: [],
            formulas: [
                // 高维相似度计算公式
                {
                    name: 'euclidean',
                    display: '欧几里得相似度',
                    type: 'high',
                    expression: katex.renderToString('s_{ij} = \\exp\\left(-\\frac{\\|x_i - x_j\\|^2}{2\\sigma^2}\\right)', { displayMode: true }),
                    params: [
                        {
                            name: 'sigma',
                            label: '参数 σ',
                            type: 'number',
                            default: 1.0,
                            min: 0.1,
                            max: 10,
                            step: 0.1,
                            precision: 2,
                            description: '控制相似度递减的速率，较大的值使得距离远的点仍具有较高的相似度'
                        }
                    ]
                },
                {
                    name: 'cosine',
                    display: '余弦相似度',
                    type: 'high',
                    expression: katex.renderToString('s_{ij} = \\frac{x_i \\cdot x_j}{\\|x_i\\| \\|x_j\\|}', { displayMode: true }),
                    params: []
                },
                {
                    name: 'gaussian',
                    display: '高斯相似度',
                    type: 'high',
                    expression: katex.renderToString('p_{j|i} = \\frac{\\exp\\left(-\\frac{\\|x_i - x_j\\|^2}{2\\sigma_i^2}\\right)}{\\sum_{k \\neq i}\\exp\\left(-\\frac{\\|x_i - x_k\\|^2}{2\\sigma_i^2}\\right)}', { displayMode: true }),
                    params: [
                        {
                            name: 'perplexity',
                            label: '参数 σ',
                            type: 'number',
                            default: 30,
                            min: 5,
                            max: 100,
                            step: 1,
                            precision: 0,
                            description: '控制局部邻域大小，类似于考虑邻近点的数量'
                        }
                    ]
                },
                {
                    name: 'symmetric_sne',
                    display: '对称SNE相似度',
                    type: 'high',
                    expression: katex.renderToString(`

p_{ij} = \\frac{p_{j|i} + p_{i|j}}{2n}, 
p_{j|i} = \\frac{\\exp\\left(-\\frac{\\|x_i - x_j\\|^2}{2\\sigma_i^2}\\right)}{\\sum_{k \\neq i}\\exp\\left(-\\frac{\\|x_i - x_k\\|^2}{2\\sigma_i^2}\\right)}

`, { displayMode: true }),
                    params: [
                        {
                            name: 'perplexity',
                            label: '参数 σ',
                            type: 'number',
                            default: 30,
                            min: 5,
                            max: 100,
                            step: 1,
                            precision: 0,
                            description: '控制局部邻域大小，类似于考虑邻近点的数量'
                        }
                    ]
                },
                {
                    name: 'umap_high_similarity',
                    display: 'UMAP高维相似度',
                    type: 'high',
                    expression: katex.renderToString(`
\\begin{aligned}
p_{j|i} &= \\exp\\left(-\\frac{d(x_i, x_j) - \\rho_i}{\\sigma_i}\\right), \\\\
P_{ij} &= p_{j|i} + p_{i|j} - p_{j|i} \\cdot p_{i|j}
\\end{aligned}
`, { displayMode: true }),
                    params: [
                        {
                            name: 'n_neighbors',
                            label: '邻居数量 k',
                            type: 'number',
                            default: 15,
                            min: 2,
                            max: 100,
                            step: 1,
                            precision: 0,
                            description: '局部邻域中考虑的点的数量'
                        },
                        {
                            name: 'min_dist',
                            label: '最小距离 δ',
                            type: 'number',
                            default: 0.1,
                            min: 0.0,
                            max: 1.0,
                            step: 0.01,
                            precision: 2,
                            description: '控制相似点之间的最小距离，影响局部结构的保留'
                        }
                    ]
                },
                // 低维相似度计算公式
                {
                    name: 'tsne_low_similarity',
                    display: 't-SNE低维相似度',
                    type: 'low',
                    expression: katex.renderToString('q_{ij} = \\frac{(1 + \\|y_i - y_j\\|^2)^{-1}}{\\sum_{k \\neq l}(1 + \\|y_k - y_l\\|^2)^{-1}}', { displayMode: true }),
                    params: [
                        {
                            name: 'degrees_of_freedom',
                            label: '自由度 ν',
                            type: 'number',
                            default: 1.0,
                            min: 0.1,
                            max: 10,
                            step: 0.1,
                            precision: 1,
                            description: '控制分布的形状，较小的值使得远距离点的排斥力更强'
                        }
                    ]
                },
                {
                    name: 'umap_low_similarity',
                    display: 'UMAP低维相似度',
                    type: 'low',
                    expression: katex.renderToString('q_{ij} = (1 + a \\cdot \\|y_i - y_j\\|^{2b})^{-1}', { displayMode: true }),
                    params: [
                        {
                            name: 'a',
                            label: '参数 a',
                            type: 'number',
                            default: 1.0,
                            min: 0.1,
                            max: 10.0,
                            step: 0.1,
                            precision: 1,
                            description: '控制嵌入分布的形状'
                        },
                        {
                            name: 'b',
                            label: '参数 b',
                            type: 'number',
                            default: 1.0,
                            min: 0.1,
                            max: 2.0,
                            step: 0.1,
                            precision: 1,
                            description: '控制嵌入空间的度量属性'
                        }
                    ]
                }
            ]
        };
    },
    computed: {
        hasValidSourceData() {
            return this.nodeData &&
                this.nodeData.dataset &&
                this.nodeData.dataset.length > 0;
        },
        currentFormulaParams() {
            // 获取当前选择的公式参数
            const formula = this.formulas.find(f => f.name === this.formData.selectedFormula);
            return formula ? formula.params : [];
        },
        matrixSize() {
            if (this.resultNode && this.resultNode.computed) {
                const matrix = this.getComputedMatrix();
                return matrix ? `${matrix.length} × ${matrix[0].length}` : '0 × 0';
            }
            return '0 × 0';
        },
        filteredFormulas() {
            // 根据当前选择的相似度类型过滤公式
            return this.formulas.filter(formula => formula.type === this.similarityType);
        }
    },
    watch: {
        similarityType() {
            // 当相似度类型改变时，重置选择的公式
            this.formData.selectedFormula = '';
            this.formData.parameters = {};
        },
        resultNode: {
            handler() {
                this.$nextTick(() => {
                    if (this.resultNode) {
                        this.renderHeatmap();
                    }
                });
            },
            deep: true
        }
    },
    methods: {
        handleFormulaChange() {
            // 重置参数
            this.formData.parameters = {};

            // 设置默认参数值
            const formula = this.formulas.find(f => f.name === this.formData.selectedFormula);
            if (formula && formula.params) {
                formula.params.forEach(param => {
                    this.$set(this.formData.parameters, param.name, param.default);
                });
            }
        },

        async calculateSimilarity() {
            if (!this.formData.selectedFormula) {
                this.$message.error('请选择相似度计算公式');
                return;
            }

            if (!this.nodeData) {
                this.$message.error('缺少有效的源数据节点');
                return;
            }

            if (!this.nodeData.dataset || this.nodeData.dataset.length === 0) {
                this.$message.error('源数据节点中没有可用的数据集');
                return;
            }

            this.loading = true;

            try {
                // 排除children属性
                // eslint-disable-next-line no-unused-vars
                const { children, ...nodeDataWithoutChildren } = this.nodeData;

                // 准备发送给后端的数据
                const requestData = {
                    source_node: nodeDataWithoutChildren,
                    formula: this.formData.selectedFormula,
                    parameters: this.formData.parameters,
                    similarityType: this.similarityType
                };

                // 发送请求到后端
                const response = await axios.post('/calculate-similarity', requestData);

                // 处理响应
                if (response && response.success) {
                    this.resultNode = response.node;
                    this.prepareMatrixPreview();
                    this.$message.success('相似度矩阵计算成功');
                    this.$emit('applySimilarity', this.resultNode);
                } else {
                    throw new Error(response.message || '计算失败');
                }
            } catch (error) {
                this.$message.error(`计算出错: ${error.message}`);
                console.error('计算相似度矩阵时出错:', error);
            } finally {
                this.loading = false;
            }
        },

        getComputedMatrix() {
            if (!this.resultNode || !this.resultNode.computed) return null;

            // 根据相似度类型获取相应的矩阵
            if (this.similarityType === 'high') {
                return this.resultNode.computed.high_similarity_matrix;
            } else {
                return this.resultNode.computed.low_similarity_matrix;
            }
        },

        prepareMatrixPreview() {
            const matrix = this.getComputedMatrix();
            if (matrix) {
                // 创建前5x5的预览数据
                const previewSize = Math.min(5, matrix.length);
                this.matrixPreview = [];

                for (let i = 0; i < previewSize; i++) {
                    const row = {};
                    for (let j = 0; j < previewSize; j++) {
                        row[j] = matrix[i][j].toFixed(4);
                    }
                    this.matrixPreview.push(row);
                }
            } else {
                this.matrixPreview = [];
            }
        },

        renderHeatmap() {
            // 使用一个简单的热力图可视化相似度矩阵
            const container = this.$refs.heatmapContainer;
            if (!container) return;

            // 清空容器
            container.innerHTML = '';

            const matrix = this.getComputedMatrix();
            if (!matrix || matrix.length === 0) return;

            // 限制可视化的大小，如果矩阵太大，只显示一部分
            const maxSize = 30;  // 最大显示30x30，以避免性能问题
            const displaySize = Math.min(matrix.length, maxSize);

            // 创建热力图
            const heatmapSize = 400;  // 热力图的大小（像素）
            const cellSize = heatmapSize / displaySize;

            // 创建SVG元素
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', heatmapSize);
            svg.setAttribute('height', heatmapSize);

            // 找到最大和最小值，用于颜色映射
            let minVal = 1;
            let maxVal = 0;
            for (let i = 0; i < displaySize; i++) {
                for (let j = 0; j < displaySize; j++) {
                    const val = matrix[i][j];
                    if (val < minVal) minVal = val;
                    if (val > maxVal) maxVal = val;
                }
            }

            // 创建热力图单元格
            for (let i = 0; i < displaySize; i++) {
                for (let j = 0; j < displaySize; j++) {
                    const val = matrix[i][j];
                    // 将值映射到0-1之间
                    const normalizedVal = (val - minVal) / (maxVal - minVal);

                    // 创建一个矩形
                    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                    rect.setAttribute('x', j * cellSize);
                    rect.setAttribute('y', i * cellSize);
                    rect.setAttribute('width', cellSize);
                    rect.setAttribute('height', cellSize);

                    // 值越高，颜色越深
                    const hue = 240 - normalizedVal * 240;  // 从蓝色(240)到红色(0)
                    rect.setAttribute('fill', `hsl(${hue}, 100%, 50%)`);

                    // 添加鼠标悬停效果显示值
                    rect.setAttribute('data-value', val.toFixed(4));
                    rect.addEventListener('mouseover', (e) => {
                        const tooltip = document.createElement('div');
                        tooltip.className = 'matrix-tooltip';
                        tooltip.innerText = `(${i},${j}): ${e.target.getAttribute('data-value')}`;
                        tooltip.style.position = 'absolute';
                        tooltip.style.left = `${e.pageX + 10}px`;
                        tooltip.style.top = `${e.pageY + 10}px`;
                        tooltip.style.backgroundColor = 'rgba(0,0,0,0.7)';
                        tooltip.style.color = 'white';
                        tooltip.style.padding = '5px';
                        tooltip.style.borderRadius = '3px';
                        tooltip.style.zIndex = '1000';
                        document.body.appendChild(tooltip);

                        e.target.addEventListener('mouseout', () => {
                            document.body.removeChild(tooltip);
                        }, { once: true });
                    });

                    svg.appendChild(rect);
                }
            }

            // 添加图例
            const legendWidth = 20;
            const legendHeight = heatmapSize;
            // const legendX = heatmapSize + 20;

            const legendSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            legendSvg.setAttribute('width', legendWidth + 50);
            legendSvg.setAttribute('height', legendHeight);

            // 创建渐变色图例
            for (let i = 0; i < legendHeight; i++) {
                const normalizedVal = 1 - (i / legendHeight);
                const hue = 240 - normalizedVal * 240;

                const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                rect.setAttribute('x', 0);
                rect.setAttribute('y', i);
                rect.setAttribute('width', legendWidth);
                rect.setAttribute('height', 1);
                rect.setAttribute('fill', `hsl(${hue}, 100%, 50%)`);

                legendSvg.appendChild(rect);
            }

            // 添加图例标签
            const textMax = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            textMax.setAttribute('x', legendWidth + 5);
            textMax.setAttribute('y', 10);
            textMax.textContent = maxVal.toFixed(2);
            legendSvg.appendChild(textMax);

            const textMin = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            textMin.setAttribute('x', legendWidth + 5);
            textMin.setAttribute('y', legendHeight - 5);
            textMin.textContent = minVal.toFixed(2);
            legendSvg.appendChild(textMin);

            // 将SVG添加到容器
            container.appendChild(svg);
            container.appendChild(legendSvg);
        },

        resetForm() {
            this.formData = {
                selectedFormula: '',
                parameters: {}
            };
            this.resultNode = null;
            this.matrixPreview = [];
        },

        selectFormula(formulaName) {
            this.formData.selectedFormula = formulaName;
            this.handleFormulaChange();
        },

        getFormulaDisplay(formulaName) {
            const formula = this.formulas.find(f => f.name === formulaName);
            return formula ? formula.display : formulaName;
        }
    }
};
</script>

<style scoped>
.similarity-calculator-container {
    max-width: 1000px;
    margin: 0 auto;
}

.calculator-card {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header h2 {
    margin: 0;
    font-size: 1.5rem;
    color: #409EFF;
}

/* 公式卡片网格布局 */
.formula-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.formula-card {
    border: 1px solid #EBEEF5;
    cursor: pointer;
    transition: all 0.3s;
}

.formula-card.selected {
    border: 2px solid #409EFF;
    box-shadow: 0 0 10px rgba(64, 158, 255, 0.2);
}

.formula-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1px dashed #EBEEF5;
}

.formula-number {
    font-weight: bold;
    color: #409EFF;
    font-size: 16px;
}

.formula-expression {
    padding: 15px 5px;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f8f8f8;
    border-radius: 4px;
}

.result-section {
    margin-top: 20px;
}

.matrix-preview {
    margin-top: 15px;
    background: #f9f9f9;
    border-radius: 4px;
    padding: 10px;
}

.matrix-table {
    width: 100%;
    max-width: 400px;
    margin-top: 10px;
}

.el-divider__text {
    font-weight: bold;
    color: #409EFF;
}

.matrix-visualization {
    margin-top: 15px;
    background: #f9f9f9;
    border-radius: 4px;
    padding: 10px;
}

.heatmap-container {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-top: 15px;
    overflow-x: auto;
    padding: 10px;
}
</style>