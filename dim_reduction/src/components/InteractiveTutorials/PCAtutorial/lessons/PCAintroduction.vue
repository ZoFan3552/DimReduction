<template>
    <base-segment :title="title" :content="content" :segment-id="segmentId" @segment-completed="onCompleted">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="quiz-container">
                <h3>理解检查</h3>
                <p>PCA最主要的目的是什么？</p>

                <el-radio-group v-model="selectedAnswer" class="option-list">
                    <el-radio v-for="(option, index) in options" :key="index" :label="index">
                        {{ option }}
                    </el-radio>
                </el-radio-group>

                <div class="submit-container">
                    <el-button type="primary" @click="checkAnswer" :disabled="selectedAnswer === null">
                        提交答案
                    </el-button>
                </div>
            </div>
        </template>
    </base-segment>
</template>

<script>
import BaseSegment from './BaseSegment.vue'

export default {
    name: 'IntroToPCA',
    components: {
        BaseSegment
    },
    data() {
        return {
            title: '1. 主成分分析(PCA)简介',
            segmentId: 'intro-to-pca',
            content: `
  ## 什么是主成分分析(PCA)?
  
  主成分分析(Principal Component Analysis, PCA)是一种常用的**无监督学习**降维技术。它通过线性变换将高维数据转换到低维空间，同时保留数据中的大部分信息。
  
  ### PCA的核心思想
  
  PCA的核心思想是寻找数据集的主要方向(主成分)，这些方向上的方差最大，也就是说，这些方向保留了数据中最多的信息。想象一下，如果我们将一个三维物体投影到二维平面上，我们希望选择的二维平面能够尽可能地保留原始物体的结构信息。
  
  
  ### PCA的主要应用
  
  PCA在数据科学和机器学习中有许多重要应用：
  
  - **降维**：将高维数据降到低维空间，便于可视化和后续处理
  - **数据压缩**：减少数据存储和计算需求
  - **噪声过滤**：通过丢弃方差较小的维度，可以去除数据中的噪声
  - **特征提取**：提取数据中最具信息量的特征
  - **数据预处理**：为其他机器学习算法准备数据
  
  ### PCA的数学本质
  
  从数学角度看，PCA是一种正交线性变换，将数据变换到一个新的坐标系统中。在新坐标系中，第一个坐标轴对应的是数据最大方差的方向，第二个坐标轴对应的是与第一个坐标轴正交的方向中，数据方差最大的方向，以此类推。
  
  对于包含$n$个样本和$p$个特征的数据矩阵$X$，PCA的目标是找到一个正交矩阵$W$，使得新的数据矩阵$Y = XW$具有某些特定性质。这个过程涉及到协方差矩阵的计算、特征值分解等步骤，我们将在后续章节详细介绍。
        `,
            // 选择题选项
            options: [
                "对高维数据进行聚类分析",
                "寻找数据中的主要方向，将高维数据投影到低维空间，同时保留最大方差",
                "通过有监督学习为数据打标签",
                "对数据进行标准化处理"
            ],
            selectedAnswer: null,
            // 跟踪答题尝试次数
            attempts: 0
        };
    },
    methods: {
        checkAnswer() {
            this.attempts++;
            const correctAnswerIndex = 1; // 正确答案是第二个选项

            if (this.selectedAnswer === correctAnswerIndex) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "回答正确！",
                    "PCA的主要目的确实是寻找数据中的主要方向，将高维数据降到低维空间，同时保留最大的方差。",
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.attempts >= 2) {
                    hint = "提示：思考PCA的核心目标，它关注数据的哪些特性？";
                }

                this.$refs.baseSegment.showResponse(
                    "回答不正确",
                    `请再次思考PCA的主要目的。${hint}`,
                    "error"
                );
            }
        },
        onCompleted() {
            // 通知父组件此片段已完成
            this.$emit('completed', this.segmentId);
        }
    },
    mounted() {
        // 确保基础组件引用正确
        this.$refs = this.$refs || {};
        this.$refs.baseSegment = this.$children[0];
    }
}
</script>

<style scoped>
.quiz-container {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.option-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 15px 0;
}

.submit-container {
    margin-top: 20px;
}

/* 确保KaTeX公式正确显示 */
:deep(.katex-display) {
    overflow-x: auto;
    overflow-y: hidden;
}
</style>