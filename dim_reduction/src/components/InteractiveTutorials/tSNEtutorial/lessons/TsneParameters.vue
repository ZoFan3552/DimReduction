<template>
    <div class="tsne-parameter-tutorial">
        <el-card class="tutorial-card">
            <div slot="header" class="card-header">
                <h1>t-SNE降维算法超参数教学</h1>
            </div>

            <el-steps :active="currentStep" finish-status="success" simple>
                <el-step v-for="(step, index) in steps" :key="index" :title="step.title"></el-step>
            </el-steps>

            <div class="content-section">
                <!-- 困惑度部分 -->
                <div v-if="currentStep >= 0">
                    <h2>超参数1: 困惑度 (Perplexity)</h2>
                    <p>困惑度是t-SNE中最重要的超参数之一，它影响算法对局部与全局结构的平衡。</p>

                    <div class="formula-container">
                        <p>困惑度定义为：</p>
                        <div class="katex-formula" ref="perplexityFormula"></div>
                    </div>

                    <p>困惑度的影响：</p>
                    <ul>
                        <li>表示每个点的"有效近邻数"</li>
                        <li>在5-50之间的值通常效果较好</li>
                        <li>太小：只关注非常局部的结构</li>
                        <li>太大：可能忽略局部特征</li>
                    </ul>



                    <div class="quiz-section">
                        <h3>小测验</h3>
                        <p>对于包含大约1000个点的数据集，以下哪个困惑度值最合适？</p>

                        <el-radio-group v-model="perplexityQuizAnswer">
                            <el-radio :label="1">困惑度 = 2</el-radio>
                            <el-radio :label="2">困惑度 = 30</el-radio>
                            <el-radio :label="3">困惑度 = 500</el-radio>
                            <el-radio :label="4">困惑度 = 1000</el-radio>
                        </el-radio-group>

                        <div v-if="perplexityQuizSubmitted">
                            <p v-if="perplexityQuizAnswer === 2" class="correct-answer">
                                正确！困惑度值通常为5-50之间，对于1000个点的数据集，30是个合理的选择。
                            </p>
                            <p v-else class="wrong-answer">
                                不太对。困惑度值通常在5-50之间较为合适，对于1000个点的数据集，30是个合理的选择。
                            </p>
                        </div>

                        <el-button type="primary" @click="submitPerplexityQuiz"
                            :disabled="perplexityQuizSubmitted || !perplexityQuizAnswer">
                            提交答案
                        </el-button>
                    </div>

                    <div class="navigation-buttons">
                        <el-button type="primary" @click="nextStep" :disabled="!perplexityQuizSubmitted">下一步</el-button>
                    </div>
                </div>

                <!-- 学习率部分 -->
                <div v-if="currentStep >= 1">
                    <h2>超参数2: 学习率 (Learning Rate)</h2>
                    <p>学习率控制每次迭代中梯度下降的步长，影响算法的收敛速度和稳定性。</p>

                    <ul>
                        <li>学习率过高：可能导致不稳定或局部最优</li>
                        <li>学习率过低：收敛速度慢，可能需要更多迭代</li>
                        <li>t-SNE通常使用自适应学习率方法</li>
                        <li>通常默认值设置为200（即2.0）</li>
                    </ul>



                    <div class="quiz-section">
                        <h3>小测验</h3>
                        <p>学习率对t-SNE的影响是什么？（可多选）</p>

                        <el-checkbox-group v-model="learningRateQuizAnswer">
                            <el-checkbox label="1">决定最终降维后数据点之间的距离</el-checkbox>
                            <el-checkbox label="2">影响算法的收敛速度</el-checkbox>
                            <el-checkbox label="3">决定困惑度的有效范围</el-checkbox>
                            <el-checkbox label="4">可能导致算法不稳定或陷入局部最优</el-checkbox>
                        </el-checkbox-group>

                        <div v-if="learningRateQuizSubmitted">
                            <p v-if="checkLearningRateQuizAnswer()" class="correct-answer">
                                正确！学习率主要影响收敛速度和稳定性。
                            </p>
                            <p v-else class="wrong-answer">
                                不完全正确。学习率主要影响算法的收敛速度(选项2)，并且设置不当可能导致算法不稳定或陷入局部最优(选项4)。
                            </p>
                        </div>

                        <el-button type="primary" @click="submitLearningRateQuiz"
                            :disabled="learningRateQuizSubmitted || learningRateQuizAnswer.length === 0">
                            提交答案
                        </el-button>
                    </div>

                    <div class="navigation-buttons">
                        <el-button @click="prevStep">上一步</el-button>
                        <el-button type="primary" @click="nextStep"
                            :disabled="!learningRateQuizSubmitted">下一步</el-button>
                    </div>
                </div>

                <!-- 最大迭代次数部分 -->
                <div v-if="currentStep >= 2">
                    <h2>超参数3: 最大迭代次数 (Max Iterations)</h2>
                    <p>最大迭代次数决定了优化过程的持续时间，影响结果的质量和计算成本。</p>

                    <ul>
                        <li>通常设置为250-1000之间</li>
                        <li>迭代次数过少：可能未完全收敛</li>
                        <li>迭代次数过多：计算成本增加，收益可能有限</li>
                        <li>复杂数据集通常需要更多的迭代次数</li>
                    </ul>



                    <div class="quiz-section">
                        <h3>小测验</h3>
                        <p>关于t-SNE的迭代次数，以下说法正确的是：</p>

                        <el-radio-group v-model="iterationQuizAnswer">
                            <el-radio :label="1">迭代次数越多，结果一定越好</el-radio>
                            <el-radio :label="2">迭代次数应该根据数据集大小和复杂性来确定</el-radio>
                            <el-radio :label="3">迭代次数对最终结果没有影响</el-radio>
                            <el-radio :label="4">t-SNE总是需要至少10000次迭代才能收敛</el-radio>
                        </el-radio-group>

                        <div v-if="iterationQuizSubmitted">
                            <p v-if="iterationQuizAnswer === 2" class="correct-answer">
                                正确！迭代次数应根据数据集大小和复杂性来确定，通常在250-1000之间。
                            </p>
                            <p v-else class="wrong-answer">
                                不正确。迭代次数应根据数据集大小和复杂性来确定，并非总是越多越好，通常在250-1000之间就足够了。
                            </p>
                        </div>

                        <el-button type="primary" @click="submitIterationQuiz"
                            :disabled="iterationQuizSubmitted || !iterationQuizAnswer">
                            提交答案
                        </el-button>
                    </div>

                    <div class="navigation-buttons">
                        <el-button @click="prevStep">上一步</el-button>
                        <el-button type="primary" @click="nextStep" :disabled="!iterationQuizSubmitted">下一步</el-button>
                    </div>
                </div>

                <!-- 总结部分 -->
                <div v-if="currentStep >= 3">
                    <h2>超参数调优总结</h2>

                    <p>t-SNE超参数的选择直接影响可视化效果。以下是关键超参数的总结：</p>

                    <el-table :data="hyperparameterSummary" style="width: 100%">
                        <el-table-column prop="name" label="超参数" width="180"></el-table-column>
                        <el-table-column prop="range" label="典型取值范围"></el-table-column>
                        <el-table-column prop="effect" label="影响"></el-table-column>
                    </el-table>

                    <div class="formula-container">
                        <p>t-SNE的目标是最小化KL散度：</p>
                        <div class="katex-formula" ref="klDivergenceFormula"></div>
                    </div>

                    <h3>实践建议</h3>
                    <ul>
                        <li>从默认参数开始，然后逐步调整</li>
                        <li>尝试不同的困惑度值（通常5-50之间）</li>
                        <li>对于大数据集，增加迭代次数</li>
                        <li>注意t-SNE的随机性，多次运行可能得到不同结果</li>
                    </ul>

                    <div class="final-quiz">
                        <h3>最终测验</h3>

                        <p>对于一个包含5000个数据点、100个特征的数据集，请选择最合适的t-SNE参数组合：</p>

                        <el-radio-group v-model="finalQuizAnswer">
                            <el-radio :label="1">困惑度=3, 学习率=10, 迭代次数=50</el-radio>
                            <el-radio :label="2">困惑度=30, 学习率=200, 迭代次数=1000</el-radio>
                            <el-radio :label="3">困惑度=2500, 学习率=1000, 迭代次数=200</el-radio>
                            <el-radio :label="4">困惑度=50, 学习率=500, 迭代次数=500</el-radio>
                        </el-radio-group>

                        <div v-if="finalQuizSubmitted">
                            <p v-if="finalQuizAnswer === 2 || finalQuizAnswer === 4" class="correct-answer">
                                正确！选项2和选项4都是合理的选择。对于5000个数据点，困惑度在30-50之间，足够的迭代次数（500-1000）和适当的学习率是合理的配置。
                            </p>
                            <p v-else class="wrong-answer">
                                不太对。选项1的困惑度和迭代次数太小，选项3的困惑度太大（不应超过数据集的大小）。较合理的选择是困惑度在30-50之间，迭代次数在500-1000之间。
                            </p>
                        </div>

                        <el-button type="primary" @click="submitFinalQuiz"
                            :disabled="finalQuizSubmitted || !finalQuizAnswer">
                            提交答案
                        </el-button>
                    </div>

                    <div class="navigation-buttons">
                        <el-button @click="prevStep">上一步</el-button>
                        <el-button type="success" @click="finishTutorial"
                            :disabled="!finalQuizSubmitted">完成学习</el-button>
                    </div>
                </div>

                <!-- 完成页面 -->
                <div v-if="currentStep === 4">
                    <div class="completion-page">
                        <h2>t-SNE超参数学习完成！</h2>

                        <el-progress type="circle" :percentage="100" status="success"></el-progress>

                        <p>您已经掌握了t-SNE的主要超参数及其影响：</p>
                        <ul>
                            <li>困惑度 (Perplexity): 影响局部与全局结构的平衡</li>
                            <li>学习率 (Learning Rate): 影响优化过程的稳定性</li>
                            <li>最大迭代次数 (Max Iterations): 影响收敛质量和计算成本</li>
                        </ul>

                        <div class="next-chapter-button">
                            <el-button type="primary" @click="goToNextChapter">下一章节</el-button>
                        </div>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import katex from 'katex';
