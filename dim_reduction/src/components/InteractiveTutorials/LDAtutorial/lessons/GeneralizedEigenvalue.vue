<!-- GeneralizedEigenvalueFormulation.vue - 广义特征值公式教学组件 -->
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

        <!-- 互动区域 - 广义特征值问题可视化与理解 -->
        <div class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-data-analysis"></i> 互动练习：广义特征值问题理解
            </h3>

            <p class="interaction-description">
                请仔细阅读以下关于广义特征值问题的描述，并在交互练习中填充缺失的数学表达式。
            </p>

            <div class="eigenvalue-quiz">
                <h4>填充正确的数学表达式</h4>

                <div class="quiz-item">
                    <p>
                        LDA的优化目标是寻找投影方向<math-formula expression="w" />，使得投影后类间距离最大，类内距离最小，可以表示为最大化比率：
                    </p>
                    <div class="formula-container">
                        <math-formula expression="J(w) = " />

                        <el-select v-model="answers[0]" placeholder="选择表达式">
                            <el-option v-for="(option, index) in options[0]" :key="index" :value="option.value"
                                :label="option.rawLabel">
                                <span class="katex-option" v-html="option.label"></span>
                            </el-option>
                        </el-select>
                    </div>
                </div>

                <div class="quiz-item">
                    <p>
                        通过拉格朗日乘数法求解这个优化问题，我们得到：
                    </p>
                    <div class="formula-container">
                        <el-select v-model="answers[1]" placeholder="选择表达式">
                            <el-option v-for="(option, index) in options[1]" :key="index" :value="option.value"
                                :label="option.rawLabel">
                                <span class="katex-option" v-html="option.label"></span>
                            </el-option>
                        </el-select>
                        <math-formula expression=" = \lambda " />

                        <el-select v-model="answers[2]" placeholder="选择表达式">
                            <el-option v-for="(option, index) in options[2]" :key="index" :value="option.value"
                                :label="option.rawLabel">
                                <span class="katex-option" v-html="option.label"></span>
                            </el-option>
                        </el-select>
                    </div>
                </div>

                <div class="quiz-item">
                    <p>
                        该方程通常被称为广义特征值问题。另一种等价形式是：
                    </p>
                    <div class="formula-container">
                        <el-select v-model="answers[3]" placeholder="选择表达式">
                            <el-option v-for="(option, index) in options[3]" :key="index" :value="option.value"
                                :label="option.rawLabel">
                                <span class="katex-option" v-html="option.label"></span>
                            </el-option>
                        </el-select>
                        <math-formula expression=" = \lambda w" />
                    </div>
                </div>

                <div class="quiz-item">
                    <p>
                        LDA投影方向的解是矩阵
                        <el-select v-model="answers[4]" placeholder="选择表达式" style="width: 150px">
                            <el-option v-for="(option, index) in options[4]" :key="index" :value="option.value"
                                :label="option.rawLabel">
                                <span class="katex-option" v-html="option.label"></span>
                            </el-option>
                        </el-select>
                        的特征向量，对应于最大的
                        <el-select v-model="answers[5]" placeholder="选择数字" style="width: 150px">
                            <el-option v-for="(option, index) in options[5]" :key="index" :value="option.value"
                                :label="option.rawLabel">
                                <span class="katex-option" v-html="option.label"></span>
                            </el-option>
                        </el-select>
                        个特征值。
                    </p>
                </div>

                <div class="quiz-actions">
                    <el-button type="primary" @click="checkAnswers" :disabled="!allAnswersSelected || quizChecked">
                        检查答案
                    </el-button>

                    <el-button type="success" @click="completeSection" v-if="allCorrect">
                        继续学习 <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
        </div>

        <!-- 回应区域 -->
        <div v-if="showResponse" class="response-area">
            <div class="response-content">
                <i :class="['response-icon', responseIconClass]"></i>
                <div class="response-message" v-html="compiledResponse"></div>
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
import MathFormula from '@/utils/MathFormula.vue';

// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}



