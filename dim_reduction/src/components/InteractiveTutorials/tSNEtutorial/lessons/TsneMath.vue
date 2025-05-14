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
                <h3>理解t-SNE的数学公式</h3>
                <p>下面是t-SNE中相似度计算和梯度计算的公式，请将公式与其描述匹配起来：</p>

                <el-row :gutter="20" class="formula-matching">
                    <el-col :span="12">
                        <h4>公式：</h4>
                        <div v-for="(formula, index) in formulas" :key="'formula-' + index" class="formula-item"
                            :class="{ selected: selectedFormula === index }" @click="selectFormula(index)">
                            <div class="formula-content" v-html="formula.latex"></div>
                        </div>
                    </el-col>

                    <el-col :span="12">
                        <h4>描述：</h4>
                        <div v-for="(description, index) in descriptions" :key="'desc-' + index"
                            class="description-item" :class="{ selected: selectedDescription === index }"
                            @click="selectDescription(index)">
                            <div class="description-content">{{ description.text }}</div>
                        </div>
                    </el-col>
                </el-row>

                <div class="matching-pairs">
                    <h4>已匹配的公式：</h4>
                    <div v-for="(pair, index) in userMatches" :key="'pair-' + index" class="matched-pair">
                        <el-card shadow="hover">
                            <div class="formula-content" v-html="formulas[pair.formulaIndex].latex"></div>
                            <el-divider></el-divider>
                            <div class="description-content">{{ descriptions[pair.descriptionIndex].text }}</div>
                            <el-button type="danger" size="mini" icon="el-icon-delete" circle
                                @click="removeMatch(index)"></el-button>
                        </el-card>
                    </div>
                </div>

                <div class="action-buttons">
                    <el-button type="primary" :disabled="userMatches.length < formulas.length"
                        @click="checkAnswer">检查匹配</el-button>
                    <el-button @click="resetMatches">重置</el-button>
                </div>
            </el-card>
        </div>

        <!-- 回应部分 -->
        <div v-if="showResponse" class="response-section">
            <el-card :class="{ 'correct-answer': isCorrect, 'wrong-answer': !isCorrect }">
                <div v-if="isCorrect">
                    <h3><i class="el-icon-success"></i> 匹配正确!</h3>
                    <p>你已经正确理解了t-SNE的核心数学公式：</p>
                    <div v-for="(match, index) in correctMatches" :key="index">
                        <h4>公式 {{ index + 1 }}:</h4>
                        <div class="formula-content" v-html="formulas[match.formulaIndex].latex"></div>
                        <p><strong>描述：</strong> {{ descriptions[match.descriptionIndex].text }}</p>
                        <el-divider v-if="index < correctMatches.length - 1"></el-divider>
                    </div>
                    <p>理解这些数学公式是掌握t-SNE算法的关键。接下来，我们将探讨t-SNE算法的超参数如何影响结果。</p>
                    <el-button type="success" @click="proceedToNext">继续学习</el-button>
                </div>
                <div v-else>
                    <h3><i class="el-icon-error"></i> 匹配有误</h3>
                    <p>请重新检查公式与描述的对应关系。提示：仔细阅读公式中的符号，思考它们的物理意义。</p>
                    <el-button @click="resetAnswer">重新匹配</el-button>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
import { marked } from 'marked';
import 'katex/dist/katex.min.css';
import katex from 'katex';


