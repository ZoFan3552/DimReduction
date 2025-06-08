<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>1. UMAP简介</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 -->
            <div class="interaction-container" v-if="!isAnswered">
                <h3>理解检查</h3>
                <p>以下哪项最准确地描述了UMAP算法？</p>

                <el-radio-group v-model="selectedAnswer" class="answer-options">
                    <el-radio :label="1">UMAP是一种深度学习算法，需要大量标记数据进行训练</el-radio>
                    <el-radio :label="2">UMAP是一种降维算法，基于流形学习和拓扑数据分析理论</el-radio>
                    <el-radio :label="3">UMAP主要用于数据压缩，但不保留数据间的相似性结构</el-radio>
                    <el-radio :label="4">UMAP是t-SNE的简化版本，计算速度更快但精度较低</el-radio>
                </el-radio-group>

                <el-button type="primary" @click="checkAnswer" :disabled="!selectedAnswer" class="submit-btn">
                    提交答案
                </el-button>
            </div>

            <!-- 回应部分 -->
            <div v-if="isAnswered" class="response-container">
                <el-alert :title="feedbackTitle" :type="isCorrect ? 'success' : 'error'"
                    :description="feedbackDescription" show-icon>
                </el-alert>

                <div v-if="isCorrect" class="next-section">
                    <p>🎉 恭喜！您可以继续学习下一部分。</p>
                    <el-button type="success" @click="goToNextSection">
                        继续学习 <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>

                <div v-else class="retry-section">
                    <el-button type="info" @click="resetAnswer">
                        重新选择
                    </el-button>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { marked } from 'marked';
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
    name: 'Section1Introduction',
    data() {
        return {
            markdownContent: `
  ## UMAP: 统一流形近似和投影
  
  UMAP (Uniform Manifold Approximation and Projection) 是由 Leland McInnes、John Healy 和 James Melville 于2018年提出的一种降维算法。它已经迅速成为数据科学和机器学习领域中最流行的降维技术之一。
  
  ### 什么是UMAP？
  
  UMAP是一种**非线性降维**算法，可以将高维数据投影到低维空间（通常是2D或3D），同时尽可能地保留数据的全局结构和局部关系。与传统的降维方法相比，UMAP具有以下特点：
  
  - **理论基础扎实**：基于黎曼几何和代数拓扑
  - **计算效率高**：比t-SNE等算法更快，可以处理大规模数据集
  - **保留全局结构**：能够更好地保留数据的全局拓扑结构
  - **灵活性强**：有多个可调参数，适应不同类型的数据和任务需求
  
  
  ### UMAP的主要应用
  
  UMAP在多个领域有广泛应用：
  
  1. **数据可视化**：将高维数据投影到2D或3D空间进行可视化
  2. **特征工程**：作为机器学习管道中的预处理步骤
  3. **聚类分析**：辅助发现数据中的自然聚类
  4. **生物信息学**：基因表达数据分析、单细胞RNA测序等
  5. **图像处理**：图像特征降维和可视化
  
  ### UMAP与其他降维方法的比较
  
  UMAP与PCA、t-SNE等降维方法相比：
  
  | 算法 | 计算复杂度 | 保留全局结构 | 保留局部结构 | 应用场景 |
  |------|------------|--------------|--------------|----------|
  | PCA  | 低(O(n²)) | 一般 | 弱 | 线性数据、初步降维 |
  | t-SNE | 高(O(n²)) | 弱 | 强 | 局部结构可视化 |
  | UMAP | 中等(O(n log n)) | 强 | 强 | 综合性数据分析 |
  
  在接下来的教程中，我们将深入探讨UMAP的工作原理、数学基础、参数调整以及实际应用。
        `,
            selectedAnswer: null,
            isAnswered: false,
            isCorrect: false,
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
        },
        feedbackTitle() {
            return this.isCorrect ? '回答正确！' : '回答不正确';
        },
        feedbackDescription() {
            if (this.isCorrect) {
                return 'UMAP确实是一种基于流形学习和拓扑数据分析的降维算法，能够有效保留数据的局部和全局结构。';
            }

            switch (this.selectedAnswer) {
                case 1:
                    return 'UMAP不是深度学习算法，它是一种无监督的降维方法，不需要标记数据。';
                case 3:
                    return 'UMAP不仅仅用于数据压缩，它的主要目标是保留数据间的相似性结构。';
                case 4:
                    return 'UMAP不是t-SNE的简化版，它们基于不同的数学理论，UMAP通常比t-SNE更快且能更好地保留全局结构。';
                default:
                    return '请选择一个选项。';
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(1);
        }
    },
    methods: {
        checkAnswer() {
            this.isAnswered = true;
            this.isCorrect = this.selectedAnswer === 2;

            if (this.isCorrect) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },
        resetAnswer() {
            this.isAnswered = false;
            this.selectedAnswer = null;
        },
        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
            // this.$parent.scrollToSection("2");
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

.markdown-content img {
    max-width: 100%;
    margin: 20px 0;
    border-radius: 5px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.answer-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 15px 0;
}

.submit-btn {
    margin-top: 15px;
}

.response-container {
    margin-top: 20px;
}

.next-section,
.retry-section {
    margin-top: 20px;
    text-align: center;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

th,
td {
    border: 1px solid #dcdfe6;
    padding: 8px 12px;
    text-align: left;
}

th {
    background-color: #f5f7fa;
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

:deep(ul),
:deep(ol) {
    padding-left: 20px;
}

:deep(li) {
    margin: 8px 0;
}
</style>