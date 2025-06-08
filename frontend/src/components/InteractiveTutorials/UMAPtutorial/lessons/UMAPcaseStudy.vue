<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>11. UMAP案例分析</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 案例分析 -->
            <div class="interaction-container">
                <h3>案例研究：单细胞基因表达数据分析</h3>
                <p>这个案例展示了UMAP在分析单细胞RNA测序数据中的应用。您可以交互式地探索数据，尝试不同的参数设置，并观察其对结果的影响。</p>

                <div class="case-study">
                    <div class="case-description">
                        <div class="case-header">
                            <i class="el-icon-s-data"></i>
                            <h4>背景</h4>
                        </div>
                        <p>我们有一个来自小鼠大脑的单细胞RNA测序数据集，包含5,000个细胞和15,000个基因。研究目标是识别不同的细胞类型并探索它们之间的关系。</p>
                        <p>数据特点：</p>
                        <ul>
                            <li>高维度（15,000个基因表达值）</li>
                            <li>数据稀疏（大多数基因在大多数细胞中不表达）</li>
                            <li>存在技术噪声和批次效应</li>
                            <li>包含多种未知的细胞类型</li>
                        </ul>
                    </div>

                    <div class="analysis-workflow">
                        <div class="workflow-header">
                            <i class="el-icon-share"></i>
                            <h4>分析流程</h4>
                        </div>
                        <el-steps direction="horizontal" :active="activeStep">
                            <el-step v-for="(step, index) in workflowSteps" :key="index" :title="step.title"
                                :description="step.shortDesc">
                            </el-step>
                        </el-steps>

                        <div class="step-navigation">
                            <el-button type="primary" icon="el-icon-arrow-left" :disabled="activeStep <= 0"
                                @click="prevStep">
                                上一步
                            </el-button>
                            <el-button type="primary" @click="nextStep"
                                :disabled="activeStep >= workflowSteps.length - 1">
                                下一步 <i class="el-icon-arrow-right"></i>
                            </el-button>
                        </div>
                    </div>

                    <div class="step-detail">
                        <h4>{{ workflowSteps[activeStep].title }}</h4>
                        <div class="step-description" v-html="workflowSteps[activeStep].description"></div>

                        <!-- <div class="step-visualization" ref="stepVisualization"></div> -->

                        <!-- <div v-if="activeStep === 3" class="parameter-controls">
                            <h5>尝试调整UMAP参数</h5>
                            <div class="parameter-sliders">
                                <div class="parameter-item">
                                    <span>n_neighbors:</span>
                                    <el-slider v-model="nNeighbors" :min="5" :max="50" :step="5"
                                        @change="updateVisualization"></el-slider>
                                    <div class="parameter-value">{{ nNeighbors }}</div>
                                </div>
                                <div class="parameter-item">
                                    <span>min_dist:</span>
                                    <el-slider v-model="minDist" :min="0" :max="1" :step="0.1"
                                        @change="updateVisualization"></el-slider>
                                    <div class="parameter-value">{{ minDist.toFixed(1) }}</div>
                                </div>
                            </div>
                            <div class="parameter-effect" v-html="parameterEffect"></div>
                        </div> -->

                        <div v-if="activeStep === 4" class="interpretation-quiz">
                            <h5>解释结果</h5>
                            <p>根据UMAP结果和细胞类型标记，回答以下问题：</p>

                            <div class="interpretation-question">
                                <p><strong>问题：</strong> UMAP可视化中，哪种细胞类型与神经元(Neurons)关系最密切？</p>
                                <el-radio-group v-model="interpretationAnswer">
                                    <el-radio :label="1">小胶质细胞(Microglia)</el-radio>
                                    <el-radio :label="2">少突胶质细胞前体细胞(OPCs)</el-radio>
                                    <el-radio :label="3">星形胶质细胞(Astrocytes)</el-radio>
                                </el-radio-group>

                                <el-button type="primary" @click="checkInterpretation" :disabled="!interpretationAnswer"
                                    class="submit-btn">
                                    提交答案
                                </el-button>
                            </div>
                        </div>
                    </div>

                    <!-- 解释题回应部分 -->
                    <div v-if="interpretationCompleted" class="interpretation-response">
                        <el-alert :title="interpretationFeedbackTitle"
                            :type="isInterpretationCorrect ? 'success' : 'error'"
                            :description="interpretationFeedbackDescription" show-icon>
                        </el-alert>

                        <div v-if="isInterpretationCorrect || interpretationRetries >= 1" class="completion-section">
                            <p>🎉 恭喜！您已经完成了所有的UMAP教程内容！</p>
                            <div class="completion-message">
                                <h4>学习总结</h4>
                                <p>在这个互动教程中，您学习了：</p>
                                <ul>
                                    <li>UMAP算法的数学原理和工作机制</li>
                                    <li>UMAP与其他降维算法的对比</li>
                                    <li>如何调整关键参数以获得最佳结果</li>
                                    <li>UMAP在不同领域的实际应用</li>
                                    <li>如何实现和优化UMAP</li>
                                    <li>如何解析和解释UMAP结果</li>
                                </ul>
                                <p>您现在已经具备了使用UMAP进行数据分析和可视化的知识和技能。希望这个教程对您的研究和工作有所帮助！</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { marked } from 'marked';