export default {
    name: 'Lesson4TsneMath',
    props: {
        isCompleted: {
            type: Boolean,
            default: false
        },
        userAnswers: {
            type: Array,
            default: null
        }
    },
    data() {
        return {
            markdown: `
  # t-SNE的数学原理
  
  t-SNE算法的核心是通过最小化原始空间和嵌入空间中概率分布的Kullback-Leibler散度来保留数据点之间的相似度。
  
  ## 高维空间中的相似度
  
  在高维空间中，点 $x_i$ 和 $x_j$ 之间的相似度使用条件概率 $p_{j|i}$ 表示：
  
  $$p_{j|i} = \\frac{\\exp(-\\|x_i - x_j\\|^2 / 2\\sigma_i^2)}{\\sum_{k \\neq i} \\exp(-\\|x_i - x_k\\|^2 / 2\\sigma_i^2)}$$
  
  其中 $\\sigma_i$ 是以点 $x_i$ 为中心的高斯分布的方差，通过二分搜索确定，使得困惑度（perplexity）达到用户指定的值。
  
  为了简化，我们通常使用对称版本：
  
  $$p_{ij} = \\frac{p_{j|i} + p_{i|j}}{2n}$$
  
  ## 低维空间中的相似度
  
  在低维空间中，点 $y_i$ 和 $y_j$ 之间的相似度使用t分布定义：
  
  $$q_{ij} = \\frac{(1 + \\|y_i - y_j\\|^2)^{-1}}{\\sum_{k \\neq l}(1 + \\|y_k - y_l\\|^2)^{-1}}$$
  
  t分布有较重的尾部，这有助于解决"拥挤问题"。
  
  ## 目标函数
  
  t-SNE的目标是最小化两个分布 $P$ 和 $Q$ 之间的KL散度：
  
  $$C = KL(P || Q) = \\sum_{i} \\sum_{j} p_{ij} \\log \\frac{p_{ij}}{q_{ij}}$$
  
  ## 梯度计算
  
  通过梯度下降最小化目标函数，梯度计算公式为：
  
  $$\\frac{\\partial C}{\\partial y_i} = 4 \\sum_j (p_{ij} - q_{ij})(y_i - y_j)(1 + \\|y_i - y_j\\|^2)^{-1}$$
  
  在梯度下降过程中，我们通常使用动量加速收敛。
  
  接下来，让我们通过一个互动练习来巩固对这些公式的理解。
        `,
            formulas: [
                {
                    id: 1,
                    latex: katex.renderToString("p_{j|i} = \\frac{\\exp(-\\|x_i - x_j\\|^2 / 2\\sigma_i^2)}{\\sum_{k \\neq i} \\exp(-\\|x_i - x_k\\|^2 / 2\\sigma_i^2)}", { displayMode: true })
                },
                {
                    id: 2,
                    latex: katex.renderToString("q_{ij} = \\frac{(1 + \\|y_i - y_j\\|^2)^{-1}}{\\sum_{k \\neq l}(1 + \\|y_k - y_l\\|^2)^{-1}}", { displayMode: true })
                },
                {
                    id: 3,
                    latex: katex.renderToString("C = KL(P || Q) = \\sum_{i} \\sum_{j} p_{ij} \\log \\frac{p_{ij}}{q_{ij}}", { displayMode: true })
                },
                {
                    id: 4,
                    latex: katex.renderToString("\\frac{\\partial C}{\\partial y_i} = 4 \\sum_j (p_{ij} - q_{ij})(y_i - y_j)(1 + \\|y_i - y_j\\|^2)^{-1}", { displayMode: true })
                }
            ],
            descriptions: [
                {
                    id: 1,
                    text: "高维空间中数据点之间的相似度，使用高斯分布建模。表示给定点i时，选择点j作为邻居的条件概率。"
                },
                {
                    id: 2,
                    text: "低维空间中数据点之间的相似度，使用t分布建模。t分布的厚尾特性有助于解决拥挤问题。"
                },
                {
                    id: 3,
                    text: "t-SNE的目标函数，是高维分布P和低维分布Q之间的Kullback-Leibler散度，我们希望最小化这个散度。"
                },
                {
                    id: 4,
                    text: "t-SNE的梯度公式，表示如何调整低维坐标以最小化目标函数。这个梯度用于更新低维表示中的每个点。"
                }
            ],
            selectedFormula: null,
            selectedDescription: null,
            userMatches: [],
            showResponse: false,
            isCorrect: false,
            correctMatches: [
                { formulaIndex: 0, descriptionIndex: 0 },
                { formulaIndex: 1, descriptionIndex: 1 },
                { formulaIndex: 2, descriptionIndex: 2 },
                { formulaIndex: 3, descriptionIndex: 3 }
            ]
        };
    },
    computed: {
        renderedMarkdown() {
            return marked(this.markdown);
        }
    },
    watch: {
        selectedFormula(val) {
            if (val !== null && this.selectedDescription !== null) {
                this.addMatch();
            }
        },
        selectedDescription(val) {
            if (this.selectedFormula !== null && val !== null) {
                this.addMatch();
            }
        }
    },
    mounted() {
        // 如果已经完成，使用保存的答案
        if (this.isCompleted && this.userAnswers) {
            this.userMatches = this.userAnswers;
            this.showResponse = true;
            this.isCorrect = true;
        }
    },
    methods: {
        selectFormula(index) {
            this.selectedFormula = index;
        },
        selectDescription(index) {
            this.selectedDescription = index;
        },
        addMatch() {
            // 检查是否已经匹配过这个公式或描述
            const formulaAlreadyMatched = this.userMatches.some(match => match.formulaIndex === this.selectedFormula);
            const descriptionAlreadyMatched = this.userMatches.some(match => match.descriptionIndex === this.selectedDescription);

            if (!formulaAlreadyMatched && !descriptionAlreadyMatched) {
                this.userMatches.push({
                    formulaIndex: this.selectedFormula,
                    descriptionIndex: this.selectedDescription
                });
            }

            // 重置选择
            this.selectedFormula = null;
            this.selectedDescription = null;
        },
        removeMatch(index) {
            this.userMatches.splice(index, 1);
        },
        checkAnswer() {
            if (this.userMatches.length !== this.correctMatches.length) {
                this.isCorrect = false;
                this.showResponse = true;
                return;
            }

            // 检查每个匹配是否正确
            this.isCorrect = this.userMatches.every((match, index) => {
                const correctMatch = this.correctMatches[index];
                return match.formulaIndex === correctMatch.formulaIndex &&
                    match.descriptionIndex === correctMatch.descriptionIndex;
            });

            this.showResponse = true;
        },
        resetMatches() {
            this.userMatches = [];
            this.selectedFormula = null;
            this.selectedDescription = null;
        },
        resetAnswer() {
            this.showResponse = false;
            this.resetMatches();
        },
        proceedToNext() {
            this.$emit('lesson-completed', true);
            this.$emit('user-response', this.userMatches);
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

.formula-matching {
    margin: 20px 0;
}

.formula-item,
.description-item {
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}

.formula-item:hover,
.description-item:hover {
    border-color: #409eff;
}

.formula-item.selected,
.description-item.selected {
    border-color: #409eff;
    background-color: #ecf5ff;
}

.matching-pairs {
    margin: 20px 0;
}

.matched-pair {
    margin-bottom: 15px;
    position: relative;
}

.matched-pair .el-button {
    position: absolute;
    top: 10px;
    right: 10px;
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