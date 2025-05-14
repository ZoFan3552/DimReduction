<!-- LDAMathematicalFoundation.vue - LDA数学基础教学组件 -->
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

        <!-- 互动区域 - 数学公式匹配 -->
        <div class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-edit"></i> 互动练习：匹配LDA关键数学公式
            </h3>

            <p class="interaction-description">
                将右侧的公式描述与左侧的数学公式进行匹配。
            </p>

            <div class="matching-exercise">
                <div class="formulas-container">
                    <div v-for="(formula, index) in formulas" :key="'formula-' + index" class="formula-item"
                        :class="{ 'selected': selectedFormula === index }" @click="selectFormula(index)">
                        <div class="formula-content" v-html="formula.rendered"></div>
                        <div class="formula-label">公式 {{ index + 1 }}</div>
                    </div>
                </div>

                <div class="arrow-container">
                    <i class="el-icon-right"></i>
                </div>

                <div class="descriptions-container">
                    <div v-for="(description, index) in descriptions" :key="'desc-' + index" class="description-item"
                        :class="{
                            'selected': selectedDescription === index,
                            'matched': matchedDescriptions.includes(index),
                            'correct-match': checkMatchStatus(index) === 'correct',
                            'wrong-match': checkMatchStatus(index) === 'wrong'
                        }" @click="selectDescription(index)">
                        <div class="description-content">{{ description.text }}</div>
                        <div class="description-label">描述 {{ index + 1 }}</div>
                        <div v-if="matchedDescriptions.includes(index)" class="match-info">
                            已匹配到: 公式 {{ getMatchedFormulaIndex(index) + 1 }}
                            <i v-if="checkMatchStatus(index) === 'correct'"
                                class="el-icon-check match-icon correct"></i>
                            <i v-if="checkMatchStatus(index) === 'wrong'" class="el-icon-close match-icon wrong"></i>
                        </div>
                    </div>
                </div>
            </div>

            <div class="matching-controls">
                <el-button type="primary" @click="createMatch"
                    :disabled="selectedFormula === null || selectedDescription === null || matchedDescriptions.includes(selectedDescription)">
                    创建匹配
                </el-button>

                <el-button type="danger" @click="resetMatch" :disabled="matches.length === 0">
                    重置匹配
                </el-button>

                <el-button type="success" @click="checkAllMatches" :disabled="matches.length < formulas.length">
                    检查答案
                </el-button>
            </div>
        </div>

        <!-- 回应区域 -->
        <div v-if="showResponse" class="response-area">
            <div class="response-content">
                <i :class="['response-icon', responseIconClass]"></i>
                <div class="response-message" v-html="compiledResponse"></div>
            </div>

            <div class="action-buttons">
                <el-button v-if="allCorrect" type="primary" @click="completeSection">
                    继续学习 <i class="el-icon-arrow-right"></i>
                </el-button>
                <el-button v-else type="info" @click="resetMatchAndHideResponse">
                    重新尝试 <i class="el-icon-refresh"></i>
                </el-button>
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
    name: 'LDAMathematicalFoundation',
    props: {
        sectionId: {
            type: String,
            default: 'lda-mathematical-foundation'
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
            title: "LDA数学基础",
            markdownContent: `
# LDA的数学基础

线性判别分析(LDA)是一种强大的降维和分类算法，它的数学原理非常优雅，涉及到线性代数和统计学的概念。

## 问题设定

假设我们有一个包含 $n$ 个样本的数据集 $X$，每个样本有 $d$ 个特征。这些样本分属于 $k$ 个不同的类别。

LDA的目标是找到一个投影矩阵 $W$，将原始的 $d$ 维特征空间投影到一个较低维度（通常是 $k-1$ 维）的空间，同时：
1. 最大化不同类别之间的距离 (类间散度)
2. 最小化每个类别内部样本之间的距离 (类内散度)

## 关键数学概念

LDA算法的核心涉及以下数学概念：

### 1. 类均值向量

对于每个类别 $c$，其均值向量定义为：

$$
\\mu_c = \\frac{1}{n_c} \\sum_{i \\in c} x_i
$$

其中 $n_c$ 是类别 $c$ 中的样本数量，$x_i$ 是类别 $c$ 中的一个样本。

全局均值向量定义为：

$$
\\mu = \\frac{1}{n} \\sum_{i=1}^{n} x_i
$$

### 2. 散布矩阵

LDA使用三种散布矩阵来量化数据分布：

**类内散布矩阵** $S_W$ (Within-class scatter matrix)：
$$
S_W = \\sum_{c=1}^{k} \\sum_{i \\in c} (x_i - \\mu_c)(x_i - \\mu_c)^T
$$

**类间散布矩阵** $S_B$ (Between-class scatter matrix)：
$$
S_B = \\sum_{c=1}^{k} n_c (\\mu_c - \\mu)(\\mu_c - \\mu)^T
$$

**总散布矩阵** $S_T$ (Total scatter matrix)：
$$
S_T = \\sum_{i=1}^{n} (x_i - \\mu)(x_i - \\mu)^T = S_W + S_B
$$

### 3. Fisher准则

LDA的优化目标可以用Fisher判别准则表示，即最大化：

$$
J(W) = \\frac{W^T S_B W}{W^T S_W W}
$$

这个比率代表"类间散度"与"类内散度"的比值。我们希望找到一个投影方向 $W$，使得投影后，不同类别之间尽可能分开（$W^T S_B W$ 大），而同一类别内的样本尽可能聚集（$W^T S_W W$ 小）。

### 4. 求解方法

可以证明，最优的投影方向 $W$ 是 $S_W^{-1}S_B$ 的特征向量，对应于其最大的 $k-1$ 个特征值。

这可以表示为求解广义特征值问题：

$$
S_B w = \\lambda S_W w
$$

或等价地：

$$
S_W^{-1} S_B w = \\lambda w
$$

其中 $\\lambda$ 是特征值，$w$ 是对应的特征向量。

## 二分类情况的简化

当只有两个类别时，LDA尤其简单。最优的投影方向为：

$$
w = S_W^{-1}(\\mu_1 - \\mu_2)
$$

也就是说，投影方向与两类均值的差向量在类内散布矩阵的"度量"下的方向一致。

在接下来的部分，我们将详细探讨散布矩阵的计算以及LDA的实现步骤。
      `,
            isCompleted: false,

            // 互动部分数据
            formulas: [
                {
                    latex: "\\mu_c = \\frac{1}{n_c} \\sum_{i \\in c} x_i",
                    rendered: null,
                    description: "类均值向量",
                    descriptionIndex: 0
                },
                {
                    latex: "S_W = \\sum_{c=1}^{k} \\sum_{i \\in c} (x_i - \\mu_c)(x_i - \\mu_c)^T",
                    rendered: null,
                    description: "类内散布矩阵",
                    descriptionIndex: 2
                },
                {
                    latex: "S_B = \\sum_{c=1}^{k} n_c (\\mu_c - \\mu)(\\mu_c - \\mu)^T",
                    rendered: null,
                    description: "类间散布矩阵",
                    descriptionIndex: 3
                },
                {
                    latex: "J(W) = \\frac{W^T S_B W}{W^T S_W W}",
                    rendered: null,
                    description: "Fisher准则",
                    descriptionIndex: 1
                },
                {
                    latex: "S_B w = \\lambda S_W w",
                    rendered: null,
                    description: "广义特征值问题",
                    descriptionIndex: 4
                }
            ],
            descriptions: [
                {
                    text: "表示每个类别中所有样本的平均值，是计算散布矩阵的基础",
                    correctFormulaIndex: 0
                },
                {
                    text: "LDA的优化目标，即最大化类间散度与类内散度的比值",
                    correctFormulaIndex: 3
                },
                {
                    text: "度量同一类别内样本的分散程度，我们希望它尽可能小",
                    correctFormulaIndex: 1
                },
                {
                    text: "度量不同类别之间的分离程度，我们希望它尽可能大",
                    correctFormulaIndex: 2
                },
                {
                    text: "求解最优投影方向的数学方程，其解是S_W^{-1}S_B的特征向量",
                    correctFormulaIndex: 4
                }
            ],
            selectedFormula: null,
            selectedDescription: null,
            matches: [], // 格式: {formulaIndex, descriptionIndex}
            matchedDescriptions: [],
            matchResults: [], // 格式: {descriptionIndex, isCorrect}

            // 回应部分数据
            showResponse: false,
            allCorrect: false,
            response: ''
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
            return this.allCorrect ? 'el-icon-check correct' : 'el-icon-close incorrect';
        },
        hasNext() {
            return this.sectionIndex < this.totalSections;
        }
    },
    created() {
        // 检查该部分是否已完成
        const completedSections = this.getCompletedSections();
        this.isCompleted = completedSections.includes(this.sectionId);

        // 渲染公式
        this.formulas.forEach((formula, index) => {
            try {
                this.formulas[index].rendered = katex.renderToString(formula.latex, {
                    displayMode: true,
                    throwOnError: false
                });
            } catch (e) {
                console.error('KaTeX rendering error:', e);
                this.formulas[index].rendered = `<pre>Error rendering formula: ${e.message}</pre>`;
            }
        });
    },
    methods: {
        selectFormula(index) {
            this.selectedFormula = index;
        },

        selectDescription(index) {
            if (!this.matchedDescriptions.includes(index)) {
                this.selectedDescription = index;
            }
        },

        createMatch() {
            if (this.selectedFormula === null || this.selectedDescription === null) {
                return;
            }

            // 创建匹配
            this.matches.push({
                formulaIndex: this.selectedFormula,
                descriptionIndex: this.selectedDescription
            });

            this.matchedDescriptions.push(this.selectedDescription);

            // 重置选择
            this.selectedFormula = null;
            this.selectedDescription = null;
        },

        resetMatch() {
            this.matches = [];
            this.matchedDescriptions = [];
            this.matchResults = [];
            this.selectedFormula = null;
            this.selectedDescription = null;
        },

        resetMatchAndHideResponse() {
            this.resetMatch();
            this.showResponse = false;
        },

        getMatchedFormulaIndex(descriptionIndex) {
            const match = this.matches.find(m => m.descriptionIndex === descriptionIndex);
            return match ? match.formulaIndex : -1;
        },

        checkMatchStatus(descriptionIndex) {
            const result = this.matchResults.find(r => r.descriptionIndex === descriptionIndex);
            if (!result) return null;
            return result.isCorrect ? 'correct' : 'wrong';
        },

        checkAllMatches() {
            // 检查所有匹配是否正确
            this.matchResults = this.matches.map(match => {
                const description = this.descriptions[match.descriptionIndex];
                return {
                    descriptionIndex: match.descriptionIndex,
                    isCorrect: description.correctFormulaIndex === match.formulaIndex
                };
            });

            // 计算正确匹配的数量
            const correctCount = this.matchResults.filter(r => r.isCorrect).length;
            this.allCorrect = correctCount === this.formulas.length;

            // 生成回应
            if (this.allCorrect) {
                this.response = `
  ### 🎉 太棒了！所有公式都匹配正确！
  
  你已经成功地理解了LDA算法的核心数学概念。重温一下这些公式：
  
  1. **类均值向量** - 计算每个类别样本的平均位置
  2. **类内散布矩阵** - 衡量同一类别内部样本的分散程度
  3. **类间散布矩阵** - 衡量不同类别之间的分离程度
  4. **Fisher准则** - LDA的优化目标，最大化类间散度与类内散度的比值
  5. **广义特征值问题** - 求解最优投影方向的数学方程
  
  在下一部分中，我们将更详细地探讨类内散布矩阵和类间散布矩阵的几何意义和计算方法。
          `;
            } else {
                const incorrectCount = this.formulas.length - correctCount;
                this.response = `
  ### 匹配结果：有 ${incorrectCount} 个不正确
  
  请检查你的匹配结果，特别留意那些标记为错误的匹配。回顾一下各公式的含义：
  
  - **类均值向量** 计算每个类别的中心位置
  - **类内散布矩阵** 反映了每个类别内部的分散程度
  - **类间散布矩阵** 反映了不同类别之间的分离程度
  - **Fisher准则** 是LDA的优化目标函数
  - **广义特征值问题** 是求解最优投影方向的数学方法
  
  请重新尝试匹配各公式及其描述。
          `;
            }

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

.interaction-description {
    margin-bottom: 20px;
    font-size: 14px;
    color: #606266;
}

.matching-exercise {
    display: flex;
    margin-bottom: 20px;
    align-items: flex-start;
}

.formulas-container,
.descriptions-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.arrow-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 20px;
    font-size: 24px;
    color: #909399;
}

.formula-item,
.description-item {
    background-color: white;
    padding: 15px;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
    cursor: pointer;
    transition: all 0.3s;
    position: relative;
}

.formula-item.selected,
.description-item.selected {
    border-color: #409EFF;
    box-shadow: 0 0 8px rgba(64, 158, 255, 0.4);
}

.description-item.matched {
    border-color: #909399;
    cursor: default;
}

.description-item.correct-match {
    border-color: #67C23A;
    background-color: rgba(103, 194, 58, 0.1);
}

.description-item.wrong-match {
    border-color: #F56C6C;
    background-color: rgba(245, 108, 108, 0.1);
}

.formula-content,
.description-content {
    margin-bottom: 10px;
}

.formula-label,
.description-label {
    font-size: 12px;
    color: #909399;
}

.match-info {
    position: absolute;
    top: 5px;
    right: 5px;
    font-size: 12px;
    color: #909399;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 2px 5px;
    border-radius: 3px;
    display: flex;
    align-items: center;
}

.match-icon {
    margin-left: 5px;
}

.match-icon.correct {
    color: #67C23A;
}

.match-icon.wrong {
    color: #F56C6C;
}

.matching-controls {
    display: flex;
    gap: 10px;
    justify-content: center;
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