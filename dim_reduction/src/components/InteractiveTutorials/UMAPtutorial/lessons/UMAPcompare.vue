<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>8. UMAP与其他降维算法比较</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 算法比较可视化 -->
            <div class="interaction-container">


                <div class="algorithm-comparison">
                    <h4>算法比较分析</h4>
                    <p>不同算法在处理上述数据集时各有优劣：</p>
                    <el-table :data="comparisonData" style="width: 100%" border>
                        <el-table-column prop="aspect" label="比较方面" width="180"></el-table-column>
                        <el-table-column prop="pca" label="PCA"></el-table-column>
                        <el-table-column prop="tsne" label="t-SNE"></el-table-column>
                        <el-table-column prop="umap" label="UMAP"></el-table-column>
                    </el-table>
                </div>

                <!-- 互动测验 -->
                <div class="quiz-container" v-if="!quizCompleted">
                    <h4>算法选择测验</h4>
                    <p>基于您对不同算法的观察，回答以下问题：</p>

                    <div class="questions">
                        <div class="question" v-for="(q, index) in questions" :key="index">
                            <p><strong>{{ index + 1 }}. {{ q.text }}</strong></p>
                            <el-radio-group v-model="userAnswers[index]">
                                <el-radio v-for="(option, optIndex) in q.options" :key="optIndex" :label="optIndex"
                                    class="option-radio">
                                    {{ option }}
                                </el-radio>
                            </el-radio-group>
                        </div>
                    </div>

                    <el-button type="primary" @click="checkAnswers" :disabled="!isAllAnswered" class="submit-btn">
                        提交答案
                    </el-button>
                </div>

                <!-- 回应部分 -->
                <div v-if="quizCompleted" class="response-container">
                    <el-alert :title="quizFeedbackTitle" :type="allCorrect ? 'success' : 'info'"
                        :description="quizFeedbackDescription" show-icon>
                    </el-alert>

                    <div v-if="!allCorrect" class="quiz-results">
                        <h4>测验结果:</h4>
                        <div v-for="(question, index) in questions" :key="index" class="question-result">
                            <p>
                                <strong>{{ index + 1 }}. {{ question.text }}</strong>
                                <el-tag size="small" :type="questionResults[index] ? 'success' : 'danger'">
                                    {{ questionResults[index] ? '正确' : '错误' }}
                                </el-tag>
                            </p>
                            <p v-if="!questionResults[index]" class="explanation">
                                正确答案: {{ question.options[question.answer] }}<br>
                                解释: {{ question.explanation }}
                            </p>
                        </div>

                        <el-button type="info" @click="resetQuiz" class="retry-btn">
                            重新作答
                        </el-button>
                    </div>

                    <div v-if="allCorrect || retries >= 1" class="next-section">
                        <p>🎉 您已完成UMAP与其他算法比较部分！可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { marked } from 'marked';
// import * as d3 from 'd3';

// 设置渲染器以支持数学公式
import 'katex/dist/katex.min.css';
// import katex from 'katex';
import katex from 'katex';
// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}