import 'katex/dist/katex.min.css';

export default {
    name: 'TSNEParameterTutorial',
    data() {
        return {
            currentStep: 0,
            steps: [
                { title: '困惑度' },
                { title: '学习率' },
                { title: '迭代次数' },
                { title: '总结' },
                { title: '完成' }
            ],

            // 困惑度相关
            perplexityQuizAnswer: null,
            perplexityQuizSubmitted: false,

            // 学习率相关
            learningRateQuizAnswer: [],
            learningRateQuizSubmitted: false,

            // 迭代次数相关
            iterationQuizAnswer: null,
            iterationQuizSubmitted: false,

            // 总结页面相关
            finalQuizAnswer: null,
            finalQuizSubmitted: false,

            // 超参数总结表
            hyperparameterSummary: [
                {
                    name: '困惑度 (Perplexity)',
                    range: '5-50',
                    effect: '影响局部与全局结构的平衡'
                },
                {
                    name: '学习率 (Learning Rate)',
                    range: '10-1000 (0.1-10.0)',
                    effect: '影响优化速度和稳定性'
                },
                {
                    name: '最大迭代次数',
                    range: '250-1000',
                    effect: '影响结果质量和计算时间'
                }
            ]
        };
    },
    methods: {
        nextStep() {
            if (this.currentStep < this.steps.length - 1) {
                this.currentStep++;
                this.$nextTick(() => {
                    this.renderFormulas();
                });
            }
        },

        prevStep() {
            if (this.currentStep > 0) {
                this.currentStep--;
                this.$nextTick(() => {
                    this.renderFormulas();
                });
            }
        },

        finishTutorial() {
            this.currentStep = 4;
        },

        goToNextChapter() {
            this.$emit('lesson-completed', true);
            // this.$emit('user-response', this.userMatches);
        },

        // 公式渲染
        renderFormulas() {
            // 困惑度公式
            if (this.$refs.perplexityFormula) {
                katex.render(
                    'Perp(P_i) = 2^{H(P_i)} = 2^{-\\sum_j p_{j|i} \\log_2 p_{j|i}}',
                    this.$refs.perplexityFormula,
                    { displayMode: true }
                );
            }

            // KL散度公式
            if (this.$refs.klDivergenceFormula) {
                katex.render(
                    'KL(P || Q) = \\sum_i \\sum_j p_{ij} \\log\\frac{p_{ij}}{q_{ij}}',
                    this.$refs.klDivergenceFormula,
                    { displayMode: true }
                );
            }
        },

        // 提交困惑度测验
        submitPerplexityQuiz() {
            this.perplexityQuizSubmitted = true;
        },

        // 提交学习率测验
        submitLearningRateQuiz() {
            this.learningRateQuizSubmitted = true;
        },

        // 检查学习率测验答案
        checkLearningRateQuizAnswer() {
            // 正确答案是选项2和4
            return this.learningRateQuizAnswer.length === 2 &&
                this.learningRateQuizAnswer.includes('2') &&
                this.learningRateQuizAnswer.includes('4');
        },

        // 提交迭代次数测验
        submitIterationQuiz() {
            this.iterationQuizSubmitted = true;
        },

        // 提交最终测验
        submitFinalQuiz() {
            this.finalQuizSubmitted = true;
        }
    },
    mounted() {
        this.renderFormulas();
    }
};
</script>

<style scoped>
.tsne-parameter-tutorial {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.tutorial-card {
    margin-bottom: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.content-section {
    padding: 20px 0;
    min-height: 400px;
}

.formula-container {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 5px;
    margin: 15px 0;
}

.katex-formula {
    overflow-x: auto;
    padding: 10px 0;
}

.interactive-section {
    background-color: #f5f7fa;
    padding: 20px;
    border-radius: 5px;
    margin: 20px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.quiz-section {
    background-color: #ecf5ff;
    padding: 20px;
    border-radius: 5px;
    margin: 20px 0;
}

.correct-answer {
    color: #67c23a;
    font-weight: bold;
}

.wrong-answer {
    color: #f56c6c;
    font-weight: bold;
}

.navigation-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}

.completion-page {
    text-align: center;
    padding: 30px 20px;
}

.completion-page ul {
    text-align: left;
    display: inline-block;
    margin: 20px auto;
}

.next-chapter-button {
    margin-top: 30px;
}
</style>