import * as d3 from 'd3';

// 设置渲染器以支持数学公式
import 'katex/dist/katex.min.css';
// import katex from 'katex';
import katex from 'katex';
// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}


export default {
    name: 'Section11CaseStudy',
    data() {
        return {
            markdownContent: `
## UMAP案例分析

在这最后一节中，我们将通过真实案例展示UMAP的应用。这些案例覆盖了不同领域，说明了如何在实际问题中应用UMAP，如何解释结果，以及如何处理常见挑战。通过分析这些案例，您将获得实际应用UMAP的经验和见解。

### 案例研究的价值

案例研究提供了算法应用的上下文，帮助您理解：

1. **适用场景**：何时选择UMAP是合适的
2. **工作流程**：UMAP如何融入整体数据分析流程
3. **参数选择**：如何为特定数据类型选择合适的参数
4. **结果解释**：如何有意义地解读UMAP的降维结果
5. **实际挑战**：如何处理大规模数据、噪声和异常值

### 实际应用中的常见挑战

在实际应用UMAP时，经常面临以下挑战：

- **数据预处理决策**：如何标准化数据？是否需要先进行特征选择？
- **参数选择权衡**：更高的n_neighbors捕获更多全局结构，但可能丢失局部细节
- **结果验证**：如何评估降维结果的质量和可靠性？
- **解释与沟通**：如何向非技术人员解释UMAP结果？
- **集成到分析流程**：如何结合聚类、分类等后续分析？

案例研究将展示这些挑战的实际处理方法，帮助您在自己的项目中做出明智决策。

### 案例研究的类型

本节将重点关注以下案例：

1. **单细胞基因组学案例**：
   - 分析单细胞RNA测序数据
   - 识别细胞类型和发育轨迹
   - 处理高维度、稀疏的生物数据

2. **自然语言处理案例**：
   - 分析文档集合的语义关系
   - 可视化词嵌入
   - 处理高维文本特征向量

3. **图像数据案例**：
   - 分析图像特征空间
   - 探索深度学习模型提取的特征
   - 处理视觉相似性和模式

通过这些案例，我们将展示UMAP在不同数据类型和问题上的多功能性，以及如何调整方法以适应特定需求。

接下来，我们将深入探讨单细胞RNA测序数据分析的案例，这是UMAP最成功和广泛应用的领域之一。您将看到一个完整的工作流程，从原始数据处理到最终的生物学解释。
      `,
            activeStep: 0,
            workflowSteps: [
                {
                    title: "数据质控与预处理",
                    shortDesc: "过滤低质量细胞和低表达基因",
                    description: `
            <p>单细胞RNA测序数据通常包含大量噪声和技术误差。在应用UMAP之前，必须进行充分的质量控制和预处理：</p>
            <ol>
              <li><strong>细胞质控</strong>：移除低质量细胞
                <ul>
                  <li>过滤检测到基因数过少的细胞（可能是空液滴或死细胞）</li>
                  <li>过滤线粒体基因比例过高的细胞（表明细胞受损）</li>
                  <li>移除异常高的总RNA含量细胞（可能是多个细胞）</li>
                </ul>
              </li>
              <li><strong>基因过滤</strong>：保留信息量高的基因
                <ul>
                  <li>移除在极少数细胞中表达的基因</li>
                  <li>移除家务基因（在所有细胞中均匀表达）</li>
                </ul>
              </li>
              <li><strong>数据标准化</strong>：校正技术偏差
                <ul>
                  <li>校正细胞间测序深度差异</li>
                  <li>对数转换以处理表达值的偏态分布</li>
                  <li>批次效应校正（如有多个批次）</li>
                </ul>
              </li>
            </ol>
            <p>这些预处理步骤对后续分析至关重要。在本案例中，5,000个细胞经过质控后保留了4,800个，15,000个基因过滤后保留了2,000个高变异基因。</p>
          `
                },
                {
                    title: "特征选择",
                    shortDesc: "选择高变异基因作为特征",
                    description: `
            <p>单细胞RNA测序数据有成千上万个基因，但并非所有基因都对细胞类型鉴定有用。识别高变异基因可以：</p>
            <ul>
              <li>提高信噪比，专注于生物学相关信号</li>
              <li>减少计算负担，加快降维速度</li>
              <li>减少技术噪声的影响</li>
            </ul>
            <p>特征选择策略：</p>
            <ol>
              <li><strong>计算每个基因的变异性</strong>
                <ul>
                  <li>通常使用<em>变异系数</em>或<em>高斯拟合的残差方差</em></li>
                  <li>控制基因表达水平与变异性的关系</li>
                </ul>
              </li>
              <li><strong>选择顶部高变异基因</strong>
                <ul>
                  <li>通常选择1,000-5,000个最变异的基因</li>
                  <li>本案例中，我们选择了前2,000个高变异基因</li>
                </ul>
              </li>
              <li><strong>排除潜在的压力或批次相关基因</strong>
                <ul>
                  <li>线粒体基因、核糖体基因等可能反映细胞状态而非类型</li>
                </ul>
              </li>
            </ol>
            <p>右图显示了基因表达变异性分析，红色点表示选择的高变异基因，这些基因将作为UMAP输入。</p>
          `
                },
                {
                    title: "降维准备",
                    shortDesc: "PCA预处理以减少噪声和计算量",
                    description: `
            <p>在应用UMAP之前，通常先使用PCA（主成分分析）进行初步降维，这有几个重要原因：</p>
            <ul>
              <li><strong>降低噪声</strong>：PCA保留数据中的主要变异方向，过滤掉次要变异（可能是噪声）</li>
              <li><strong>加速计算</strong>：UMAP在较低维度（如50个PCA主成分）上运行比在原始2,000个基因上快得多</li>
              <li><strong>处理数据稀疏性</strong>：将稀疏矩阵转换为密集主成分表示</li>
            </ul>
            <p>PCA前的数据维度：4,800个细胞 × 2,000个基因</p>
            <p>PCA后的数据维度：4,800个细胞 × 50个主成分</p>
            <p>这种降维预处理在高维生物数据分析中是标准实践，且对最终UMAP结果影响很小，因为PCA保留了数据中的主要变异源。</p>
            <p>右图展示了PCA结果的前两个主成分，可以看到一些细胞群已经开始显现，但群体间的边界仍不清晰。这表明线性降维方法（如PCA）无法充分捕捉单细胞数据的复杂非线性结构，需要UMAP等非线性方法进一步处理。</p>
          `
                },
                {
                    title: "UMAP降维",
                    shortDesc: "将PCA结果映射到2D空间",
                    description: `
            <p>现在我们将PCA降维后的数据（50个主成分）输入UMAP算法，将其映射到2D平面用于可视化和分析。这是工作流中的关键步骤，能够揭示细胞之间的复杂关系。</p>
            <p>UMAP参数选择考虑因素：</p>
            <ul>
              <li><strong>n_neighbors</strong>: 控制关注局部还是全局结构
                <ul>
                  <li>单细胞数据通常使用10-30范围内的值</li>
                  <li>较大值有助于观察细胞类型之间的发育关系</li>
                  <li>较小值有助于分离罕见细胞类型</li>
                </ul>
              </li>
              <li><strong>min_dist</strong>: 控制簇的紧密程度
                <ul>
                  <li>较小值（0.1-0.3）使簇更紧凑，适合细胞类型识别</li>
                  <li>较大值（0.5-0.8）使点分布更均匀，适合观察连续轨迹</li>
                </ul>
              </li>
              <li><strong>metric</strong>: 距离度量选择
                <ul>
                  <li>单细胞数据通常使用"cosine"或"correlation"距离</li>
                  <li>这些度量关注基因表达模式而非绝对水平</li>
                </ul>
              </li>
            </ul>
            <p>右侧的交互式可视化让您可以调整UMAP参数，观察它们如何影响最终结果。尝试不同的参数组合，看看哪一组最能清晰地分离不同细胞类型。</p>
          `
                },
                {
                    title: "结果解释",
                    shortDesc: "细胞类型注释和生物学解读",
                    description: `
            <p>UMAP降维后，我们可以根据已知的细胞类型标记基因，对不同的细胞簇进行注释。右图显示了按细胞类型着色的UMAP结果。</p>
            <p>主要发现：</p>
            <ul>
              <li><strong>清晰的细胞类型分离</strong>: UMAP成功分离了8种主要神经细胞类型</li>
              <li><strong>发育关系保留</strong>: 注意细胞类型之间的空间关系反映了已知的发育关系：
                <ul>
                  <li>少突胶质细胞前体细胞(OPCs)与成熟少突胶质细胞相邻</li>
                  <li>神经元亚型根据区域身份和发育阶段聚集</li>
                </ul>
              </li>
              <li><strong>罕见细胞类型检测</strong>: UMAP成功捕捉了数据中仅占1%的罕见细胞类型(周细胞)</li>
            </ul>
            <p>这些结果使我们能够：</p>
            <ol>
              <li>识别和定量不同细胞类型的比例</li>
              <li>研究基因在不同细胞类型中的表达模式</li>
              <li>发现新的细胞亚型或状态</li>
              <li>重建细胞分化轨迹</li>
            </ol>
            <p>最重要的是，UMAP提供了一个强大的可视化框架，使研究人员能够直观地探索和解读复杂的单细胞数据，得出生物学见解。</p>
          `
                }
            ],
            nNeighbors: 15,
            minDist: 0.3,
            cellData: [],
            svgElement: null,
            interpretationAnswer: null,
            interpretationCompleted: false,
            isInterpretationCorrect: false,
            interpretationRetries: 0,
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
        },
        parameterEffect() {
            let effect = '<p><strong>当前参数效果分析：</strong></p>';

            if (this.nNeighbors <= 10) {
                effect += '<p><strong>n_neighbors = ' + this.nNeighbors + '</strong> (较小值)：当前设置强调局部结构，有助于分离不同的细胞群，但可能会丢失一些全局关系，如细胞发育轨迹。</p>';
            } else if (this.nNeighbors >= 30) {
                effect += '<p><strong>n_neighbors = ' + this.nNeighbors + '</strong> (较大值)：当前设置更强调全局结构，能更好地保留细胞类型之间的发育关系，但可能导致一些罕见细胞类型无法明显分离。</p>';
            } else {
                effect += '<p><strong>n_neighbors = ' + this.nNeighbors + '</strong> (平衡值)：当前设置在保留局部和全局结构之间取得了良好平衡，适合大多数单细胞分析场景。</p>';
            }

            if (this.minDist <= 0.1) {
                effect += '<p><strong>min_dist = ' + this.minDist.toFixed(1) + '</strong> (较小值)：当前设置使细胞簇更加紧凑，有助于清晰区分不同的细胞类型，但可能导致点过度重叠，难以观察簇内结构。</p>';
            } else if (this.minDist >= 0.5) {
                effect += '<p><strong>min_dist = ' + this.minDist.toFixed(1) + '</strong> (较大值)：当前设置使点分布更加均匀，便于观察细胞亚群和连续状态，但可能导致细胞类型边界变得模糊。</p>';
            } else {
                effect += '<p><strong>min_dist = ' + this.minDist.toFixed(1) + '</strong> (平衡值)：当前设置在簇的分离度和可观察性之间取得了良好平衡，适合大多数单细胞分析场景。</p>';
            }

            return effect;
        },
        interpretationFeedbackTitle() {
            return this.isInterpretationCorrect ? '解释正确！' : '请再思考一下';
        },
        interpretationFeedbackDescription() {
            if (this.isInterpretationCorrect) {
                return '正确！少突胶质细胞前体细胞(OPCs)与神经元在发育上有密切关系，它们在UMAP可视化中的相对位置反映了这种关系。';
            }

            switch (this.interpretationAnswer) {
                case 1:
                    return '小胶质细胞是中枢神经系统中的免疫细胞，与神经元的发育关系较远。在UMAP图中，它们通常与神经元簇距离较远。';
                case 3:
                    return '虽然星形胶质细胞与神经元有功能上的相互作用，但在发育谱系上，少突胶质细胞前体细胞(OPCs)与神经元的关系更密切，这在UMAP可视化中体现为它们之间的距离较近。';
                default:
                    return '请选择一个选项。';
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(11);
        }

        // 生成模拟细胞数据
        this.generateCellData();

        // 初始化可视化
        this.$nextTick(() => {
            this.createStepVisualization();
        });
    },
    methods: {
        prevStep() {
            if (this.activeStep > 0) {
                this.activeStep--;
                this.$nextTick(() => {
                    this.createStepVisualization();
                });
            }
        },

        nextStep() {
            if (this.activeStep < this.workflowSteps.length - 1) {
                this.activeStep++;
                this.$nextTick(() => {
                    this.createStepVisualization();
                });
            }
        },

        generateCellData() {
            // 生成模拟的单细胞数据
            this.cellData = [];

            // 定义细胞类型及其位置和颜色
            const cellTypes = [
                { name: "Neurons", x: 0, y: 0, radius: 4, color: "#1f77b4" },
                { name: "Astrocytes", x: -8, y: -2, radius: 3, color: "#ff7f0e" },
                { name: "Microglia", x: -5, y: 8, radius: 2.5, color: "#2ca02c" },
                { name: "Oligodendrocytes", x: 8, y: -2, radius: 3, color: "#d62728" },
                { name: "OPCs", x: 3, y: 3, radius: 2, color: "#9467bd" },
                { name: "Endothelial", x: -8, y: 5, radius: 2, color: "#8c564b" },
                { name: "Pericytes", x: -9, y: 0, radius: 1.5, color: "#e377c2" },
                { name: "Ependymal", x: 8, y: 5, radius: 2, color: "#7f7f7f" }
            ];

            // 为每种细胞类型生成点
            cellTypes.forEach(type => {
                const cellCount = type.name === "Pericytes" ? 50 :
                    (type.name === "Neurons" ? 1500 : 500);

                for (let i = 0; i < cellCount; i++) {
                    // 生成围绕中心点的随机分布
                    const angle = Math.random() * Math.PI * 2;
                    const distance = Math.random() * type.radius;

                    this.cellData.push({
                        x: type.x + Math.cos(angle) * distance + (Math.random() - 0.5) * 0.8,
                        y: type.y + Math.sin(angle) * distance + (Math.random() - 0.5) * 0.8,
                        type: type.name,
                        color: type.color
                    });
                }
            });
        },

        createStepVisualization() {
            // if (!this.$refs.stepVisualization) return;

            // const width = this.$refs.stepVisualization.clientWidth;
            // const height = 400;

            // // 清除现有的可视化
            // d3.select(this.$refs.stepVisualization).selectAll("*").remove();

            // // 创建SVG元素
            // this.svgElement = d3.select(this.$refs.stepVisualization)
            //     .append("svg")
            //     .attr("width", width)
            //     .attr("height", height);

            // // 根据当前步骤创建不同的可视化
            // switch (this.activeStep) {
            //     case 0:
            //         this.createQCVisualization();
            //         break;
            //     case 1:
            //         this.createFeatureSelectionVisualization();
            //         break;
            //     case 2:
            //         this.createPCAVisualization();
            //         break;
            //     case 3:
            //         this.createUMAPVisualization();
            //         break;
            //     case 4:
            //         this.createAnnotatedVisualization();
            //         break;
            // }
        },

        createQCVisualization() {
            const width = this.svgElement.attr("width");
            const height = this.svgElement.attr("height");

            // 创建质控指标可视化（散点图）
            // X轴：检测到的基因数，Y轴：线粒体比例

            // 生成模拟的质控数据
            const qcData = [];
            for (let i = 0; i < 5000; i++) {
                // 有90%是高质量细胞
                const isGoodQuality = Math.random() < 0.9;

                let genes, mito;
                if (isGoodQuality) {
                    genes = Math.random() * 2000 + 1000; // 1000-3000之间
                    mito = Math.random() * 0.1; // 0-10%
                } else {
                    // 低质量细胞：低基因数或高线粒体比例
                    if (Math.random() < 0.5) {
                        genes = Math.random() * 800 + 200; // 200-1000之间
                        mito = Math.random() * 0.1 + 0.05; // 5-15%
                    } else {
                        genes = Math.random() * 1500 + 500; // 500-2000之间
                        mito = Math.random() * 0.2 + 0.1; // 10-30%
                    }
                }

                qcData.push({
                    genes: genes,
                    mito: mito,
                    status: isGoodQuality ? "pass" : "fail"
                });
            }

            // 创建比例尺
            const xScale = d3.scaleLinear()
                .domain([0, 4000])
                .range([50, width - 50]);

            const yScale = d3.scaleLinear()
                .domain([0, 0.35])
                .range([height - 50, 50]);

            // 添加散点
            this.svgElement.selectAll("circle")
                .data(qcData)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d.genes))
                .attr("cy", d => yScale(d.mito))
                .attr("r", 3)
                .attr("fill", d => d.status === "pass" ? "#69b3a2" : "#e15759")
                .attr("opacity", 0.6)
                .attr("stroke", "#fff")
                .attr("stroke-width", 0.5);

            // 添加质控阈值线
            this.svgElement.append("line")
                .attr("x1", xScale(800))
                .attr("y1", 50)
                .attr("x2", xScale(800))
                .attr("y2", height - 50)
                .attr("stroke", "#e15759")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "5,5");

            this.svgElement.append("line")
                .attr("x1", 50)
                .attr("y1", yScale(0.1))
                .attr("x2", width - 50)
                .attr("y2", yScale(0.1))
                .attr("stroke", "#e15759")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "5,5");

            // 添加坐标轴
            const xAxis = d3.axisBottom(xScale);
            const yAxis = d3.axisLeft(yScale).tickFormat(d => (d * 100) + "%");

            this.svgElement.append("g")
                .attr("transform", `translate(0, ${height - 50})`)
                .call(xAxis);

            this.svgElement.append("g")
                .attr("transform", `translate(50, 0)`)
                .call(yAxis);

            // 添加轴标签
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", height - 10)
                .attr("text-anchor", "middle")
                .text("检测到的基因数");

            this.svgElement.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -height / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .text("线粒体基因比例");

            // 添加图例
            const legend = this.svgElement.append("g")
                .attr("transform", `translate(${width - 200}, 30)`);

            legend.append("rect")
                .attr("width", 180)
                .attr("height", 50)
                .attr("fill", "white")
                .attr("stroke", "#ddd");

            legend.append("circle")
                .attr("cx", 20)
                .attr("cy", 20)
                .attr("r", 5)
                .attr("fill", "#69b3a2");

            legend.append("text")
                .attr("x", 35)
                .attr("y", 25)
                .text("通过质控的细胞 (4,800)");

            legend.append("circle")
                .attr("cx", 20)
                .attr("cy", 40)
                .attr("r", 5)
                .attr("fill", "#e15759");

            legend.append("text")
                .attr("x", 35)
                .attr("y", 45)
                .text("未通过质控的细胞 (200)");
        },

        createFeatureSelectionVisualization() {
            const width = this.svgElement.attr("width");
            const height = this.svgElement.attr("height");

            // 创建基因变异性可视化
            // X轴：平均表达，Y轴：变异性

            // 生成模拟的基因变异性数据
            const geneData = [];
            for (let i = 0; i < 2000; i++) {
                const meanExp = Math.pow(10, Math.random() * 3 - 1); // 0.1到100之间的对数分布

                // 变异性随平均表达增加而降低，但有一些高变基因
                let variance;
                const isHighlyVariable = i < 400; // 前400个是高变基因

                if (isHighlyVariable) {
                    variance = Math.log(meanExp) * 0.5 + Math.random() * 1.5 + 0.5;
                } else {
                    variance = Math.log(meanExp) * 0.5 + Math.random() * 0.5;
                }

                geneData.push({
                    mean: meanExp,
                    variance: variance,
                    selected: isHighlyVariable
                });
            }

            // 创建比例尺
            const xScale = d3.scaleLog()
                .domain([0.1, 100])
                .range([50, width - 50]);

            const yScale = d3.scaleLinear()
                .domain([0, 5])
                .range([height - 50, 50]);

            // 绘制点
            this.svgElement.selectAll("circle")
                .data(geneData)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d.mean))
                .attr("cy", d => yScale(d.variance))
                .attr("r", 3)
                .attr("fill", d => d.selected ? "#e15759" : "#69b3a2")
                .attr("opacity", 0.6)
                .attr("stroke", "#fff")
                .attr("stroke-width", 0.5);

            // 拟合曲线
            const lineData = [];
            for (let x = 0.1; x <= 100; x *= 1.5) {
                lineData.push({
                    x: x,
                    y: Math.log(x) * 0.5 + 0.5
                });
            }

            const line = d3.line()
                .x(d => xScale(d.x))
                .y(d => yScale(d.y))
                .curve(d3.curveBasis);

            this.svgElement.append("path")
                .datum(lineData)
                .attr("fill", "none")
                .attr("stroke", "#888")
                .attr("stroke-width", 1.5)
                .attr("stroke-dasharray", "5,5")
                .attr("d", line);

            // 添加坐标轴
            const xAxis = d3.axisBottom(xScale)
                .tickValues([0.1, 1, 10, 100])
                .tickFormat(d => d.toString());

            const yAxis = d3.axisLeft(yScale);

            this.svgElement.append("g")
                .attr("transform", `translate(0, ${height - 50})`)
                .call(xAxis);

            this.svgElement.append("g")
                .attr("transform", `translate(50, 0)`)
                .call(yAxis);

            // 添加轴标签
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", height - 10)
                .attr("text-anchor", "middle")
                .text("平均表达量（对数尺度）");

            this.svgElement.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -height / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .text("变异性（残差方差）");

            // 添加图例
            const legend = this.svgElement.append("g")
                .attr("transform", `translate(${width - 200}, 30)`);

            legend.append("rect")
                .attr("width", 190)
                .attr("height", 50)
                .attr("fill", "white")
                .attr("stroke", "#ddd");

            legend.append("circle")
                .attr("cx", 20)
                .attr("cy", 20)
                .attr("r", 5)
                .attr("fill", "#e15759");

            legend.append("text")
                .attr("x", 35)
                .attr("y", 25)
                .text("选择的高变异基因 (2,000)");

            legend.append("circle")
                .attr("cx", 20)
                .attr("cy", 40)
                .attr("r", 5)
                .attr("fill", "#69b3a2");

            legend.append("text")
                .attr("x", 35)
                .attr("y", 45)
                .text("其他基因 (13,000)");
        },

        createPCAVisualization() {
            const width = this.svgElement.attr("width");
            const height = this.svgElement.attr("height");

            // 创建PCA结果可视化
            // 生成模拟的PCA数据
            const pcaData = [];

            // 定义几个模糊的细胞类型团
            const clusters = [
                { x: width * 0.3, y: height * 0.3, radius: 60, count: 1500 },
                { x: width * 0.7, y: height * 0.3, radius: 50, count: 800 },
                { x: width * 0.3, y: height * 0.7, radius: 60, count: 900 },
                { x: width * 0.7, y: height * 0.7, radius: 70, count: 1600 }
            ];

            // 为每个簇生成点
            clusters.forEach((cluster, clusterIndex) => {
                for (let i = 0; i < cluster.count; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const r = Math.random() * cluster.radius;

                    pcaData.push({
                        x: cluster.x + Math.cos(angle) * r + (Math.random() - 0.5) * 30,
                        y: cluster.y + Math.sin(angle) * r + (Math.random() - 0.5) * 30,
                        cluster: clusterIndex
                    });
                }
            });

            // 绘制点
            this.svgElement.selectAll("circle")
                .data(pcaData)
                .enter()
                .append("circle")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 2)
                .attr("fill", d => d3.schemeCategory10[d.cluster])
                .attr("opacity", 0.5);

            // 添加坐标轴标签
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", height - 10)
                .attr("text-anchor", "middle")
                .text("PC1 (14.2% 方差解释)");

            this.svgElement.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -height / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .text("PC2 (8.7% 方差解释)");

            // 添加标题
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", 25)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .text("PCA结果 (前两个主成分)");
        },

        createUMAPVisualization() {
            // 根据当前UMAP参数显示结果
            this.updateUMAPResult();
        },

        updateUMAPResult() {
            const width = this.svgElement.attr("width");
            const height = this.svgElement.attr("height");

            // 清除现有可视化
            this.svgElement.selectAll("*").remove();

            // 模拟不同参数对UMAP结果的影响
            // n_neighbors影响分离程度，min_dist影响点分布的紧凑性

            // 计算簇中心的位置和散布程度
            const clusterSpread = 12 - this.nNeighbors / 5; // n_neighbors越大，分离越差
            const pointSpread = 1 + this.minDist * 5; // min_dist越大，点分布越松散

            // 定义模拟的细胞类型簇
            const clusters = [
                { name: "Neurons", x: 0, y: 0, radius: 4 * pointSpread, color: "#1f77b4" },
                { name: "Astrocytes", x: -8 + clusterSpread * 0.3, y: -2, radius: 3 * pointSpread, color: "#ff7f0e" },
                { name: "Microglia", x: -5 + clusterSpread * 0.2, y: 8 - clusterSpread * 0.3, radius: 2.5 * pointSpread, color: "#2ca02c" },
                { name: "Oligodendrocytes", x: 8 - clusterSpread * 0.3, y: -2, radius: 3 * pointSpread, color: "#d62728" },
                { name: "OPCs", x: 3 - clusterSpread * 0.1, y: 3 - clusterSpread * 0.1, radius: 2 * pointSpread, color: "#9467bd" },
                { name: "Endothelial", x: -8 + clusterSpread * 0.4, y: 5 - clusterSpread * 0.2, radius: 2 * pointSpread, color: "#8c564b" },
                { name: "Pericytes", x: -9 + clusterSpread * 0.4, y: 0, radius: 1.5 * pointSpread, color: "#e377c2" },
                { name: "Ependymal", x: 8 - clusterSpread * 0.4, y: 5 - clusterSpread * 0.2, radius: 2 * pointSpread, color: "#7f7f7f" }
            ];

            // 生成模拟数据
            const umapData = [];

            clusters.forEach(cluster => {
                const count = cluster.name === "Pericytes" ? 50 :
                    (cluster.name === "Neurons" ? 1500 : 500);

                for (let i = 0; i < count; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const distance = Math.random() * cluster.radius;

                    umapData.push({
                        x: cluster.x + Math.cos(angle) * distance + (Math.random() - 0.5) * 0.8,
                        y: cluster.y + Math.sin(angle) * distance + (Math.random() - 0.5) * 0.8,
                        type: cluster.name,
                        color: cluster.color
                    });
                }
            });

            // 设置比例尺
            const xExtent = d3.extent(umapData, d => d.x);
            const yExtent = d3.extent(umapData, d => d.y);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - 1, xExtent[1] + 1])
                .range([50, width - 50]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - 1, yExtent[1] + 1])
                .range([height - 50, 50]);

            // 绘制点
            this.svgElement.selectAll("circle")
                .data(umapData)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 2)
                .attr("fill", d => d.color)
                .attr("opacity", 0.7);

            // 添加坐标轴
            const xAxis = d3.axisBottom(xScale).ticks(5);
            const yAxis = d3.axisLeft(yScale).ticks(5);

            this.svgElement.append("g")
                .attr("transform", `translate(0, ${height - 50})`)
                .call(xAxis);

            this.svgElement.append("g")
                .attr("transform", `translate(50, 0)`)
                .call(yAxis);

            // 添加轴标签
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", height - 10)
                .attr("text-anchor", "middle")
                .text("UMAP 1");

            this.svgElement.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -height / 2)
                .attr("y", 15)
                .attr("text-anchor", "middle")
                .text("UMAP 2");

            // 添加标题
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", 25)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .text(`UMAP结果 (n_neighbors=${this.nNeighbors}, min_dist=${this.minDist.toFixed(1)})`);
        },

        createAnnotatedVisualization() {
            const width = this.svgElement.attr("width");
            const height = this.svgElement.attr("height");

            // 使用最优参数的UMAP结果，添加细胞类型注释
            // 清除现有可视化
            this.svgElement.selectAll("*").remove();

            // 定义细胞类型簇
            const clusters = [
                { name: "Neurons", x: 0, y: 0, radius: 4, color: "#1f77b4" },
                { name: "Astrocytes", x: -8, y: -2, radius: 3, color: "#ff7f0e" },
                { name: "Microglia", x: -5, y: 8, radius: 2.5, color: "#2ca02c" },
                { name: "Oligodendrocytes", x: 8, y: -2, radius: 3, color: "#d62728" },
                { name: "OPCs", x: 3, y: 3, radius: 2, color: "#9467bd" },
                { name: "Endothelial", x: -8, y: 5, radius: 2, color: "#8c564b" },
                { name: "Pericytes", x: -9, y: 0, radius: 1.5, color: "#e377c2" },
                { name: "Ependymal", x: 8, y: 5, radius: 2, color: "#7f7f7f" }
            ];

            // 生成模拟数据
            const annotatedData = [];

            clusters.forEach(cluster => {
                const count = cluster.name === "Pericytes" ? 50 :
                    (cluster.name === "Neurons" ? 1500 : 500);

                for (let i = 0; i < count; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const distance = Math.random() * cluster.radius;

                    annotatedData.push({
                        x: cluster.x + Math.cos(angle) * distance + (Math.random() - 0.5) * 0.8,
                        y: cluster.y + Math.sin(angle) * distance + (Math.random() - 0.5) * 0.8,
                        type: cluster.name,
                        color: cluster.color
                    });
                }
            });

            // 设置比例尺
            const xExtent = d3.extent(annotatedData, d => d.x);
            const yExtent = d3.extent(annotatedData, d => d.y);

            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - 1, xExtent[1] + 1])
                .range([80, width - 50]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - 1, yExtent[1] + 1])
                .range([height - 50, 50]);

            // 绘制点
            this.svgElement.selectAll("circle")
                .data(annotatedData)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 2)
                .attr("fill", d => d.color)
                .attr("opacity", 0.7);

            // 添加细胞类型标签
            clusters.forEach(cluster => {
                this.svgElement.append("text")
                    .attr("x", xScale(cluster.x))
                    .attr("y", yScale(cluster.y))
                    .attr("text-anchor", "middle")
                    .attr("font-size", "10px")
                    .attr("font-weight", "bold")
                    .attr("fill", cluster.color)
                    .text(cluster.name);
            });

            // 添加坐标轴
            const xAxis = d3.axisBottom(xScale).ticks(5);
            const yAxis = d3.axisLeft(yScale).ticks(5);

            this.svgElement.append("g")
                .attr("transform", `translate(0, ${height - 50})`)
                .call(xAxis);

            this.svgElement.append("g")
                .attr("transform", `translate(80, 0)`)
                .call(yAxis);

            // 添加轴标签
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", height - 10)
                .attr("text-anchor", "middle")
                .text("UMAP 1");

            this.svgElement.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", -height / 2)
                .attr("y", 40)
                .attr("text-anchor", "middle")
                .text("UMAP 2");

            // 添加标题
            this.svgElement.append("text")
                .attr("x", width / 2)
                .attr("y", 25)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .text("细胞类型注释结果");

            // 添加图例
            const legend = this.svgElement.append("g")
                .attr("transform", `translate(${width - 150}, 80)`);

            clusters.forEach((cluster, i) => {
                const legendRow = legend.append("g")
                    .attr("transform", `translate(0, ${i * 20})`);

                legendRow.append("rect")
                    .attr("width", 10)
                    .attr("height", 10)
                    .attr("fill", cluster.color);

                legendRow.append("text")
                    .attr("x", 15)
                    .attr("y", 9)
                    .attr("font-size", "9px")
                    .text(cluster.name);
            });
        },

        updateVisualization() {
            if (this.activeStep === 3) {
                this.updateUMAPResult();
            }
        },

        checkInterpretation() {
            this.interpretationCompleted = true;
            this.isInterpretationCorrect = this.interpretationAnswer === 2; // OPCs是正确答案

            if (this.isInterpretationCorrect || ++this.interpretationRetries >= 1) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        }
    }
}
</script>

