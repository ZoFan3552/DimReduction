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
                <p>以下哪些参数会影响t-SNE算法的聚类效果？（可多选）</p>
                <el-checkbox-group v-model="userAnswer">
                    <el-checkbox label="perplexity">困惑度(perplexity)</el-checkbox>
                    <el-checkbox label="iterations">迭代次数(iterations)</el-checkbox>
                    <el-checkbox label="learning_rate">学习率(learning rate)</el-checkbox>
                    <el-checkbox label="early_exaggeration">早期夸大系数(early exaggeration)</el-checkbox>
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
                    <p>是的，所有这些参数都会影响t-SNE的聚类效果：</p>
                    <ul>
                        <li><strong>困惑度(perplexity)</strong>：控制考虑的近邻数量，影响局部与全局结构的平衡</li>
                        <li><strong>迭代次数(iterations)</strong>：更多迭代通常产生更好的结果，但会增加计算时间</li>
                        <li><strong>学习率(learning rate)</strong>：控制每次迭代的步长，过大或过小都会影响结果质量</li>
                        <li><strong>早期夸大系数(early exaggeration)</strong>：增强早期阶段的聚类分离，帮助避免局部最优</li>
                    </ul>
                    <el-button type="success" @click="proceedToNext">继续学习</el-button>
                </div>
                <div v-else>
                    <h3><i class="el-icon-error"></i> 再想想...</h3>
                    <p>t-SNE的效果高度依赖于参数设置，多个参数共同影响最终的可视化效果。请再考虑一下。</p>
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
    name: 'LessonTsneHyperparameters',
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
# t-SNE算法的超参数

**t-SNE**算法的效果很大程度上取决于其超参数的设置。理解这些参数对于获得有意义的可视化结果至关重要。

## 主要超参数

### 1. 困惑度(Perplexity)

这是t-SNE中最重要的参数，通常设置在5到50之间：

- **定义**: 可以理解为考虑每个点周围的有效近邻数量
- **低困惑度值**: 关注非常局部的结构，可能显示许多小聚类
- **高困惑度值**: 保留更多全局结构，但可能会丢失一些局部细节
- **经验法则**: 对于小数据集(n < 200)，使用较小的perplexity(5-10)；对于大数据集，可以使用较大值(30-50)

### 2. 学习率(Learning Rate)

控制每次迭代中点移动的程度：

- **过高**: 可能导致不稳定，产生"爆炸"效应
- **过低**: 可能陷入局部最优解
- **默认值**: 通常设为200
- **自适应方法**: 有些实现使用自适应学习率

### 3. 迭代次数(Iterations)

t-SNE是一个迭代算法，需要足够的迭代次数才能收敛：

- **推荐值**: 通常为1000-2000次迭代
- **早期与后期迭代**: 早期迭代建立大致结构，后期迭代微调局部结构
- **收敛判断**: 当成本函数变化很小时，可以停止迭代

### 4. 早期夸大系数(Early Exaggeration)

在优化的早期阶段，临时增大相似度以帮助形成更好的聚类：

- **作用**: 增加聚类间距离，防止早期陷入局部最优
- **典型值**: 通常设置为12
- **应用阶段**: 仅在前100-250次迭代中应用

## 参数调优策略

调整t-SNE参数时，建议采用以下策略：

1. **从多个不同的初始化开始**，选择成本最低的结果
2. **尝试不同的perplexity值**，比较结果
3. **增加迭代次数**，直到可视化结果稳定
4. **谨慎调整学习率**，从默认值开始尝试

记住，t-SNE主要用于可视化，结果的质量应该基于其可解释性而非某个数值指标。
`,
            userAnswer: [],
            showResponse: false,
            isCorrect: false,
            correctAnswers: ['perplexity', 'iterations', 'learning_rate', 'early_exaggeration']
        };
    },
    computed: {
        renderedMarkdown() {
            // 将多行字符串的缩进去掉，并确保正确处理
            try {
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