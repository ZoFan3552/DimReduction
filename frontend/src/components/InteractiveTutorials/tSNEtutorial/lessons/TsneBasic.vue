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
                <h3>t-SNE 算法步骤</h3>
                <p>请将下面的t-SNE算法步骤拖动到正确的顺序：</p>

                <div class="sorting-container">
                    <draggable v-model="userSortedSteps" animation="300" class="sorting-list">
                        <div v-for="(step, index) in userSortedSteps" :key="index" class="sorting-item">
                            <el-card shadow="hover">
                                <div class="step-number">{{ index + 1 }}</div>
                                <div class="step-content">{{ step.text }}</div>
                            </el-card>
                        </div>
                    </draggable>
                </div>

                <div class="action-buttons">
                    <el-button type="primary" @click="checkAnswer">检查顺序</el-button>
                    <el-button @click="resetSteps">重置</el-button>
                </div>
            </el-card>
        </div>

        <!-- 回应部分 -->
        <div v-if="showResponse" class="response-section">
            <el-card :class="{ 'correct-answer': isCorrect, 'wrong-answer': !isCorrect }">
                <div v-if="isCorrect">
                    <h3><i class="el-icon-success"></i> 排序正确!</h3>
                    <p>你已经正确理解了t-SNE算法的基本步骤：</p>
                    <ol>
                        <li v-for="(step, index) in correctSteps" :key="index">
                            {{ step.text }}
                        </li>
                    </ol>
                    <p>这些步骤共同构成了t-SNE算法的核心流程。接下来，我们将深入探讨每个步骤的数学细节。</p>
                    <el-button type="success" @click="proceedToNext">继续学习</el-button>
                </div>
                <div v-else>
                    <h3><i class="el-icon-error"></i> 顺序不太对</h3>
                    <p>请仔细思考t-SNE算法的基本流程。提示：首先需要计算原始空间中数据点之间的相似度。</p>
                    <el-button @click="resetAnswer">重新排序</el-button>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
import { marked } from 'marked';
import draggable from 'vuedraggable';
import 'katex/dist/katex.min.css';


export default {
    name: 'Lesson3TsneBasics',
    components: {
        draggable
    },
    props: {
        isCompleted: {
            type: Boolean,
            default: false
        },
        // userAnswers: {
        //     type: Array,
        //     default: null
        // }
    },
    data() {
        return {
            markdown: `
  # t-SNE算法基础
  
  t-SNE（t-distributed Stochastic Neighbor Embedding）是由Laurens van der Maaten和Geoffrey Hinton在2008年提出的算法，其目标是找到数据的低维表示，使得相似的数据点在低维空间中靠近，不相似的数据点远离。
  
  ## t-SNE的核心思想
  
  t-SNE的关键思想是将欧几里得距离转换为条件概率，表示数据点之间的相似度：
  
  1. 在原始高维空间中，使用高斯分布建模点与点之间的相似度
  2. 在目标低维空间中，使用t分布建模点之间的相似度
  3. 通过最小化这两种分布之间的KL散度来优化低维表示
  
  ## 为什么使用t分布？
  
  在低维空间使用t分布（而不是高斯分布）有两个主要原因：
  
  1. **解决拥挤问题(Crowding Problem)**：在高维空间，数据点可以以多种方式彼此远离，但在低维空间，这种"远离"的可能性减少了。t分布有较重的尾部，能更好地表示中等距离的点。
  
  2. **计算效率**：t分布的导数计算更简单，减少了计算复杂度。
  
  
  *t分布（橙色）比高斯分布（蓝色）有更厚的尾部*
  
  接下来，我们将学习t-SNE算法的具体步骤。
        `,
            correctSteps: [
                { id: 1, text: "计算高维空间中数据点之间的相似度（使用高斯分布）" },
                { id: 2, text: "初始化低维空间中的数据点（通常使用随机初始化或PCA）" },
                { id: 3, text: "计算低维空间中数据点之间的相似度（使用t分布）" },
                { id: 4, text: "计算两种分布之间的KL散度" },
                { id: 5, text: "使用梯度下降最小化KL散度，更新低维坐标" },
                { id: 6, text: "重复步骤3-5直到收敛" }
            ],
            userSortedSteps: [],
            showResponse: false,
            isCorrect: false
        };
    },
    computed: {
        renderedMarkdown() {
            return marked(this.markdown);
        },
        isStepOrderCorrect() {
            if (this.userSortedSteps.length !== this.correctSteps.length) {
                return false;
            }

            for (let i = 0; i < this.userSortedSteps.length; i++) {
                if (this.userSortedSteps[i].id !== this.correctSteps[i].id) {
                    return false;
                }
            }

            return true;
        }
    },
    created() {
        // 打乱步骤顺序
        this.userSortedSteps = [...this.correctSteps]
            .sort(() => Math.random() - 0.5);
    },
    mounted() {
        // 如果已经完成，使用保存的答案
        // if (this.isCompleted && this.userAnswers) {
        //     this.userSortedSteps = this.userAnswers;
        //     this.showResponse = true;
        //     this.isCorrect = true;
        // }
    },
    methods: {
        checkAnswer() {
            this.isCorrect = this.isStepOrderCorrect;
            this.showResponse = true;
        },
        resetSteps() {
            // 重新打乱步骤顺序
            this.userSortedSteps = [...this.correctSteps]
                .sort(() => Math.random() - 0.5);
        },
        resetAnswer() {
            this.showResponse = false;
        },
        proceedToNext() {
            this.$emit('lesson-completed', true);
            this.$emit('user-response', this.userSortedSteps);
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

.sorting-container {
    margin: 20px 0;
}

.sorting-list {
    min-height: 300px;
}

.sorting-item {
    margin-bottom: 10px;
    cursor: move;
}

.step-number {
    display: inline-block;
    width: 30px;
    height: 30px;
    line-height: 30px;
    text-align: center;
    border-radius: 50%;
    background-color: #409eff;
    color: white;
    margin-right: 10px;
}

.step-content {
    display: inline-block;
    vertical-align: middle;
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