export default {
    name: 'Section8Comparison',
    data() {
        return {
            markdownContent: `
  ## UMAP与其他降维算法比较
  
  在机器学习和数据可视化领域，有多种降维算法可供选择。理解UMAP与其他常用算法的异同对于选择合适的工具至关重要。本节我们将UMAP与几种主流降维算法进行比较，重点关注它们的理论基础、性能特点和适用场景。
  
  ### 主要降维算法概述
  
  #### 1. PCA (Principal Component Analysis)
  
  **原理**：PCA寻找数据方差最大的方向（主成分），然后将数据投影到这些方向上。它是一种线性降维方法。
  
  **优点**：
  - 计算效率高，扩展性好
  - 解释性强，每个主成分有明确的方差解释比例
  - 不需要调参，结果确定性强
  
  **局限性**：
  - 只能捕捉线性关系，对非线性结构表现不佳
  - 对异常值敏感
  - 难以保留局部结构
  
  #### 2. t-SNE (t-Distributed Stochastic Neighbor Embedding)
  
  **原理**：t-SNE在高维和低维空间中建立点之间的条件概率分布，并最小化这两个分布的KL散度。它使用t分布来避免"拥挤问题"。
  
  **优点**：
  - 擅长保留局部结构和发现聚类
  - 产生视觉上令人满意的结果，适合可视化
  - 处理非线性关系表现优异
  
  **局限性**：
  - 计算成本高，难以处理大型数据集
  - 不擅长保留全局结构
  - 对参数（尤其是困惑度perplexity）敏感
  - 结果依赖于初始化和随机种子
  
  #### 3. UMAP (Uniform Manifold Approximation and Projection)
  
  **原理**：UMAP基于黎曼几何和拓扑学，构建数据的高维表示，然后优化低维表示以保留这种拓扑结构。
  
  **优点**：
  - 比t-SNE更好地保留全局结构
  - 计算效率高于t-SNE，可以处理更大的数据集
  - 理论基础扎实
  - 支持监督、半监督和无监督模式
  
  **局限性**：
  - 多个参数需要调整
  - 结果可能因随机种子而异
  - 在某些极端数据上可能表现不稳定
  
  #### 4. Isomap
  
  **原理**：Isomap估计数据点之间的测地线距离（流形上的最短路径），然后应用多维缩放(MDS)进行降维。
  
  **优点**：
  - 擅长处理流形上的数据
  - 明确保留全局结构
  - 在某些非线性结构上表现优异
  
  **局限性**：
  - 计算复杂度高
  - 对噪声和"短路"问题敏感
  - 依赖于正确的邻域图构建
  
  #### 5. LLE (Locally Linear Embedding)
  
  **原理**：LLE假设每个数据点可以表示为其邻居的线性组合，并尝试在低维空间中保留这种关系。
  
  **优点**：
  - 保留局部几何结构
  - 对连续流形表现良好
  - 参数较少
  
  **局限性**：
  - 难以处理非均匀采样的数据
  - 对噪声敏感
  - 不适合具有孔洞的流形
  
  ### UMAP与t-SNE的关键区别
  
  UMAP和t-SNE是目前最流行的非线性降维可视化方法，它们有一些重要区别：
  
  1. **理论基础**
     - t-SNE: 基于概率论和KL散度最小化
     - UMAP: 基于黎曼几何、代数拓扑和流形学习
  
  2. **计算效率**
     - t-SNE: 计算复杂度为O(n²)
     - UMAP: 计算复杂度为O(n log n)，大数据集上明显更快
  
  3. **全局结构保留**
     - t-SNE: 主要关注局部结构，全局结构保留较差
     - UMAP: 能更好地平衡局部和全局结构的保留
  
  4. **参数灵活性**
     - t-SNE: 主要参数是perplexity，影响结果的局部性
     - UMAP: 有多个可调参数，提供更多灵活性
  
  5. **扩展性**
     - t-SNE: 对新数据点的映射需要重新训练
     - UMAP: 支持将模型应用于新数据（transform方法）
  
  ### 不同数据类型的适用场景
  
  不同的降维算法在不同类型的数据上表现各异：
  
  1. **高维表格数据**
     - 快速概览: PCA
     - 详细结构探索: UMAP
     - 聚类可视化: t-SNE或UMAP
  
  2. **图像数据**
     - 一般特征提取: PCA
     - 模式识别和可视化: UMAP
  
  3. **文本数据**
     - 主题建模: PCA或NMF
     - 文档聚类可视化: UMAP
  
  4. **时间序列数据**
     - 趋势分析: PCA
     - 模式可视化: UMAP
  
  5. **生物信息学数据**
     - 基因表达分析: PCA初步探索，UMAP深入分析
     - 单细胞数据: UMAP
  
  ### 实际使用建议
  
  在实践中选择降维算法时，可以考虑以下因素：
  
  1. **数据规模**
     - 大数据集 (>10000点): PCA或UMAP
     - 中等数据集: 任何算法都可以，但UMAP通常是最佳平衡
     - 小数据集: 可以尝试多种算法比较
  
  2. **分析目标**
     - 快速探索: PCA
     - 聚类识别: t-SNE或UMAP
     - 全局结构保留: UMAP或Isomap
     - 特征降维作为预处理: PCA或UMAP
  
  3. **计算资源**
     - 有限的计算资源: PCA
     - 中等计算资源: UMAP
     - 充足的计算资源: 可以尝试多种算法
  
  在下面的互动演示中，您可以比较不同降维算法在各种数据集上的表现，深入理解它们的优势和局限性。
        `,
            selectedDataset: 'mnist',
            algorithms: [],
            comparisonData: [
                {
                    aspect: '计算效率',
                    pca: '高 O(n²)',
                    tsne: '低 O(n²)',
                    umap: '中 O(n log n)'
                },
                {
                    aspect: '保留局部结构',
                    pca: '弱',
                    tsne: '强',
                    umap: '强'
                },
                {
                    aspect: '保留全局结构',
                    pca: '中等',
                    tsne: '弱',
                    umap: '强'
                },
                {
                    aspect: '处理大型数据集',
                    pca: '适合',
                    tsne: '困难',
                    umap: '适合'
                },
                {
                    aspect: '易于调参',
                    pca: '无需调参',
                    tsne: '需要调整perplexity',
                    umap: '多参数需调整'
                }
            ],
            questions: [
                {
                    text: '在需要保留数据全局结构的情况下，以下哪种算法最合适？',
                    options: [
                        'PCA',
                        't-SNE',
                        'UMAP',
                        'K-means'
                    ],
                    answer: 2,
                    explanation: 'UMAP优于t-SNE的一个主要优势是它能更好地保留数据的全局结构，同时仍然很好地保留局部关系。'
                },
                {
                    text: '对于具有100万样本的大型数据集，以下哪种算法在计算效率上最高？',
                    options: [
                        'UMAP',
                        't-SNE',
                        'Isomap',
                        'LLE'
                    ],
                    answer: 0,
                    explanation: 'UMAP的计算复杂度为O(n log n)，比t-SNE、Isomap和LLE都更适合处理大型数据集。'
                },
                {
                    text: '以下哪种算法是线性降维方法？',
                    options: [
                        'UMAP',
                        't-SNE',
                        'PCA',
                        'LLE'
                    ],
                    answer: 2,
                    explanation: 'PCA是线性降维方法，它通过找到数据方差最大的方向进行投影。而UMAP、t-SNE和LLE都是非线性降维方法。'
                }
            ],
            userAnswers: [],
            questionResults: [],
            quizCompleted: false,
            allCorrect: false,
            retries: 0,
            datasets: {},
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
const withMath = renderMath(this.markdownContent)
            return marked(withMath)        },
        isAllAnswered() {
            return this.userAnswers.length === this.questions.length &&
                !this.userAnswers.includes(undefined);
        },
        quizFeedbackTitle() {
            return this.allCorrect ? '恭喜！所有问题回答正确！' : '测验完成';
        },
        quizFeedbackDescription() {
            if (this.allCorrect) {
                return '您已经很好地理解了不同降维算法的特点和适用场景。';
            } else {
                const correctCount = this.questionResults.filter(result => result).length;
                return `您答对了${correctCount}道题目（共${this.questions.length}题）。请查看下方的详细解释。`;
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(8);
        }

        // 生成示例数据集
        this.generateDatasets();

        // 初始化可视化
        this.$nextTick(() => {
            this.updateVisualizations();
        });
    },
    methods: {
        //该函数无用处
        generateDatasets() {


        },

        updateAlgorithmStats() {

        },

        updateVisualizations() {

        },

        createAlgorithmVisualization() {

        },

        getDatasetTitle() {

        },

        checkAnswers() {
            this.quizCompleted = true;
            this.questionResults = this.questions.map(
                (q, i) => this.userAnswers[i] === q.answer
            );
            this.allCorrect = this.questionResults.every(result => result);

            if (this.allCorrect || ++this.retries >= 1) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },

        resetQuiz() {
            this.quizCompleted = false;
            this.userAnswers = [];
            this.questionResults = [];
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    }
}
</script>

<style scoped>
.section-container {
    margin-bottom: 40px;
}

.section-card {
    margin-bottom: 20px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.markdown-content {
    margin-bottom: 30px;
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.dataset-selector {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.dataset-selector span {
    font-weight: bold;
}

.algorithm-visualizations {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 20px 0;
}

.algorithm-panel {
    flex: 1;
    min-width: 300px;
    max-width: 400px;
    background-color: white;
    border-radius: 4px;
    padding: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.algorithm-panel h4 {
    text-align: center;
    margin-top: 0;
    margin-bottom: 15px;
    color: #409EFF;
}

.viz-container {
    width: 100%;
    height: 250px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
}

.algorithm-stats {
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px dashed #dcdfe6;
}

.algorithm-stats p {
    margin: 5px 0;
    font-size: 0.9rem;
}

.algorithm-comparison {
    margin: 30px 0;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.algorithm-comparison h4 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #409EFF;
}

.quiz-container {
    margin-top: 30px;
    padding: 15px;
    border-top: 1px dashed #dcdfe6;
}

.questions {
    margin-top: 20px;
}

.question {
    margin-bottom: 25px;
}

.option-radio {
    display: block;
    margin: 10px 0 10px 20px;
}

.submit-btn {
    margin-top: 15px;
}

.response-container {
    margin-top: 20px;
}

.quiz-results {
    margin-top: 20px;
    padding: 15px;
    background-color: #f2f6fc;
    border-radius: 4px;
}

.question-result {
    margin-bottom: 15px;
}

.explanation {
    margin-top: 5px;
    margin-left: 20px;
    color: #606266;
    font-size: 0.9rem;
}

.retry-btn {
    margin-top: 15px;
}

.next-section {
    margin-top: 20px;
    text-align: center;
}

/* 全局样式适配 */
:deep(h2) {
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    margin-top: 20px;
}

:deep(blockquote) {
    border-left: 4px solid #409EFF;
    padding-left: 15px;
    color: #606266;
    margin: 20px 0;
}

:deep(p) {
    line-height: 1.6;
}

:deep(strong) {
    color: #409EFF;
}

:deep(ul),
:deep(ol) {
    padding-left: 20px;
    line-height: 1.6;
}
</style>