<!-- IntroductionToLDA.vue - LDA介绍教学组件 -->
<template>
    <div class="tutorial-section" :id="sectionId">
        <div class="section-header">
            <h2 class="section-title">{{ title }}</h2>
            <div class="section-progress">
                <el-tag v-if="isCompleted" type="success" effect="dark">已完成</el-tag>
                <el-tag v-else type="info" effect="plain">进行中</el-tag>
                <div class="section-number">{{ sectionIndex }}/{{ totalSections }}</div>
            </div>
        </div>

        <!-- 教学内容展示区 -->
        <div class="content-area">
            <div class="markdown-content" v-html="compiledMarkdown"></div>
        </div>

        <!-- 互动区域 - 直接集成在组件中 -->
        <div v-if="!isCompleted" class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-s-opportunity"></i> 互动练习：理解LDA的基本概念
            </h3>

            <div class="question">
                <p>LDA（线性判别分析）主要用于哪种机器学习任务？</p>
            </div>

            <el-radio-group v-model="selectedOption" class="options-list" :disabled="answered">
                <el-radio v-for="(option, index) in options" :key="index" :label="index" border class="option-item"
                    :class="{
                        'is-correct': answered && index === correctOption,
                        'is-wrong': answered && selectedOption === index && index !== correctOption
                    }">
                    {{ option }}
                </el-radio>
            </el-radio-group>

            <div class="actions">
                <el-button type="primary" @click="checkAnswer" :disabled="selectedOption === null || answered">
                    提交答案
                </el-button>
            </div>
        </div>

        <!-- 回应区域 - 直接集成在组件中 -->
        <div v-if="showResponse" class="response-area">
            <div class="response-content">
                <i :class="['response-icon', responseIconClass]"></i>
                <div class="response-message" v-html="compiledResponse"></div>
            </div>

            <div class="action-buttons">
                <template v-if="isCorrect">
                    <el-button type="primary" @click="completeSection">
                        继续学习 <i class="el-icon-arrow-right"></i>
                    </el-button>
                </template>
                <template v-else>
                    <el-button type="info" @click="retry">
                        <i class="el-icon-refresh-left"></i> 重试
                    </el-button>
                    <el-button v-if="retryCount >= 2" type="warning" @click="showHint">
                        <i class="el-icon-light-rain"></i> 显示提示
                    </el-button>
                </template>
            </div>
        </div>

        <div v-if="isCompleted" class="completed-message">
            <i class="el-icon-circle-check"></i>
            <span>此部分已完成！</span>
            <el-button v-if="hasNext" type="text" @click="navigateToNext">
                前往下一部分 <i class="el-icon-arrow-right"></i>
            </el-button>
        </div>

        <el-divider></el-divider>
    </div>
</template>

<script>
import { marked } from 'marked';
import 'katex/dist/katex.min.css';
import katex from 'katex';

// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}