export default {
    name: 'GeneralizedEigenvalueFormulation',
    components: {
        MathFormula
    },
    props: {
        sectionId: {
            type: String,
            default: 'eigenvalue-formulation'
        },
        sectionIndex: {
            type: Number,
            required: true
        },
        totalSections: {
            type: Number,
            required: true
        },
        userAnswers: {
            default: null
        }
    },
    watch: {
        // 当从父组件收到新的用户答案时更新本地状态
        userAnswers(newVal) {
            if (newVal) {
                this.answers = JSON.parse(newVal);
            }

        }
    },
    data() {
        return {
            title: "广义特征值公式",
            markdownContent: `
# 广义特征值公式

LDA的核心是将Fisher判别准则的优化问题转化为求解广义特征值问题。这一数学转换使得LDA可以通过矩阵运算高效地找到最优投影方向。

## Fisher判别准则回顾

回顾LDA的优化目标，Fisher判别准则定义为：

$$
J(w) = \\frac{w^T S_B w}{w^T S_W w}
$$

其中：
- $w$ 是投影方向（向量或矩阵）
- $S_B$ 是类间散布矩阵
- $S_W$ 是类内散布矩阵

我们的目标是找到 $w$，使得 $J(w)$ 最大化，即投影后类间距离尽可能大，类内距离尽可能小。

## 优化问题的数学推导

为了最大化 $J(w)$，我们可以对 $w$ 求导并令其等于零。但是，这个比值形式的优化目标不易直接求导。因此，我们通过拉格朗日乘数法将其转化为一个约束优化问题。

具体来说，我们可以将目标重新表述为：
- 最大化 $w^T S_B w$（类间散度）
- 同时约束 $w^T S_W w = 1$（类内散度固定）

对应的拉格朗日函数为：

$$
L(w, \\lambda) = w^T S_B w - \\lambda(w^T S_W w - 1)
$$

对 $w$ 求导并令其等于零：

$$
\\frac{\\partial L}{\\partial w} = 2S_B w - 2\\lambda S_W w = 0
$$

化简得到：

$$
S_B w = \\lambda S_W w
$$

这就是广义特征值问题的标准形式。

## 广义特征值问题

广义特征值问题与普通特征值问题的差别在于，等式右侧包含矩阵 $S_W$ 与特征向量 $w$ 的乘积，而不仅仅是特征向量本身。

如果 $S_W$ 是可逆的（在大多数实际情况下成立），我们可以将等式转换为：

$$
S_W^{-1} S_B w = \\lambda w
$$

这样，我们就将广义特征值问题转化为普通特征值问题，即求解矩阵 $S_W^{-1} S_B$ 的特征值和特征向量。

## LDA解的维度

对于有 $k$ 个类别的问题，类间散布矩阵 $S_B$ 的秩最多是 $k-1$（因为它是 $k$ 个向量的线性组合，但这些向量并不完全独立）。这意味着 $S_W^{-1} S_B$ 最多有 $k-1$ 个非零特征值。

因此，对于一个 $k$ 类问题，LDA可以将数据降维到最多 $k-1$ 维的子空间。特别地，对于二分类问题 ($k=2$)，LDA将数据投影到一维空间，这也是为什么二分类LDA通常被视为一种投影到一条线上的方法。

## 实际求解过程

在实际应用中，求解LDA的步骤为：

1. 计算类内散布矩阵 $S_W$ 和类间散布矩阵 $S_B$
2. 计算 $S_W^{-1} S_B$（如果 $S_W$ 可逆）或使用其他方法（如奇异值分解）处理 $S_W$ 不可逆的情况
3. 求解 $S_W^{-1} S_B$ 的特征值和特征向量
4. 选择对应于最大的 $k-1$ 个特征值的特征向量，构成投影矩阵 $W$

通过这些步骤，我们可以找到最优的投影方向，实现降维的同时保留类别判别信息。

在下面的互动练习中，你将加深对广义特征值问题及其在LDA中应用的理解。
      `,
            isCompleted: false,


            // 互动练习数据
            options: [
                [
                    {
                        value: 0,
                        rawLabel: "w^T S_W w / w^T S_B w",
                        label: katex.renderToString("\\frac{w^T S_W w}{w^T S_B w}")
                    },
                    {
                        value: 1,
                        rawLabel: "w^T S_B w / w^T S_W w",
                        label: katex.renderToString("\\frac{w^T S_B w}{w^T S_W w}")
                    },
                    {
                        value: 2,
                        rawLabel: "(w^T S_B w - w^T S_W w)",
                        label: katex.renderToString("(w^T S_B w - w^T S_W w)")
                    },
                    {
                        value: 3,
                        rawLabel: "w^T (S_B - S_W) w",
                        label: katex.renderToString("w^T (S_B - S_W) w")
                    }
                ],
                [
                    {
                        value: 0,
                        rawLabel: "S_W w",
                        label: katex.renderToString("S_W w", {
                            displayMode: true,
                        })
                    },
                    {
                        value: 1,
                        rawLabel: "S_B w",
                        label: katex.renderToString("S_B w", {
                            displayMode: true,
                        })
                    },
                    {
                        value: 2,
                        rawLabel: "w^T S_B",
                        label: katex.renderToString("w^T S_B", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 3,
                        rawLabel: "S_B S_W w",
                        label: katex.renderToString("S_B S_W w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    }
                ],
                [
                    {
                        value: 0,
                        rawLabel: "S_W w",
                        label: katex.renderToString("S_W w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 1,
                        rawLabel: "S_B w",
                        label: katex.renderToString("S_B w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 2,
                        rawLabel: "w",
                        label: katex.renderToString("w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 3,
                        rawLabel: "S_W S_B w",
                        label: katex.renderToString("S_W S_B w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    }
                ],
                [
                    {
                        value: 0,
                        rawLabel: "S_W^{-1} w",
                        label: katex.renderToString("S_W^{-1} w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 1,
                        rawLabel: "S_B S_W^{-1} w",
                        label: katex.renderToString("S_B S_W^{-1} w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 2,
                        rawLabel: "S_W^{-1} S_B w",
                        label: katex.renderToString("S_W^{-1} S_B w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 3,
                        rawLabel: "S_B^{-1} S_W w",
                        label: katex.renderToString("S_B^{-1} S_W w", {
                            displayMode: true,
                            throwOnError: false
                        })
                    }
                ],
                [
                    {
                        value: 0,
                        rawLabel: "S_W^{-1}",
                        label: katex.renderToString("S_W^{-1}", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 1,
                        rawLabel: "S_B^{-1}",
                        label: katex.renderToString("S_B^{-1}", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 2,
                        rawLabel: "S_W^{-1} S_B",
                        label: katex.renderToString("S_W^{-1} S_B", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 3,
                        rawLabel: "S_B S_W^{-1}",
                        label: katex.renderToString("S_B S_W^{-1}", {
                            displayMode: true,
                            throwOnError: false
                        })
                    }
                ],
                [
                    {
                        value: 0,
                        rawLabel: "1",
                        label: katex.renderToString("1", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 1,
                        rawLabel: "k",
                        label: katex.renderToString("k", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 2,
                        rawLabel: "k-1",
                        label: katex.renderToString("k-1", {
                            displayMode: true,
                            throwOnError: false
                        })
                    },
                    {
                        value: 3,
                        rawLabel: "d",
                        label: katex.renderToString("d", {
                            displayMode: true,
                            throwOnError: false
                        })
                    }
                ],
                [
                    {
                        value: 0,
                        rawLabel: "p_{j|i} = \\frac{\\exp(-\\|x_i - x_j\\|^2 / 2\\sigma_i^2)}{\\sum_{k \\neq i} \\exp(-\\|x_i - x_k\\|^2 / 2\\sigma_i^2)}",
                        label: katex.renderToString("p_{j|i} = \\frac{\\exp(-\\|x_i - x_j\\|^2 / 2\\sigma_i^2)}{\\sum_{k \\neq i} \\exp(-\\|x_i - x_k\\|^2 / 2\\sigma_i^2)}", {
                            displayMode: true,
                            throwOnError: false
                        })
                    }
                ]
            ],
            answers: [null, null, null, null, null, null],
            correctAnswers: [1, 1, 0, 2, 2, 2],
            quizChecked: false,
            answerResults: [],

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
            // return marked(this.markdownContent);
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
        },
        allAnswersSelected() {
            return this.answers.every(answer => answer !== null);
        }
    },
    created() {
        // 检查该部分是否已完成
        const completedSections = this.getCompletedSections();
        this.isCompleted = completedSections.includes(this.sectionId);
    },
    methods: {
        checkAnswers() {

            this.quizChecked = true;
            this.answerResults = this.answers.map((answer, index) => answer === this.correctAnswers[index]);
            this.allCorrect = this.answerResults.every(result => result);

            // 发送答案给父组件保存
            this.$emit('save-answer', JSON.stringify(this.answers));

            if (this.allCorrect) {
                this.response = `
  ### 🎉 太棒了！所有答案都正确！
  
  你已经很好地理解了LDA中的广义特征值问题：
  
  1. LDA优化目标是最大化比率 $J(w) = \\frac{w^T S_B w}{w^T S_W w}$
  2. 经过拉格朗日乘数法推导，我们得到广义特征值问题 $S_B w = \\lambda S_W w$
  3. 如果 $S_W$ 可逆，可将广义特征值问题转化为 $S_W^{-1} S_B w = \\lambda w$
  4. LDA投影方向是矩阵 $S_W^{-1} S_B$ 的特征向量，对应于最大的 $k-1$ 个特征值
  
  这些理解对于实现LDA算法至关重要，也是我们后面学习LDA具体实现步骤的基础。
          `;
            } else {
                // 找出错误的答案
                const wrongAnswers = this.answerResults.map((result, index) => result ? null : index).filter(i => i !== null);

                let wrongItemsText = "";
                wrongAnswers.forEach(index => {
                    const questionTexts = [
                        "LDA优化目标",
                        "拉格朗日乘数法求解得到的等式左侧",
                        "拉格朗日乘数法求解得到的等式右侧",
                        "广义特征值问题的等价形式",
                        "LDA投影方向对应的矩阵",
                        "LDA能降低到的维度"
                    ];
                    wrongItemsText += `- 问题${index + 1}（${questionTexts[index]}）的答案不正确\n`;
                });

                this.response = `
  ### 有些答案不正确
  
  ${wrongItemsText}
  
  请再次回顾LDA的数学推导过程，特别注意广义特征值问题的形式和转换方法。
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

.eigenvalue-quiz {
    background-color: white;
    padding: 15px;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
}

.eigenvalue-quiz h4 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    color: #303133;
}

.quiz-item {
    margin-bottom: 20px;
}

.quiz-item p {
    margin: 0 0 10px 0;
    color: #606266;
}

.formula-container {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    background-color: #f8f8f9;
    padding: 10px;
    border-radius: 4px;
}

.el-select {
    min-width: 180px;
}

.quiz-actions {
    margin-top: 20px;
    display: flex;
    gap: 10px;
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