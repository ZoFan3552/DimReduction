<template>
    <base-segment ref="baseSegment" :title="title" :content="content" :segment-id="segmentId"
        @segment-completed="onCompleted" :isLastSegment="true">

        <!-- 互动部分 -->
        <template v-slot:interaction>
            <div class="practical-interactive">
                <h3>实际案例：鸢尾花数据集PCA分析</h3>
                <p>通过这个经典数据集，体验完整的PCA降维流程和可视化。</p>

                <div class="dataset-description">
                    <h4>鸢尾花数据集</h4>
                    <p>
                        鸢尾花数据集包含了三个不同品种的鸢尾花（Setosa、Versicolor和Virginica）的150个样本。
                        每个样本有4个特征：萼片长度、萼片宽度、花瓣长度和花瓣宽度。
                    </p>
                    <div class="dataset-preview">
                        <el-table :data="dataPreview" style="width: 100%" border size="mini">
                            <el-table-column prop="sepalLength" label="萼片长度"></el-table-column>
                            <el-table-column prop="sepalWidth" label="萼片宽度"></el-table-column>
                            <el-table-column prop="petalLength" label="花瓣长度"></el-table-column>
                            <el-table-column prop="petalWidth" label="花瓣宽度"></el-table-column>
                            <el-table-column prop="species" label="品种"></el-table-column>
                        </el-table>
                    </div>
                </div>

                <div class="analysis-steps">
                    <h4>PCA分析步骤</h4>
                    <el-steps :active="currentStep" finish-status="success" align-center>
                        <el-step v-for="(step, index) in steps" :key="index" :title="step.title"></el-step>
                    </el-steps>

                    <div class="step-content">
                        <div v-show="currentStep === 0" class="step-data-exploration">
                            <h5>步骤1: 数据探索</h5>
                            <p>首先，我们需要了解数据的基本特性和分布。</p>

                            <div class="stats-container">
                                <div class="stats-card">
                                    <h6>描述性统计</h6>
                                    <el-table :data="descriptiveStats" border size="mini">
                                        <el-table-column prop="stat" label="统计量"></el-table-column>
                                        <el-table-column prop="sepalLength" label="萼片长度"></el-table-column>
                                        <el-table-column prop="sepalWidth" label="萼片宽度"></el-table-column>
                                        <el-table-column prop="petalLength" label="花瓣长度"></el-table-column>
                                        <el-table-column prop="petalWidth" label="花瓣宽度"></el-table-column>
                                    </el-table>
                                </div>

                                <div class="correlation-matrix">
                                    <h6>特征相关性矩阵</h6>
                                    <div class="correlation-heatmap" ref="correlationHeatmap">
                                    </div>
                                </div>
                            </div>

                            <div class="data-insight">
                                <p>
                                    <strong>观察</strong>：花瓣长度和花瓣宽度高度相关，萼片长度与花瓣特征也有明显相关性。
                                    这表明特征间存在冗余信息，适合使用PCA进行降维。
                                </p>
                            </div>
                        </div>

                        <div v-show="currentStep === 1" class="step-data-preprocessing">
                            <h5>步骤2: 数据预处理</h5>
                            <p>在应用PCA之前，需要对数据进行标准化处理，使各特征具有相同的尺度。</p>

                            <div class="preprocessing-container">
                                <div class="preprocessing-viz" ref="preprocessingViz"></div>

                                <div class="preprocessing-explanation">
                                    <h6>标准化过程</h6>
                                    <p>标准化公式：<math-formula expression="z = \frac{x - \mu}{\sigma}" /></p>
                                    <p>其中，<math-formula expression="\mu" /> 是特征的平均值，<math-formula expression="\sigma" />
                                        是特征的标准差。</p>

                                    <div class="standardized-stats">
                                        <h6>标准化后的统计量</h6>
                                        <el-table :data="standardizedStats" border size="mini">
                                            <el-table-column prop="stat" label="统计量"></el-table-column>
                                            <el-table-column prop="sepalLength" label="萼片长度"></el-table-column>
                                            <el-table-column prop="sepalWidth" label="萼片宽度"></el-table-column>
                                            <el-table-column prop="petalLength" label="花瓣长度"></el-table-column>
                                            <el-table-column prop="petalWidth" label="花瓣宽度"></el-table-column>
                                        </el-table>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div v-show="currentStep === 2" class="step-pca-computation">
                            <h5>步骤3: PCA计算</h5>
                            <p>计算协方差矩阵，并求解其特征值和特征向量。</p>

                            <div class="pca-computation-container">
                                <div class="covariance-matrix">
                                    <h6>协方差矩阵</h6>
                                    <el-table :data="covarianceMatrix" border size="mini">
                                        <el-table-column prop="feature" label="特征"></el-table-column>
                                        <el-table-column prop="sepalLength" label="萼片长度"></el-table-column>
                                        <el-table-column prop="sepalWidth" label="萼片宽度"></el-table-column>
                                        <el-table-column prop="petalLength" label="花瓣长度"></el-table-column>
                                        <el-table-column prop="petalWidth" label="花瓣宽度"></el-table-column>
                                    </el-table>
                                </div>

                                <div class="eigenvalues">
                                    <h6>特征值</h6>
                                    <div class="eigenvalues-viz" ref="eigenvaluesViz"></div>
                                </div>

                                <div class="eigenvectors">
                                    <h6>特征向量（主成分）</h6>
                                    <el-table :data="eigenvectors" border size="mini">
                                        <el-table-column prop="component" label="主成分"></el-table-column>
                                        <el-table-column prop="sepalLength" label="萼片长度"></el-table-column>
                                        <el-table-column prop="sepalWidth" label="萼片宽度"></el-table-column>
                                        <el-table-column prop="petalLength" label="花瓣长度"></el-table-column>
                                        <el-table-column prop="petalWidth" label="花瓣宽度"></el-table-column>
                                    </el-table>
                                </div>
                            </div>
                        </div>

                        <div v-show="currentStep === 3" class="step-component-selection">
                            <h5>步骤4: 选择主成分</h5>
                            <p>根据特征值的方差贡献率，确定保留多少主成分。</p>

                            <div class="component-selection-container">
                                <div class="scree-plot" ref="screePlot"></div>

                                <div class="explained-variance">
                                    <h6>方差解释比例</h6>
                                    <el-table :data="explainedVariance" border size="mini">
                                        <el-table-column prop="component" label="主成分"></el-table-column>
                                        <el-table-column prop="eigenvalue" label="特征值"></el-table-column>
                                        <el-table-column prop="variance" label="方差百分比"></el-table-column>
                                        <el-table-column prop="cumulative" label="累计方差"></el-table-column>
                                    </el-table>

                                    <div class="variance-insight">
                                        <p>
                                            前两个主成分累计解释了原始数据的<strong>{{
                                                parseFloat(explainedVariance[1].cumulative).toFixed(2) }}%</strong>方差。
                                            这意味着我们可以使用这两个主成分来表示数据，同时保留大部分信息。
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <div class="component-selection">
                                <h6>选择主成分数量</h6>
                                <el-radio-group v-model="selectedComponents" @change="updateProjection">
                                    <el-radio :label="1">保留1个主成分</el-radio>
                                    <el-radio :label="2">保留2个主成分</el-radio>
                                    <el-radio :label="3">保留3个主成分</el-radio>
                                </el-radio-group>
                            </div>
                        </div>

                        <div v-show="currentStep === 4" class="step-data-projection">
                            <h5>步骤5: 数据投影</h5>
                            <p>将原始数据投影到选定的主成分上。</p>

                            <div class="projection-container">
                                <div class="projection-viz" ref="projectionViz"></div>

                                <div class="projection-explanation">
                                    <h6>投影后的数据（前{{ selectedComponents }}个主成分）</h6>
                                    <el-table :data="projectedDataPreview" border size="mini">
                                        <el-table-column v-for="i in selectedComponents" :key="i" :prop="`pc${i}`"
                                            :label="`PC${i}`"></el-table-column>
                                        <el-table-column prop="species" label="品种"></el-table-column>
                                    </el-table>

                                    <div class="dimension-reduction">
                                        <p><strong>降维效果</strong>：从原始的4个维度降低到{{ selectedComponents }}个维度，同时保留了数据的主要结构。
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div v-show="currentStep === 5" class="step-interpretation">
                            <h5>步骤6: 结果解释与应用</h5>
                            <p>解释主成分的含义，并探讨降维结果的应用。</p>

                            <div class="interpretation-container">
                                <div class="loadings-plot" ref="loadingsPlot"></div>

                                <div class="interpretation-explanation">
                                    <h6>主成分解释</h6>
                                    <ul>
                                        <li><strong>PC1</strong>（{{ parseFloat(explainedVariance[0].variance).toFixed(1)
                                        }}%）: 主要反映花的整体大小，尤其是花瓣的大小。</li>
                                        <li><strong>PC2</strong>（{{ parseFloat(explainedVariance[1].variance).toFixed(1)
                                        }}%）: 主要反映萼片宽度与其他特征的对比。</li>
                                    </ul>

                                    <h6>实际应用</h6>
                                    <p>降维后的数据可用于：</p>
                                    <ul>
                                        <li>数据可视化：在二维平面上直观展示数据结构</li>
                                        <li>特征工程：将主成分作为新特征用于后续机器学习任务</li>
                                        <li>聚类分析：基于降维数据进行品种聚类</li>
                                        <li>异常检测：识别不符合一般模式的鸢尾花样本</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="result-summary">
                                <h6>案例总结</h6>
                                <p>
                                    通过PCA，我们成功地将鸢尾花数据从4个维度降到2个维度，同时保留了约95%的原始信息。
                                    降维后的数据清晰地展示了三个鸢尾花品种的分布模式，证明了PCA在数据可视化和降维方面的有效性。
                                </p>
                            </div>
                        </div>

                        <div class="step-navigation">
                            <el-button type="info" icon="el-icon-arrow-left" @click="prevStep"
                                :disabled="currentStep === 0">
                                上一步
                            </el-button>
                            <el-button type="primary" @click="nextStep" :disabled="currentStep === steps.length - 1">
                                下一步
                                <i class="el-icon-arrow-right"></i>
                            </el-button>
                        </div>
                    </div>
                </div>

                <div class="case-quiz" v-if="currentStep === steps.length - 1">
                    <h4>理解检查</h4>
                    <p>基于鸢尾花数据集的PCA分析，请回答以下问题：</p>

                    <div class="quiz-question">
                        <p><strong>问题</strong>：根据PCA分析结果，以下哪个陈述是正确的？</p>

                        <el-radio-group v-model="quizAnswer" class="quiz-options">
                            <el-radio :label="0">三种鸢尾花品种在所有4个原始特征上的差异都非常显著</el-radio>
                            <el-radio :label="1">萼片宽度是区分鸢尾花品种的最重要特征</el-radio>
                            <el-radio :label="2">保留前两个主成分可以解释数据超过90%的方差</el-radio>
                            <el-radio :label="3">PCA表明鸢尾花的4个特征之间完全没有相关性</el-radio>
                        </el-radio-group>

                        <el-button type="primary" @click="checkAnswer" :disabled="quizAnswer === null"
                            class="submit-answer">
                            提交答案
                        </el-button>
                    </div>
                </div>
            </div>
        </template>
    </base-segment>