export default {
    name: 'IntroductionToLDA',
    props: {
        sectionId: {
            type: String,
            default: 'introduction-to-lda'
        },
        sectionIndex: {
            type: Number,
            required: true
        },
        totalSections: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            title: "LDA介绍",
            markdownContent: `
  # 线性判别分析（LDA）介绍
  
  ## 什么是线性判别分析？
  
  线性判别分析（Linear Discriminant Analysis，简称LDA）是一种经典的有监督降维和分类算法。它最早由英国统计学家Ronald A. Fisher于1936年提出，也被称为Fisher线性判别式。
  
  
  ## LDA的主要功能
  
  LDA 主要有两个功能：
  
  1. **降维**：将高维数据降低到较低维度，同时尽可能保留不同类别之间的可区分性。
  2. **分类**：作为一种分类器，将未知样本分类到已知类别。
  
  ## LDA的基本思想
  
  LDA的核心思想非常直观，它寻求：
  
  - **最大化类间距离** - 不同类别的样本投影后应该尽可能地分离开
  - **最小化类内距离** - 同一类别的样本投影后应该尽可能地靠近
  
  
  这可以形式化表示为寻找一个投影方向 $\\mathbf{w}$，使得投影后的类间散度与类内散度的比值最大化：
  $$J(w) = \\frac{w^T S_B w}{w^T S_W w}$$
  
  其中：
  - $S_B$ 是类间散布矩阵
  - $S_W$ 是类内散布矩阵
  
  ## LDA与PCA的区别
  
  虽然LDA和PCA都是经典的降维方法，但它们的目标有本质区别：
  
  - **PCA**（主成分分析）：无监督方法，寻找数据方差最大的方向
  - **LDA**：有监督方法，寻找最能区分不同类别的方向
  
  ## LDA的应用场景
  
  LDA广泛应用于：
  
  - 人脸识别
  - 图像分类
  - 医学诊断
  - 市场细分
  - 生物特征识别
  - 文本分类
  
  在接下来的教程中，我们将深入探讨LDA的数学原理、算法实现和实际应用。
        `,
            isCompleted: false,
            // 互动部分数据
            selectedOption: null,
            options: [
                "无监督学习与聚类",
                "监督学习与分类/降维",
                "强化学习",
                "生成对抗网络"
            ],
            correctOption: 1,
            answered: false,

            // 回应部分数据
            showResponse: false,
            isCorrect: false,
            response: '',
            retryCount: 0,
            hintShown: false
        }
    },
    computed: {
        compiledMarkdown() {
            const withMath = renderMath(this.markdownContent);
            return marked(withMath);
        },
        compiledResponse() {
            const withMath = renderMath(this.response);
            return marked(withMath);
        },
        responseIconClass() {
            return this.isCorrect ? 'el-icon-check correct' : 'el-icon-close incorrect';
        },
        hasNext() {
            return this.sectionIndex < this.totalSections;
        }
    },
    created() {
        // 检查该部分是否已完成
        const completedSections = this.getCompletedSections();
        this.isCompleted = completedSections.includes(this.sectionId);
    },
    methods: {
        checkAnswer() {
            if (this.selectedOption === null) return;

            this.answered = true;
            this.isCorrect = this.selectedOption === this.correctOption;

            if (this.isCorrect) {
                this.response = `
  ### 🎉 回答正确！
  
  LDA确实主要用于**监督学习与分类/降维**任务。
  
  LDA是一种有监督的算法，它利用已知的类别信息来找到最能区分不同类别的投影方向。作为降维技术，它在保留类别判别信息的同时减少特征空间的维度。
  
  关键点：
  - LDA是**有监督的**，需要样本的标签信息
  - LDA既可以用于降维，也可以用于分类
  - LDA寻找的是能最大化类间散度、最小化类内散度的投影方向
          `;
            } else {
                this.response = `
  ### ❌ 回答不正确
  
  虽然LDA可以用于无监督学习环境中的特殊情况，但它主要是一种**监督学习算法**，为分类和降维而设计。
  
  LDA需要数据的标签信息来寻找能够最大化类间差异和最小化类内差异的投影方向。
  
  请再次尝试！
          `;
                this.retryCount++;
            }

            this.showResponse = true;
        },
        retry() {
            this.showResponse = false;
            this.answered = false;
        },
        showHint() {
            this.hintShown = true;
            this.response = `
  ### 💡 提示
  
  LDA需要使用数据的类别标签信息（即已知每个样本属于哪个类别），它的主要目标是找到一个投影方向，使得投影后的不同类别样本尽可能地分开，而同一类别的样本尽可能地靠近。
  
  思考：哪种学习范式需要使用标签信息？LDA的这种特性更接近于哪种机器学习任务？
        `;
            this.showResponse = true;
        },
        completeSection() {
            this.isCompleted = true;
            this.$emit('complete', this.sectionId);

            // 滚动到下一部分
            if (this.hasNext) {
                this.navigateToNext();
            }
        },
        getCompletedSections() {
            const saved = localStorage.getItem('lda-tutorial-progress');
            if (saved) {
                try {
                    return JSON.parse(saved);
                } catch (e) {
                    console.error('Failed to parse completed sections:', e);
                    return [];
                }
            }
            return [];
        },
        navigateToNext() {
            // 计算下一个部分的ID
            const allSections = this.$parent.sections;
            const currentIndex = allSections.findIndex(s => s.id === this.sectionId);

            if (currentIndex >= 0 && currentIndex < allSections.length - 1) {
                const nextSectionId = allSections[currentIndex + 1].id;
                this.$parent.scrollToSection(nextSectionId);
            }
        }
    }
}
</script>

<style scoped>
.tutorial-section {
    margin-bottom: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.section-title {
    margin: 0;
    color: #303133;
}

.section-progress {
    display: flex;
    align-items: center;
}

.section-number {
    margin-left: 10px;
    font-size: 14px;
    color: #909399;
}

.content-area {
    margin-bottom: 20px;
}

.markdown-content {
    line-height: 1.6;
}

.markdown-content img {
    max-width: 100%;
    border-radius: 4px;
    margin: 10px 0;
}

.markdown-content table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
}

.markdown-content th,
.markdown-content td {
    border: 1px solid #dcdfe6;
    padding: 8px 12px;
    text-align: left;
}

.markdown-content th {
    background-color: #f5f7fa;
}

.markdown-content blockquote {
    border-left: 4px solid #409EFF;
    padding-left: 15px;
    color: #606266;
    background-color: #f8f8f9;
    margin: 15px 0;
    padding: 10px 15px;
    border-radius: 0 4px 4px 0;
}

/* 互动区域样式 */
.interaction-area {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
}

.interaction-title {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    color: #606266;
}

.question {
    margin-bottom: 15px;
}

.question p {
    font-weight: 500;
    margin: 0 0 10px 0;
    line-height: 1.5;
}

.options-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 15px;
}

.option-item {
    width: 100%;
    margin-left: 0 !important;
    margin-right: 0 !important;
    transition: all 0.3s;
}

.option-item.is-correct {
    background-color: rgba(103, 194, 58, 0.1);
    border-color: #67C23A;
}

.option-item.is-wrong {
    background-color: rgba(245, 108, 108, 0.1);
    border-color: #F56C6C;
}

/* 回应区域样式 */
.response-area {
    margin-top: 20px;
    padding: 15px;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
}

.response-content {
    display: flex;
    margin-bottom: 15px;
}

.response-icon {
    font-size: 24px;
    margin-right: 10px;
}

.response-icon.correct {
    color: #67C23A;
}

.response-icon.incorrect {
    color: #F56C6C;
}

.response-message {
    flex: 1;
}

.action-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.completed-message {
    display: flex;
    align-items: center;
    color: #67C23A;
    margin-top: 20px;
}

.completed-message i {
    font-size: 20px;
    margin-right: 8px;
}

/* KaTeX样式调整 */
:deep(.math-block) {
    overflow-x: auto;
    margin: 15px 0;
    padding: 10px;
    background-color: #f8f8f9;
    border-radius: 4px;
}
</style>