<style scoped>
.el-slider {
    width: 100%;
}

.section-container {
    margin-bottom: 40px;
}

.section-card {
    margin-bottom: 20px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.markdown-content {
    margin-bottom: 30px;
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.case-study {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.case-description {
    flex: 1;
    min-width: 300px;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.case-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.case-header i {
    font-size: 24px;
    color: #409EFF;
    margin-right: 10px;
}

.case-header h4 {
    margin: 0;
    color: #303133;
}

.analysis-workflow {
    flex: 1;
    min-width: 300px;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.workflow-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.workflow-header i {
    font-size: 24px;
    color: #409EFF;
    margin-right: 10px;
}

.workflow-header h4 {
    margin: 0;
    color: #303133;
}

.step-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.step-detail {
    flex: 2;
    min-width: 100%;
    padding: 15px;
    margin-top: 20px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.step-description {
    margin-bottom: 20px;
}

.step-visualization {
    width: 100%;
    height: 400px;
    margin: 20px 0;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
}

.parameter-controls {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.parameter-sliders {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin: 15px 0;
}

.parameter-item {
    display: flex;
    align-items: center;
}

.parameter-item span {
    width: 100px;
    margin-right: 15px;
}

.parameter-value {
    width: 50px;
    text-align: right;
    margin-left: 15px;
    color: #606266;
}

.parameter-effect {
    margin-top: 15px;
    padding: 10px;
    background-color: white;
    border-radius: 4px;
}

.interpretation-quiz {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.interpretation-question {
    margin-top: 15px;
}

.interpretation-question .el-radio-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 15px 0;
    margin-left: 20px;
}

.submit-btn {
    margin-top: 15px;
}

.interpretation-response {
    margin-top: 20px;
}

.completion-section {
    margin-top: 30px;
    padding: 15px;
    background-color: #ecf5ff;
    border-radius: 4px;
    border: 1px solid #d9ecff;
}

.completion-message {
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    margin-top: 15px;
}

.completion-message h4 {
    color: #409EFF;
    margin-top: 0;
}

/* 全局样式适配 */
:deep(h2) {
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    margin-top: 20px;
}

:deep(blockquote) {
    border-left: 4px solid #409EFF;
    padding-left: 15px;
    color: #606266;
    margin: 20px 0;
}

:deep(p) {
    line-height: 1.6;
}

:deep(strong) {
    color: #409EFF;
}

:deep(ul),
:deep(ol) {
    padding-left: 20px;
    line-height: 1.6;
}
</style>