</template>

<script>
import BaseSegment from './BaseSegment.vue';
import * as d3 from 'd3';
import MathFormula from '@/utils/MathFormula.vue';

export default {
    name: 'PracticalExample',
    components: {
        BaseSegment,
        MathFormula
    },
    props: {
        savedAnswer: {
            type: String,
            default: null
        }
    },
    watch: {
        // 监听savedAnswer属性的变化
        savedAnswer: {
            immediate: true,
            handler(newValue) {
                console.log("intro子组件接受回答", newValue);
                if (newValue) {
                    this.quizAnswer = Number(newValue);
                    //   this.hasSubmittedAnswer = true;
                    //   this.feedback = '您之前已经完成了这个章节的练习。';
                }
            }
        }
    },
    data() {
        return {
            title: '9. 实际案例分析',
            segmentId: 'practical-example',
            content: `
  ## 实际案例：PCA在现实数据中的应用
  
  理论知识的掌握是基础，但将PCA应用于真实数据集才能真正体会其价值。在本章中，我们将通过一个经典的案例，展示PCA在实际数据分析中的完整流程和应用价值。
  
  ### 实际应用中的PCA流程
  
  在实际应用中，PCA分析通常遵循以下流程：
  
  1. **数据探索**：了解数据的基本特性、分布和相关性
  2. **数据预处理**：包括缺失值处理、异常值检测和数据标准化
  3. **PCA计算**：计算协方差矩阵及其特征值和特征向量
  4. **主成分选择**：基于方差解释比例等标准选择合适数量的主成分
  5. **数据投影**：将原始数据投影到选定的主成分上
  6. **结果解释与应用**：解释主成分的实际含义，并应用于后续任务
  
  ### 案例价值
  
  通过实际案例，我们可以：
  
  - **巩固理论知识**：将前面学习的PCA概念与方法应用于实际数据
  - **掌握实操技能**：学习数据预处理、结果可视化等实用技巧
  - **培养分析思维**：理解如何解释PCA结果，并从中获取有价值的见解
  - **了解应用场景**：探索PCA在数据可视化、特征工程等方面的具体应用
  
  ### 经典数据集：鸢尾花数据集
  
  鸢尾花（Iris）数据集是机器学习中最著名的数据集之一，包含三种不同品种的鸢尾花的测量数据。每个样本有四个特征：萼片长度、萼片宽度、花瓣长度和花瓣宽度。
  
  这个数据集非常适合PCA演示，因为：
  - 它具有多个特征，需要降维来可视化
  - 特征之间存在一定的相关性，适合应用PCA
  - 数据量适中，便于快速计算和理解
  - 结果直观，容易解释和评估
  
  在下面的互动环节中，我们将逐步展示如何对鸢尾花数据集应用PCA，从数据探索到结果解释的完整流程。
        `,
            // 分析步骤
            steps: [
                { title: '数据探索' },
                { title: '数据预处理' },
                { title: 'PCA计算' },
                { title: '选择主成分' },
                { title: '数据投影' },
                { title: '结果解释' }
            ],
            currentStep: 0,

            // 鸢尾花数据（模拟数据）
            irisData: [],
            dataPreview: [
                { sepalLength: 5.1, sepalWidth: 3.5, petalLength: 1.4, petalWidth: 0.2, species: 'Setosa' },
                { sepalLength: 7.0, sepalWidth: 3.2, petalLength: 4.7, petalWidth: 1.4, species: 'Versicolor' },
                { sepalLength: 6.3, sepalWidth: 3.3, petalLength: 6.0, petalWidth: 2.5, species: 'Virginica' },
                { sepalLength: 4.9, sepalWidth: 3.0, petalLength: 1.4, petalWidth: 0.2, species: 'Setosa' },
                { sepalLength: 5.7, sepalWidth: 2.8, petalLength: 4.1, petalWidth: 1.3, species: 'Versicolor' }
            ],

            // 描述性统计
            descriptiveStats: [
                { stat: '均值', sepalLength: '5.84', sepalWidth: '3.05', petalLength: '3.76', petalWidth: '1.20' },
                { stat: '标准差', sepalLength: '0.83', sepalWidth: '0.43', petalLength: '1.76', petalWidth: '0.76' },
                { stat: '最小值', sepalLength: '4.30', sepalWidth: '2.00', petalLength: '1.00', petalWidth: '0.10' },
                { stat: '最大值', sepalLength: '7.90', sepalWidth: '4.40', petalLength: '6.90', petalWidth: '2.50' }
            ],

            // 标准化后的统计量
            standardizedStats: [
                { stat: '均值', sepalLength: '0.00', sepalWidth: '0.00', petalLength: '0.00', petalWidth: '0.00' },
                { stat: '标准差', sepalLength: '1.00', sepalWidth: '1.00', petalLength: '1.00', petalWidth: '1.00' },
                { stat: '最小值', sepalLength: '-1.86', sepalWidth: '-2.43', petalLength: '-1.57', petalWidth: '-1.44' },
                { stat: '最大值', sepalLength: '2.48', sepalWidth: '3.12', petalLength: '1.78', petalWidth: '1.71' }
            ],

            // 协方差矩阵
            covarianceMatrix: [
                { feature: '萼片长度', sepalLength: '1.00', sepalWidth: '-0.12', petalLength: '0.87', petalWidth: '0.82' },
                { feature: '萼片宽度', sepalLength: '-0.12', sepalWidth: '1.00', petalLength: '-0.43', petalWidth: '-0.37' },
                { feature: '花瓣长度', sepalLength: '0.87', sepalWidth: '-0.43', petalLength: '1.00', petalWidth: '0.96' },
                { feature: '花瓣宽度', sepalLength: '0.82', sepalWidth: '-0.37', petalLength: '0.96', petalWidth: '1.00' }
            ],

            // 特征向量（主成分）
            eigenvectors: [
                { component: 'PC1', sepalLength: '0.52', sepalWidth: '-0.27', petalLength: '0.58', petalWidth: '0.56' },
                { component: 'PC2', sepalLength: '0.38', sepalWidth: '0.92', petalLength: '-0.02', petalWidth: '-0.06' },
                { component: 'PC3', sepalLength: '0.72', sepalWidth: '-0.24', petalLength: '-0.67', petalWidth: '-0.12' },
                { component: 'PC4', sepalLength: '0.26', sepalWidth: '-0.12', petalLength: '0.45', petalWidth: '-0.82' }
            ],

            // 方差解释比例
            explainedVariance: [
                { component: 'PC1', eigenvalue: '2.92', variance: '72.96', cumulative: '72.96' },
                { component: 'PC2', eigenvalue: '0.92', variance: '23.10', cumulative: '96.06' },
                { component: 'PC3', eigenvalue: '0.15', variance: '3.68', cumulative: '99.74' },
                { component: 'PC4', eigenvalue: '0.01', variance: '0.26', cumulative: '100.00' }
            ],

            // 选择的主成分数量
            selectedComponents: 2,

            // 投影数据预览
            projectedDataPreview: [
                { pc1: '2.68', pc2: '0.32', species: 'Setosa' },
                { pc1: '-0.63', pc2: '-0.18', species: 'Versicolor' },
                { pc1: '-2.09', pc2: '0.53', species: 'Virginica' },
                { pc1: '2.71', pc2: '0.17', species: 'Setosa' },
                { pc1: '-0.32', pc2: '-0.02', species: 'Versicolor' }
            ],

            // 生成完整数据集
            completeIrisData: [],
            standardizedData: [],
            projectedData: [],

            // 测验回答
            quizAnswer: null,
            quizAttempts: 0
        };
    },
    methods: {
        // 分析步骤导航
        nextStep() {
            if (this.currentStep < this.steps.length - 1) {
                this.currentStep++;
                this.$nextTick(() => {
                    this.updateVisualizations();
                });
            }
        },

        prevStep() {
            if (this.currentStep > 0) {
                this.currentStep--;
                this.$nextTick(() => {
                    this.updateVisualizations();
                });
            }
        },

        // 更新可视化
        updateVisualizations() {
            switch (this.currentStep) {
                case 0:
                    this.createCorrelationHeatmap();
                    break;
                case 1:
                    this.createPreprocessingViz();
                    break;
                case 2:
                    this.createEigenvaluesViz();
                    break;
                case 3:
                    this.createScreePlot();
                    break;
                case 4:
                    this.createProjectionViz();
                    break;
                case 5:
                    this.createLoadingsPlot();
                    break;
            }
        },

        // 数据生成
        generateCompleteData() {
            // 生成完整的鸢尾花数据集（模拟）
            const speciesCount = 50; // 每个品种50个样本
            this.completeIrisData = [];

            // Setosa品种
            for (let i = 0; i < speciesCount; i++) {
                this.completeIrisData.push({
                    sepalLength: 5 + 0.5 * this.randomNormal(),
                    sepalWidth: 3.5 + 0.4 * this.randomNormal(),
                    petalLength: 1.5 + 0.3 * this.randomNormal(),
                    petalWidth: 0.2 + 0.1 * this.randomNormal(),
                    species: 'Setosa'
                });
            }

            // Versicolor品种
            for (let i = 0; i < speciesCount; i++) {
                this.completeIrisData.push({
                    sepalLength: 6 + 0.5 * this.randomNormal(),
                    sepalWidth: 2.7 + 0.3 * this.randomNormal(),
                    petalLength: 4.2 + 0.5 * this.randomNormal(),
                    petalWidth: 1.3 + 0.2 * this.randomNormal(),
                    species: 'Versicolor'
                });
            }

            // Virginica品种
            for (let i = 0; i < speciesCount; i++) {
                this.completeIrisData.push({
                    sepalLength: 6.5 + 0.6 * this.randomNormal(),
                    sepalWidth: 3 + 0.4 * this.randomNormal(),
                    petalLength: 5.5 + 0.6 * this.randomNormal(),
                    petalWidth: 2 + 0.3 * this.randomNormal(),
                    species: 'Virginica'
                });
            }

            // 生成标准化数据
            this.standardizeData();

            // 生成投影数据
            this.projectData();
        },

        randomNormal() {
            // Box-Muller变换生成标准正态分布随机数
            const u1 = Math.random();
            const u2 = Math.random();

            return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        },

        standardizeData() {
            // 计算每个特征的均值和标准差
            const features = ['sepalLength', 'sepalWidth', 'petalLength', 'petalWidth'];
            const means = {};
            const stdDevs = {};

            features.forEach(feature => {
                const values = this.completeIrisData.map(d => d[feature]);
                means[feature] = d3.mean(values);
                stdDevs[feature] = d3.deviation(values);
            });

            // 标准化数据
            this.standardizedData = this.completeIrisData.map(d => {
                const standardized = { species: d.species };

                features.forEach(feature => {
                    standardized[feature] = (d[feature] - means[feature]) / stdDevs[feature];
                });

                return standardized;
            });
        },

        projectData() {
            // 使用预设的特征向量将标准化数据投影到主成分空间
            // 注意：这里使用的是模拟数据，实际应用中应该基于计算得到的特征向量

            const eigenVectors = [
                // PC1
                { sepalLength: 0.52, sepalWidth: -0.27, petalLength: 0.58, petalWidth: 0.56 },
                // PC2
                { sepalLength: 0.38, sepalWidth: 0.92, petalLength: -0.02, petalWidth: -0.06 },
                // PC3
                { sepalLength: 0.72, sepalWidth: -0.24, petalLength: -0.67, petalWidth: -0.12 },
                // PC4
                { sepalLength: 0.26, sepalWidth: -0.12, petalLength: 0.45, petalWidth: -0.82 }
            ];

            this.projectedData = this.standardizedData.map(d => {
                const projected = { species: d.species };

                for (let i = 0; i < eigenVectors.length; i++) {
                    const vector = eigenVectors[i];
                    const pc = `pc${i + 1}`;

                    projected[pc] =
                        d.sepalLength * vector.sepalLength +
                        d.sepalWidth * vector.sepalWidth +
                        d.petalLength * vector.petalLength +
                        d.petalWidth * vector.petalWidth;
                }

                return projected;
            });
        },

        // 可视化创建函数
        createCorrelationHeatmap() {
            // 清除容器
            d3.select(this.$refs.correlationHeatmap).selectAll("*").remove();

            // 设置尺寸和边距
            const width = 300;
            const height = 300;
            const margin = { top: 30, right: 30, bottom: 50, left: 80 };
            const cellSize = 50;

            // 特征和相关系数
            const features = ['萼片长度', '萼片宽度', '花瓣长度', '花瓣宽度'];
            const correlationMatrix = [
                [1.00, -0.12, 0.87, 0.82],
                [-0.12, 1.00, -0.43, -0.37],
                [0.87, -0.43, 1.00, 0.96],
                [0.82, -0.37, 0.96, 1.00]
            ];

            // 创建SVG
            const svg = d3.select(this.$refs.correlationHeatmap)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 创建颜色比例尺
            const colorScale = d3.scaleLinear()
                .domain([-1, 0, 1])
                .range(["#4575b4", "#f7f7f7", "#d73027"]);

            // 绘制相关性热图
            for (let i = 0; i < features.length; i++) {
                for (let j = 0; j < features.length; j++) {
                    svg.append("rect")
                        .attr("x", margin.left + j * cellSize)
                        .attr("y", margin.top + i * cellSize)
                        .attr("width", cellSize)
                        .attr("height", cellSize)
                        .style("fill", colorScale(correlationMatrix[i][j]));

                    svg.append("text")
                        .attr("x", margin.left + j * cellSize + cellSize / 2)
                        .attr("y", margin.top + i * cellSize + cellSize / 2)
                        .attr("text-anchor", "middle")
                        .attr("dominant-baseline", "middle")
                        .style("font-size", "12px")
                        .style("fill", Math.abs(correlationMatrix[i][j]) > 0.5 ? "white" : "black")
                        .text(correlationMatrix[i][j].toFixed(2));
                }
            }

            // 添加行标签
            for (let i = 0; i < features.length; i++) {
                svg.append("text")
                    .attr("x", margin.left - 5)
                    .attr("y", margin.top + i * cellSize + cellSize / 2)
                    .attr("text-anchor", "end")
                    .attr("dominant-baseline", "middle")
                    .style("font-size", "12px")
                    .text(features[i]);
            }

            // 添加列标签
            for (let j = 0; j < features.length; j++) {
                svg.append("text")
                    .attr("x", margin.left + j * cellSize + cellSize / 2)
                    .attr("y", margin.top - 5)
                    .attr("text-anchor", "middle")
                    .style("font-size", "12px")
                    .text(features[j]);
            }

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text("特征相关性热图");

            // 添加颜色图例
            const legendWidth = 200;
            const legendHeight = 20;

            const legendX = (width - legendWidth) / 2;
            const legendY = height - 20;

            const legendScale = d3.scaleLinear()
                .domain([-1, 0, 1])
                .range([0, legendWidth / 2, legendWidth]);

            const legendAxis = d3.axisBottom(legendScale)
                .tickValues([-1, -0.5, 0, 0.5, 1])
                .tickFormat(d3.format(".1f"));

            // 绘制渐变图例
            for (let i = 0; i < legendWidth; i++) {
                const t = i / legendWidth;
                d3.interpolateRgb("#4575b4", "#f7f7f7", "#d73027")(t);

                svg.append("rect")
                    .attr("x", legendX + i)
                    .attr("y", legendY)
                    .attr("width", 1)
                    .attr("height", legendHeight)
                    .style("fill", colorScale(-1 + t * 2));
            }

            // 添加图例轴
            svg.append("g")
                .attr("transform", `translate(${legendX}, ${legendY + legendHeight})`)
                .call(legendAxis);
        },

        createPreprocessingViz() {
            // 清除容器
            d3.select(this.$refs.preprocessingViz).selectAll("*").remove();

            // 设置尺寸和边距
            const width = 700;
            const height = 300;
            const margin = { top: 40, right: 120, bottom: 60, left: 60 };

            // 创建SVG
            const svg = d3.select(this.$refs.preprocessingViz)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 绘图区域
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 生成数据
            if (!this.completeIrisData.length) {
                this.generateCompleteData();
            }

            // 选择两个要展示的特征
            const feature1 = 'sepalLength';
            const feature2 = 'petalLength';

            // 创建比例尺（原始数据）
            const x1Extent = d3.extent(this.completeIrisData, d => d[feature1]);
            const y1Extent = d3.extent(this.completeIrisData, d => d[feature2]);

            const x1Scale = d3.scaleLinear()
                .domain([x1Extent[0] - 0.5, x1Extent[1] + 0.5])
                .range([0, plotWidth / 2]);

            const y1Scale = d3.scaleLinear()
                .domain([y1Extent[0] - 0.5, y1Extent[1] + 0.5])
                .range([plotHeight, 0]);

            // 创建比例尺（标准化数据）
            const x2Extent = d3.extent(this.standardizedData, d => d[feature1]);
            const y2Extent = d3.extent(this.standardizedData, d => d[feature2]);

            const x2Scale = d3.scaleLinear()
                .domain([x2Extent[0] - 0.5, x2Extent[1] + 0.5])
                .range([plotWidth / 2 + 30, plotWidth]);

            const y2Scale = d3.scaleLinear()
                .domain([y2Extent[0] - 0.5, y2Extent[1] + 0.5])
                .range([plotHeight, 0]);

            // 创建颜色比例尺
            const colorScale = d3.scaleOrdinal()
                .domain(['Setosa', 'Versicolor', 'Virginica'])
                .range(['#4daf4a', '#377eb8', '#e41a1c']);

            // 创建图表组
            const g = svg.append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // 绘制原始数据点
            g.selectAll(".original-point")
                .data(this.completeIrisData)
                .enter()
                .append("circle")
                .attr("class", "original-point")
                .attr("cx", d => x1Scale(d[feature1]))
                .attr("cy", d => y1Scale(d[feature2]))
                .attr("r", 3)
                .style("fill", d => colorScale(d.species))
                .style("opacity", 0.7);

            // 绘制标准化数据点
            g.selectAll(".standardized-point")
                .data(this.standardizedData)
                .enter()
                .append("circle")
                .attr("class", "standardized-point")
                .attr("cx", d => x2Scale(d[feature1]))
                .attr("cy", d => y2Scale(d[feature2]))
                .attr("r", 3)
                .style("fill", d => colorScale(d.species))
                .style("opacity", 0.7);

            // 添加X轴（原始数据）
            g.append("g")
                .attr("transform", `translate(0, ${plotHeight})`)
                .call(d3.axisBottom(x1Scale));

            // 添加Y轴（原始数据）
            g.append("g")
                .call(d3.axisLeft(y1Scale));

            // 添加X轴（标准化数据）
            g.append("g")
                .attr("transform", `translate(0, ${plotHeight})`)
                .call(d3.axisBottom(x2Scale));

            // 添加Y轴（标准化数据）
            g.append("g")
                .attr("transform", `translate(${plotWidth / 2 + 30}, 0)`)
                .call(d3.axisLeft(y2Scale));

            // 添加标题
            g.append("text")
                .attr("x", plotWidth / 4)
                .attr("y", -15)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text("原始数据");

            g.append("text")
                .attr("x", plotWidth / 2 + 30 + plotWidth / 4)
                .attr("y", -15)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text("标准化后数据");

            // 添加坐标轴标签
            g.append("text")
                .attr("x", plotWidth / 4)
                .attr("y", plotHeight + 40)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("萼片长度");

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -plotHeight / 2)
                .attr("y", -40)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("花瓣长度");

            g.append("text")
                .attr("x", plotWidth / 2 + 30 + plotWidth / 4)
                .attr("y", plotHeight + 40)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("萼片长度 (标准化)");

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -plotHeight / 2)
                .attr("y", plotWidth / 2 + 10)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("花瓣长度 (标准化)");

            // 添加图例
            const legend = svg.append("g")
                .attr("transform", `translate(${width - margin.right + 20}, ${margin.top})`);

            ['Setosa', 'Versicolor', 'Virginica'].forEach((species, i) => {
                legend.append("circle")
                    .attr("cx", 10)
                    .attr("cy", i * 25 + 10)
                    .attr("r", 6)
                    .style("fill", colorScale(species));

                legend.append("text")
                    .attr("x", 25)
                    .attr("y", i * 25 + 10)
                    .attr("dy", "0.35em")
                    .style("font-size", "12px")
                    .text(species);
            });
        },

        createEigenvaluesViz() {
            // 清除容器
            d3.select(this.$refs.eigenvaluesViz).selectAll("*").remove();

            // 设置尺寸和边距
            const width = 400;
            const height = 200;
            const margin = { top: 30, right: 30, bottom: 40, left: 50 };

            // 创建SVG
            const svg = d3.select(this.$refs.eigenvaluesViz)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 绘图区域
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 创建数据
            const eigenvalues = this.explainedVariance.map(d => ({
                component: d.component,
                value: parseFloat(d.eigenvalue)
            }));

            // 创建X比例尺
            const xScale = d3.scaleBand()
                .domain(eigenvalues.map(d => d.component))
                .range([0, plotWidth])
                .padding(0.3);

            // 创建Y比例尺
            const yScale = d3.scaleLinear()
                .domain([0, d3.max(eigenvalues, d => d.value) * 1.1])
                .range([plotHeight, 0]);

            // 创建图表组
            const g = svg.append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // 绘制条形
            g.selectAll(".bar")
                .data(eigenvalues)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", d => xScale(d.component))
                .attr("y", d => yScale(d.value))
                .attr("width", xScale.bandwidth())
                .attr("height", d => plotHeight - yScale(d.value))
                .style("fill", "#69b3a2");

            // 添加数值标签
            g.selectAll(".value-label")
                .data(eigenvalues)
                .enter()
                .append("text")
                .attr("class", "value-label")
                .attr("x", d => xScale(d.component) + xScale.bandwidth() / 2)
                .attr("y", d => yScale(d.value) - 5)
                .attr("text-anchor", "middle")
                .style("font-size", "10px")
                .text(d => d.value.toFixed(2));

            // 添加X轴
            g.append("g")
                .attr("transform", `translate(0, ${plotHeight})`)
                .call(d3.axisBottom(xScale));

            // 添加Y轴
            g.append("g")
                .call(d3.axisLeft(yScale));

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text("特征值分布");

            // 添加坐标轴标签
            g.append("text")
                .attr("x", plotWidth / 2)
                .attr("y", plotHeight + 35)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("主成分");

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -plotHeight / 2)
                .attr("y", -35)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("特征值");
        },

        createScreePlot() {
            // 清除容器
            d3.select(this.$refs.screePlot).selectAll("*").remove();

            // 设置尺寸和边距
            const width = 500;
            const height = 300;
            const margin = { top: 30, right: 30, bottom: 50, left: 60 };

            // 创建SVG
            const svg = d3.select(this.$refs.screePlot)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 绘图区域
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 创建数据
            const varianceData = this.explainedVariance.map(d => ({
                component: d.component,
                variance: parseFloat(d.variance),
                cumulative: parseFloat(d.cumulative)
            }));

            // 创建X比例尺
            const xScale = d3.scaleBand()
                .domain(varianceData.map(d => d.component))
                .range([0, plotWidth])
                .padding(0.3);

            // 创建Y比例尺（方差百分比）
            const yScaleVariance = d3.scaleLinear()
                .domain([0, 100])
                .range([plotHeight, 0]);

            // 创建Y2比例尺（累计方差）
            const yScaleCumulative = d3.scaleLinear()
                .domain([0, 100])
                .range([plotHeight, 0]);

            // 创建图表组
            const g = svg.append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // 绘制条形（方差百分比）
            g.selectAll(".bar")
                .data(varianceData)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", d => xScale(d.component))
                .attr("y", d => yScaleVariance(d.variance))
                .attr("width", xScale.bandwidth())
                .attr("height", d => plotHeight - yScaleVariance(d.variance))
                .style("fill", "#69b3a2");

            // 绘制折线（累计方差）
            const line = d3.line()
                .x(d => xScale(d.component) + xScale.bandwidth() / 2)
                .y(d => yScaleCumulative(d.cumulative));

            g.append("path")
                .datum(varianceData)
                .attr("class", "line")
                .attr("fill", "none")
                .attr("stroke", "#e63946")
                .attr("stroke-width", 2)
                .attr("d", line);

            // 添加累计方差点
            g.selectAll(".cumulative-point")
                .data(varianceData)
                .enter()
                .append("circle")
                .attr("class", "cumulative-point")
                .attr("cx", d => xScale(d.component) + xScale.bandwidth() / 2)
                .attr("cy", d => yScaleCumulative(d.cumulative))
                .attr("r", 4)
                .style("fill", "#e63946");

            // 添加方差标签
            g.selectAll(".variance-label")
                .data(varianceData)
                .enter()
                .append("text")
                .attr("class", "variance-label")
                .attr("x", d => xScale(d.component) + xScale.bandwidth() / 2)
                .attr("y", d => yScaleVariance(d.variance) - 5)
                .attr("text-anchor", "middle")
                .style("font-size", "10px")
                .text(d => d.variance.toFixed(1) + "%");

            // 添加累计方差标签
            g.selectAll(".cumulative-label")
                .data(varianceData)
                .enter()
                .append("text")
                .attr("class", "cumulative-label")
                .attr("x", d => xScale(d.component) + xScale.bandwidth() / 2)
                .attr("y", d => yScaleCumulative(d.cumulative) - 10)
                .attr("text-anchor", "middle")
                .style("font-size", "10px")
                .style("fill", "#e63946")
                .text(d => d.cumulative.toFixed(1) + "%");

            // 添加X轴
            g.append("g")
                .attr("transform", `translate(0, ${plotHeight})`)
                .call(d3.axisBottom(xScale));

            // 添加Y轴（方差百分比）
            g.append("g")
                .call(d3.axisLeft(yScaleVariance).ticks(5).tickFormat(d => d + "%"));

            // 添加Y2轴（累计方差）
            g.append("g")
                .attr("transform", `translate(${plotWidth}, 0)`)
                .call(d3.axisRight(yScaleCumulative).ticks(5).tickFormat(d => d + "%"));

            // 添加阈值线（95%）
            const thresholdValue = 95;
            g.append("line")
                .attr("class", "threshold-line")
                .attr("x1", 0)
                .attr("y1", yScaleCumulative(thresholdValue))
                .attr("x2", plotWidth)
                .attr("y2", yScaleCumulative(thresholdValue))
                .style("stroke", "#aaa")
                .style("stroke-width", 1)
                .style("stroke-dasharray", "5,5");

            g.append("text")
                .attr("class", "threshold-label")
                .attr("x", 5)
                .attr("y", yScaleCumulative(thresholdValue) - 5)
                .style("font-size", "10px")
                .style("fill", "#666")
                .text("95%阈值");

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text("碎石图：方差解释比例");

            // 添加坐标轴标签
            g.append("text")
                .attr("x", plotWidth / 2)
                .attr("y", plotHeight + 40)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("主成分");

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -plotHeight / 2)
                .attr("y", -40)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .text("方差百分比 (%)");

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -plotHeight / 2)
                .attr("y", plotWidth + 25)
                .attr("text-anchor", "middle")
                .style("font-size", "12px")
                .style("fill", "#e63946")
                .text("累计方差百分比 (%)");

            // 添加图例
            const legend = svg.append("g")
                .attr("transform", `translate(${margin.left + 20}, ${height - 20})`);

            // 方差百分比图例
            legend.append("rect")
                .attr("x", 0)
                .attr("y", -15)
                .attr("width", 15)
                .attr("height", 15)
                .style("fill", "#69b3a2");

            legend.append("text")
                .attr("x", 20)
                .attr("y", -5)
                .style("font-size", "12px")
                .text("各主成分方差");

            // 累计方差图例
            legend.append("line")
                .attr("x1", 120)
                .attr("y1", -7.5)
                .attr("x2", 135)
                .attr("y2", -7.5)
                .style("stroke", "#e63946")
                .style("stroke-width", 2);

            legend.append("circle")
                .attr("cx", 127.5)
                .attr("cy", -7.5)
                .attr("r", 4)
                .style("fill", "#e63946");

            legend.append("text")
                .attr("x", 140)
                .attr("y", -5)
                .style("font-size", "12px")
                .text("累计方差");
        },

        updateProjection() {
            // 更新投影可视化
            if (this.currentStep === 4) {
                this.createProjectionViz();
            }
        },

        createProjectionViz() {
            // 清除容器
            d3.select(this.$refs.projectionViz).selectAll("*").remove();

            // 设置尺寸和边距
            const width = 500;
            const height = 400;
            const margin = { top: 40, right: 30, bottom: 50, left: 60 };

            // 创建SVG
            const svg = d3.select(this.$refs.projectionViz)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 绘图区域
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 创建图表组
            const g = svg.append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // 确定要绘制的主成分
            let xPC = 'pc1';
            let yPC = this.selectedComponents >= 2 ? 'pc2' : null;

            if (this.selectedComponents === 1) {
                // 一维投影：在y轴上随机抖动
                this.projectedData.forEach(d => {
                    d.jitter = Math.random() * 2 - 1;  // 随机值，范围[-1, 1]
                });
            }

            // 创建X比例尺
            const xExtent = d3.extent(this.projectedData, d => d[xPC]);
            const xPadding = (xExtent[1] - xExtent[0]) * 0.1;

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - xPadding, xExtent[1] + xPadding])
                .range([0, plotWidth]);

            // 创建Y比例尺
            let yScale;
            if (this.selectedComponents >= 2) {
                const yExtent = d3.extent(this.projectedData, d => d[yPC]);
                const yPadding = (yExtent[1] - yExtent[0]) * 0.1;

                yScale = d3.scaleLinear()
                    .domain([yExtent[0] - yPadding, yExtent[1] + yPadding])
                    .range([plotHeight, 0]);
            } else {
                // 一维投影：y轴只用于抖动
                yScale = d3.scaleLinear()
                    .domain([-1.5, 1.5])
                    .range([plotHeight, 0]);
            }

            // 创建颜色比例尺
            const colorScale = d3.scaleOrdinal()
                .domain(['Setosa', 'Versicolor', 'Virginica'])
                .range(['#4daf4a', '#377eb8', '#e41a1c']);

            // 绘制数据点
            g.selectAll(".data-point")
                .data(this.projectedData)
                .enter()
                .append("circle")
                .attr("class", "data-point")
                .attr("cx", d => xScale(d[xPC]))
                .attr("cy", d => {
                    if (this.selectedComponents >= 2) {
                        return yScale(d[yPC]);
                    } else {
                        return yScale(d.jitter);
                    }
                })
                .attr("r", 5)
                .style("fill", d => colorScale(d.species))
                .style("opacity", 0.7);

            // 添加轴和标签
            if (this.selectedComponents === 1) {
                // 一维投影：只显示x轴
                g.append("g")
                    .attr("transform", `translate(0, ${plotHeight / 2})`)
                    .call(d3.axisBottom(xScale));

                g.append("text")
                    .attr("x", plotWidth / 2)
                    .attr("y", plotHeight / 2 + 40)
                    .attr("text-anchor", "middle")
                    .style("font-size", "12px")
                    .text("第一主成分 (PC1)");

                // 添加说明
                g.append("text")
                    .attr("x", plotWidth / 2)
                    .attr("y", plotHeight - 20)
                    .attr("text-anchor", "middle")
                    .style("font-size", "12px")
                    .style("font-style", "italic")
                    .text("(垂直方向为随机抖动，仅用于可视化)");
            } else {
                // 二维或更高维投影
                g.append("g")
                    .attr("transform", `translate(0, ${plotHeight})`)
                    .call(d3.axisBottom(xScale));

                g.append("g")
                    .call(d3.axisLeft(yScale));

                g.append("text")
                    .attr("x", plotWidth / 2)
                    .attr("y", plotHeight + 40)
                    .attr("text-anchor", "middle")
                    .style("font-size", "12px")
                    .text("第一主成分 (PC1)");

                g.append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("x", -plotHeight / 2)
                    .attr("y", -40)
                    .attr("text-anchor", "middle")
                    .style("font-size", "12px")
                    .text("第二主成分 (PC2)");
            }

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text(`投影到前${this.selectedComponents}个主成分的鸢尾花数据`);

            // 添加图例
            const legend = svg.append("g")
                .attr("transform", `translate(${plotWidth + margin.left - 20}, ${margin.top})`);

            ['Setosa', 'Versicolor', 'Virginica'].forEach((species, i) => {
                legend.append("circle")
                    .attr("cx", 10)
                    .attr("cy", i * 25 + 10)
                    .attr("r", 6)
                    .style("fill", colorScale(species));

                legend.append("text")
                    .attr("x", 25)
                    .attr("y", i * 25 + 10)
                    .attr("dy", "0.35em")
                    .style("font-size", "12px")
                    .text(species);
            });
        },

        createLoadingsPlot() {
            // 清除容器
            d3.select(this.$refs.loadingsPlot).selectAll("*").remove();

            // 设置尺寸和边距
            const width = 400;
            const height = 400;
            const margin = { top: 40, right: 30, bottom: 50, left: 60 };

            // 创建SVG
            const svg = d3.select(this.$refs.loadingsPlot)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 绘图区域
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 提取前两个主成分的系数
            const loadings = [
                { feature: '萼片长度', pc1: 0.52, pc2: 0.38 },
                { feature: '萼片宽度', pc1: -0.27, pc2: 0.92 },
                { feature: '花瓣长度', pc1: 0.58, pc2: -0.02 },
                { feature: '花瓣宽度', pc1: 0.56, pc2: -0.06 }
            ];

            // 创建比例尺
            const xScale = d3.scaleLinear()
                .domain([-1, 1])
                .range([0, plotWidth]);

            const yScale = d3.scaleLinear()
                .domain([-1, 1])
                .range([plotHeight, 0]);

            // 创建图表组
            const g = svg.append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // 绘制参考线
            g.append("line")  // 水平线
                .attr("x1", 0)
                .attr("y1", yScale(0))
                .attr("x2", plotWidth)
                .attr("y2", yScale(0))
                .style("stroke", "#ddd")
                .style("stroke-width", 1);

            g.append("line")  // 垂直线
                .attr("x1", xScale(0))
                .attr("y1", 0)
                .attr("x2", xScale(0))
                .attr("y2", plotHeight)
                .style("stroke", "#ddd")
                .style("stroke-width", 1);

            // 绘制加载向量
            g.selectAll(".loading-vector")
                .data(loadings)
                .enter()
                .append("line")
                .attr("class", "loading-vector")
                .attr("x1", xScale(0))
                .attr("y1", yScale(0))
                .attr("x2", d => xScale(d.pc1))
                .attr("y2", d => yScale(d.pc2))
                .style("stroke", "#69b3a2")
                .style("stroke-width", 2);

            // 添加特征标签
            g.selectAll(".feature-label")
                .data(loadings)
                .enter()
                .append("text")
                .attr("class", "feature-label")
                .attr("x", d => xScale(d.pc1 * 1.1))
                .attr("y", d => yScale(d.pc2 * 1.1))
                .attr("text-anchor", d => d.pc1 > 0 ? "start" : "end")
                .style("font-size", "12px")
                .text(d => d.feature);

            // 添加箭头
            g.selectAll(".arrow-head")
                .data(loadings)
                .enter()
                .append("circle")
                .attr("class", "arrow-head")
                .attr("cx", d => xScale(d.pc1))
                .attr("cy", d => yScale(d.pc2))
                .attr("r", 4)
                .style("fill", "#69b3a2");

            // 添加X轴
            g.append("g")
                .attr("transform", `translate(0, ${yScale(0)})`)
                .call(d3.axisBottom(xScale).ticks(5));

            // 添加Y轴
            g.append("g")
                .attr("transform", `translate(${xScale(0)}, 0)`)
                .call(d3.axisLeft(yScale).ticks(5));

            // 添加轴标签
            g.append("text")
                .attr("x", plotWidth)
                .attr("y", yScale(0) + 30)
                .attr("text-anchor", "end")
                .style("font-size", "12px")
                .text("第一主成分 (PC1)");

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -10)
                .attr("y", xScale(0) - 30)
                .attr("text-anchor", "end")
                .style("font-size", "12px")
                .text("第二主成分 (PC2)");

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .style("font-size", "14px")
                .style("font-weight", "bold")
                .text("特征加载图 (Loading Plot)");

            // 添加单位圆
            g.append("circle")
                .attr("cx", xScale(0))
                .attr("cy", yScale(0))
                .attr("r", (xScale(1) - xScale(0)))
                .style("fill", "none")
                .style("stroke", "#aaa")
                .style("stroke-dasharray", "3,3");
        },

        checkAnswer() {
            this.quizAttempts++;

            // 正确答案是选项2
            const correctAnswer = 2;
            // 向父组件发送答案提交事件
            this.$emit('answer-submitted', this.quizAnswer);

            if (this.quizAnswer === correctAnswer) {
                // 回答正确
                this.$refs.baseSegment.showResponse(
                    "回答正确！",
                    "根据我们的分析，前两个主成分确实能解释数据超过90%的方差（具体为96.06%）。这说明PCA在保留鸢尾花数据主要信息的同时，有效地降低了数据维度。",
                    "success"
                );

                // 标记本节完成
                setTimeout(() => {
                    this.$refs.baseSegment.completeSegment();
                }, 200);
            } else {
                // 回答错误
                let hint = "";
                if (this.quizAttempts >= 2) {
                    hint = "提示：不能仅凭特征向量（主成分方向）的绝对值大小直接判断原始特征的重要性​​，需要结合特征值和具体分析。查看碎石图中的累计方差百分比，前两个主成分累计解释了多少方差？";
                }

                this.$refs.baseSegment.showResponse(
                    "回答不正确",
                    `请仔细回顾PCA分析结果。${hint}`,
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
        // 生成完整数据集
        this.generateCompleteData();

        // 初始化第一步的可视化
        this.$nextTick(() => {
            this.createCorrelationHeatmap();
        });
    },
    beforeDestroy() {
        // 清理D3资源
        const containers = [
            this.$refs.correlationHeatmap,
            this.$refs.preprocessingViz,
            this.$refs.eigenvaluesViz,
            this.$refs.screePlot,
            this.$refs.projectionViz,
            this.$refs.loadingsPlot
        ];

        containers.forEach(container => {
            if (container) {
                d3.select(container).selectAll("*").remove();
            }
        });
    }
}
</script>

<style scoped>
.practical-interactive {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.dataset-description {
    margin-bottom: 20px;
    background-color: #f5f7fa;
    border-radius: 4px;
    padding: 15px;
}

.dataset-preview {
    margin-top: 15px;
}

.analysis-steps {
    margin: 30px 0;
}

.step-content {
    margin-top: 30px;
    padding: 15px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
}

.stats-container,
.preprocessing-container,
.pca-computation-container,
.component-selection-container,
.projection-container,
.interpretation-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 20px 0;
}

.stats-card,
.correlation-matrix,
.preprocessing-explanation,
.covariance-matrix,
.eigenvalues,
.eigenvectors,
.explained-variance,
.projection-explanation,
.interpretation-explanation {
    flex: 1;
    min-width: 300px;
}

.correlation-heatmap,
.preprocessing-viz,
.eigenvalues-viz,
.scree-plot,
.projection-viz,
.loadings-plot {
    width: 100%;
    margin: 10px 0;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    display: flex;
    justify-content: center;
}

.data-insight,
.variance-insight,
.dimension-reduction,
.result-summary {
    margin-top: 20px;
    padding: 10px;
    background-color: #ecf5ff;
    border-left: 4px solid #409EFF;
    border-radius: 4px;
}

.component-selection {
    margin: 20px 0;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    text-align: center;
}

.step-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}

.case-quiz {
    margin-top: 30px;
    padding: 20px;
    background-color: #ecf5ff;
    border-radius: 4px;
}

.quiz-question {
    margin-top: 15px;
}

.quiz-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 15px 0;
}

.submit-answer {
    margin-top: 15px;
}
</style>