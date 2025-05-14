<template>
    <div class="lesson-container">
        <!-- Markdown展示部分 -->
        <div class="content-section">
            <el-card class="markdown-content">
                <div v-html="renderedMarkdown"></div>
            </el-card>
        </div>

        <!-- 互动部分 -->
        <div v-if="!isCompleted" class="interactive-section">
            <el-card>
                <h3>思考一下</h3>
                <p>在实际应用中，为什么我们需要降维技术？（可多选）</p>
                <el-checkbox-group v-model="userAnswer">
                    <el-checkbox label="visualization">数据可视化</el-checkbox>
                    <el-checkbox label="computation">减少计算量</el-checkbox>
                    <el-checkbox label="noise">减少噪声</el-checkbox>
                    <el-checkbox label="patterns">发现潜在模式</el-checkbox>
                </el-checkbox-group>
                <div class="action-buttons">
                    <el-button type="primary" @click="checkAnswer">提交答案</el-button>
                </div>
            </el-card>
        </div>

        <!-- 回应部分 -->
        <div v-if="showResponse" class="response-section">
            <el-card :class="{ 'correct-answer': isCorrect, 'wrong-answer': !isCorrect }">
                <div v-if="isCorrect">
                    <h3><i class="el-icon-success"></i> 回答正确!</h3>
                    <p>是的，降维的主要应用包括：</p>
                    <ul>
                        <li><strong>数据可视化</strong>：高维数据很难直观地观察，降维到2D或3D空间可以帮助我们可视化数据</li>
                        <li><strong>减少计算量</strong>：降低维度可以减少后续分析中的计算复杂度</li>
                        <li><strong>去除噪声</strong>：许多降维方法能去除数据中的噪声，突出主要特征</li>
                        <li><strong>发现潜在模式</strong>：降维有助于发现数据中的隐藏结构和模式</li>
                    </ul>
                    <el-button type="success" @click="proceedToNext">继续学习</el-button>
                </div>
                <div v-else>
                    <h3><i class="el-icon-error"></i> 再想想...</h3>
                    <p>降维技术在数据科学中有几个关键应用，请再考虑一下所有可能的用途。</p>
                    <el-button @click="resetAnswer">重新选择</el-button>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
import { marked } from 'marked';
import 'katex/dist/katex.min.css';


export default {
    name: 'Lesson1Introduction',
    props: {
        isCompleted: {
            type: Boolean,
            default: false
        },
        userAnswers: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            markdown: `
  # t-SNE降维算法介绍
  
  **t-分布随机邻域嵌入**（t-distributed Stochastic Neighbor Embedding，t-SNE）是一种非线性降维算法，特别适合高维数据可视化。
  
  ## 什么是降维？
  
  当我们分析现实世界的数据时，通常会面对大量的特征或维度。例如：
  - 一张64×64像素的灰度图像实际上是一个4096维的数据点
  - 一个基因表达数据集可能包含数万个基因的表达水平
  
  想象一下，你如何在脑海中可视化一个4096维的空间？这是人类无法做到的！
  
  而降维算法就是将这些高维数据映射到低维空间（通常是2D或3D）的技术，同时保留数据中最重要的关系或特征。
  
  
  ## 为什么t-SNE如此特别？
  
  与其他降维技术相比，t-SNE的主要优势在于它能够**保留数据的局部结构**。这意味着：
  - 原始空间中相似的数据点在降维后的空间中仍然相似
  - 可以有效地揭示数据中的聚类结构
  
  这使得t-SNE成为数据可视化和探索的强大工具。
        `,
            userAnswer: [],
            showResponse: false,
            isCorrect: false,
            correctAnswers: ['visualization', 'computation', 'noise', 'patterns']
        };
    },
    computed: {
        renderedMarkdown() {
            // 将多行字符串的缩进去掉，并确保正确处理
            try {
                // 确保this.markdown存在

                return marked(this.markdown);
            } catch (error) {
                console.error('Marked parsing error:', error);
                return '<p>无法渲染Markdown内容</p>';
            }


        }
    },
    mounted() {
        // 如果已经完成，使用保存的答案
        if (this.isCompleted && this.userAnswers) {
            this.userAnswer = this.userAnswers;
            this.showResponse = true;
            this.isCorrect = true;
        }
    },
    methods: {
        checkAnswer() {
            // 检查是否选择了所有正确答案
            this.isCorrect = this.correctAnswers.every(answer =>
                this.userAnswer.includes(answer)
            ) && this.userAnswer.length === this.correctAnswers.length;

            this.showResponse = true;
        },
        resetAnswer() {
            this.showResponse = false;
            this.userAnswer = [];
        },
        proceedToNext() {
            this.$emit('lesson-completed', true);
            this.$emit('user-response', this.userAnswer);
        }
    }
};
</script>

<style scoped>
.lesson-container {
    margin-bottom: 30px;
}

.content-section,
.interactive-section,
.response-section {
    margin-bottom: 20px;
}

.markdown-content {
    line-height: 1.6;
}

.markdown-content>>>img {
    max-width: 100%;
    display: block;
    margin: 20px auto;
}

.action-buttons {
    margin-top: 20px;
}

.correct-answer {
    background-color: #f0f9eb;
}

.wrong-answer {
    background-color: #fef0f0;
}
</style>