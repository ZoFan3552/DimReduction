<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>3. UMAP的数学基础</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 数学概念互动 -->
            <div class="interaction-container">
                <h3>互动练习：黎曼几何和流形学习</h3>
                <p>下面的交互式演示将帮助您理解距离度量和流形在UMAP中的应用。</p>

                <el-tabs v-model="activeTab" type="border-card">
                    <el-tab-pane label="黎曼几何示例" name="riemann">
                        <div class="tab-content">
                            <div class="math-viz-container" ref="riemannViz"></div>
                            <p>在上方的网格中，蓝色点表示起点，红色点表示终点。尝试拖动这些点，观察在不同流形上的最短路径（测地线）如何变化。</p>
                            <p>在平面上，最短路径是直线；但在曲面上，最短路径会沿着曲面弯曲。这就是为什么在高维空间中需要特殊的距离度量。</p>
                            <div class="controls">
                                <span>曲面弯曲度:</span>
                                <el-slider v-model="curvatureValue" :min="0" :max="10" :step="1"
                                    @change="updateRiemannViz"></el-slider>
                            </div>
                        </div>
                    </el-tab-pane>

                    <!-- <el-tab-pane label="流形投影示例" name="manifold">
                        <div class="tab-content">
                            <div class="math-viz-container" ref="manifoldViz"></div>
                            <p>此示例展示了从3D流形到2D平面的投影过程。观察当投影方式改变时，点之间的相对距离如何变化。</p>
                            <div class="controls">
                                <span>投影类型:</span>
                                <el-radio-group v-model="projectionType" @change="updateManifoldViz">
                                    <el-radio label="pca">PCA投影 (线性)</el-radio>
                                    <el-radio label="umap">UMAP投影 (非线性)</el-radio>
                                </el-radio-group>
                            </div>
                        </div>
                    </el-tab-pane> -->
                </el-tabs>

                <!-- 问答练习 -->
                <div class="quiz-container" v-if="!quizCompleted">
                    <h3>数学概念测验</h3>
                    <p>根据上面的内容和演示，回答以下问题：</p>

                    <div class="quiz-question" v-for="(question, index) in questions" :key="index">
                        <p><strong>{{ index + 1 }}. {{ question.text }}</strong></p>
                        <el-radio-group v-model="userAnswers[index]">
                            <el-radio v-for="(option, optIndex) in question.options" :key="optIndex" :label="optIndex">
                                {{ option }}
                            </el-radio>
                        </el-radio-group>
                    </div>

                    <el-button type="primary" @click="checkAnswers" :disabled="!allQuestionsAnswered"
                        class="submit-btn">
                        提交答案
                    </el-button>
                </div>

                <!-- 回应部分 -->
                <div v-if="quizCompleted" class="response-container">
                    <el-alert :title="quizFeedbackTitle" :type="allCorrect ? 'success' : 'info'"
                        :description="quizFeedbackDescription" show-icon>
                    </el-alert>

                    <div class="quiz-results" v-if="!allCorrect">
                        <h4>答题结果:</h4>
                        <div v-for="(question, index) in questions" :key="index" class="question-result">
                            <p>
                                <strong>{{ index + 1 }}. {{ question.text }}</strong>
                                <el-tag size="small" :type="questionResults[index] ? 'success' : 'danger'">
                                    {{ questionResults[index] ? '正确' : '错误' }}
                                </el-tag>
                            </p>
                            <p v-if="!questionResults[index]" class="explanation">
                                正确答案: {{ question.options[question.answer] }}<br>
                                解释: {{ question.explanation }}
                            </p>
                        </div>

                        <el-button type="info" @click="resetQuiz" class="retry-btn">
                            重新作答
                        </el-button>
                    </div>

                    <div v-if="allCorrect || retries >= 2" class="next-section">
                        <p>🎉 恭喜完成数学基础部分！您可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
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
import katex from 'katex';
// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}



export default {
    name: 'Section3MathFoundation',
    data() {
        return {
            markdownContent: `
  ## UMAP的数学基础
  
  UMAP算法的强大源于其扎实的数学基础。虽然完整的理论相当复杂，但我们可以从几个核心概念入手，循序渐进地理解其数学原理。
  
  ### 黎曼几何与流形
  
  UMAP建立在**黎曼几何**和**拓扑学**的基础上，特别是关于流形的理论。
  
  <strong>流形(Manifold)</strong>是一种拓扑空间，局部看起来像欧几里得空间(如平面或三维空间)，但全局可能具有不同的拓扑结构。简单来说，流形是可以局部被"压平"的空间。例如，地球表面是一个2维流形 - 局部看它近似一个平面，但全局它是一个球体。
  
  在机器学习中，**流形假设**认为高维数据往往位于嵌入在高维空间中的低维流形上。UMAP利用这一假设来实现降维。
  
  ### 黎曼度量与局部距离
  
  在黎曼几何中，**度量**定义了如何测量距离。在流形上，我们需要特殊的度量来正确测量点之间的距离。
  
  在欧几里得空间中，两点间的距离是直线距离：
  
  $d(x, y) = \\sqrt{\\sum_{i=1}^n (x_i - y_i)^2}$
  
  但在弯曲的流形上，我们需要考虑沿着流形的距离，这通常是测地线(geodesic)的长度。
  
  UMAP使用局部距离近似来捕捉流形的局部结构。对于每个点$x$，它定义了基于近邻的局部度量：
  
  $d_x(x, y) = d(x, y) / \\sigma_x$
  
  其中$\\sigma_x$是一个归一化因子，使得$x$的邻域内的连接性具有一致性。
  
  ### 模糊拓扑表示
  
  UMAP将数据视为**模糊拓扑结构**。在这种表示中，两点间的关系不是二元的(连接或不连接)，而是一个概率值，表示它们属于同一个邻域的概率。
  
  对于点$x$和$y$，UMAP定义了一个模糊集合成员函数：
  
  $\\mu_x(y) = \\exp(-d_x(x, y))$
  
  这个函数表示点$y$属于点$x$邻域的程度。值越接近1，表示$y$越可能在$x$的邻域内；值越接近0，表示越不可能。
  
  ### 模糊简单复形
  
  UMAP使用**模糊单纯复形(fuzzy simplicial complex)**来表示数据的高维拓扑结构。这是一种能够捕捉多尺度拓扑特征的数学结构。
  
  在实践中，UMAP构建了一个加权图，其中权重基于模糊成员函数：
  
  $$w(x, y) = \\mu_x(y) + \\mu_y(x) - \\mu_x(y) \\cdot \\mu_y(x)$$
  
  这种方式确保了图的对称性，同时保留了点之间的局部关系强度。
  
  ### 低维嵌入与力导向布局
  
  最后，UMAP通过优化一个目标函数来找到低维嵌入。这个优化过程试图使低维空间中的模糊拓扑结构尽可能接近高维空间中的结构。
  
  目标函数基于**交叉熵**，平衡了两个目标：
  1. 保持连接点之间的接近性
  2. 保持非连接点之间的分离性
  
  $$\\sum_{(x,y) \\in E} w(x,y) \\log\\left(\\frac{w(x,y)}{w'(x,y)}\\right) + (1-w(x,y)) \\log\\left(\\frac{1-w(x,y)}{1-w'(x,y)}\\right)$$
  
  其中$w(x,y)$是高维空间中点的权重，$w'(x,y)$是低维空间中对应点的权重。
  
  UMAP使用**随机梯度下降**和一种类似于力导向图布局的过程来优化这个目标函数。点之间的"力"基于它们之间的权重：连接强的点相互吸引，连接弱的点相互排斥。
  
  在接下来的互动练习中，我们将直观地理解这些数学概念如何在实践中应用。
        `,
            activeTab: 'riemann',
            curvatureValue: 5,
            projectionType: 'pca',
            questions: [
                {
                    text: 'UMAP算法的理论基础主要来自于以下哪个数学分支？',
                    options: [
                        '微积分和线性代数',
                        '概率论和统计学',
                        '黎曼几何和拓扑学',
                        '离散数学和图论'
                    ],
                    answer: 2,
                    explanation: 'UMAP的理论基础主要来自黎曼几何和拓扑学，特别是关于流形和拓扑数据分析的理论。'
                },
                {
                    text: '在UMAP中，"流形"指的是什么？',
                    options: [
                        '一种特殊的数据结构，用于存储高维数据',
                        '一种拓扑空间，局部类似于欧几里得空间',
                        '一种降维算法的特殊实现',
                        '数据中的噪声和异常值'
                    ],
                    answer: 1,
                    explanation: '流形是一种拓扑空间，在局部看起来像欧几里得空间，但全局可能有不同的拓扑结构。'
                },
                {
                    text: 'UMAP使用什么类型的距离度量来捕捉流形的局部结构？',
                    options: [
                        '仅使用欧几里得距离',
                        '仅使用曼哈顿距离',
                        '基于测地线的全局距离',
                        '基于近邻的局部距离近似'
                    ],
                    answer: 3,
                    explanation: 'UMAP使用基于近邻的局部距离近似，为每个点定义了一个局部度量，基于其邻域的连接性。'
                },
                {
                    text: 'UMAP算法中的"模糊拓扑表示"指的是什么？',
                    options: [
                        '数据点之间的关系是二元的（连接或不连接）',
                        '数据点之间的关系用概率值表示（模糊集合成员函数）',
                        '使用随机抽样来近似拓扑结构',
                        '数据点被分成不相交的簇'
                    ],
                    answer: 1,
                    explanation: '在模糊拓扑表示中，两点间的关系不是二元的，而是用一个概率值表示它们属于同一个邻域的程度。'
                }
            ],
            userAnswers: [],
            questionResults: [],
            quizCompleted: false,
            allCorrect: false,
            retries: 0,
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
            // return marked(this.markdownContent);
        },
        allQuestionsAnswered() {
            return this.userAnswers.length === this.questions.length &&
                !this.userAnswers.includes(undefined);
        },
        quizFeedbackTitle() {
            return this.allCorrect ? '恭喜！所有问题回答正确！' : '测验完成';
        },
        quizFeedbackDescription() {
            if (this.allCorrect) {
                return '您已经很好地掌握了UMAP的数学基础概念！';
            } else {
                const correctCount = this.questionResults.filter(result => result).length;
                return `您答对了${correctCount}道题目（共${this.questions.length}题）。请查看下方的详细解释。`;
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(3);
        }

        // 初始化可视化
        this.$nextTick(() => {
            this.initRiemannViz();
            this.initManifoldViz();
        });
    },
    methods: {
        initRiemannViz() {
            // 创建可视化元素
            const width = this.$refs.riemannViz.clientWidth;
            const height = 300;

            // 清除可能存在的旧SVG
            d3.select(this.$refs.riemannViz).selectAll("*").remove();

            const svg = d3.select(this.$refs.riemannViz)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 绘制网格
            const gridSize = 20;
            const rows = Math.floor(height / gridSize);
            const cols = Math.floor(width / gridSize);

            // 创建弯曲的网格线
            for (let i = 0; i <= rows; i++) {
                const points = [];
                for (let j = 0; j <= cols; j++) {
                    // 计算网格点坐标
                    const x = j * gridSize;
                    const y = i * gridSize;

                    // 根据曲率值添加弯曲效果
                    const curveFactor = this.curvatureValue / 10;
                    const curveX = x;
                    const curveY = y + Math.sin(x / width * Math.PI * 2) * 20 * curveFactor;

                    points.push([curveX, curveY]);
                }

                // 绘制水平网格线
                svg.append("path")
                    .datum(points)
                    .attr("d", d3.line())
                    .attr("fill", "none")
                    .attr("stroke", "#ddd")
                    .attr("stroke-width", 1);
            }

            for (let j = 0; j <= cols; j++) {
                const points = [];
                for (let i = 0; i <= rows; i++) {
                    // 计算网格点坐标
                    const x = j * gridSize;
                    const y = i * gridSize;

                    // 根据曲率值添加弯曲效果
                    const curveFactor = this.curvatureValue / 10;
                    const curveX = x;
                    const curveY = y + Math.sin(x / width * Math.PI * 2) * 20 * curveFactor;

                    points.push([curveX, curveY]);
                }

                // 绘制垂直网格线
                svg.append("path")
                    .datum(points)
                    .attr("d", d3.line())
                    .attr("fill", "none")
                    .attr("stroke", "#ddd")
                    .attr("stroke-width", 1);
            }

            // 添加起点和终点
            const startPoint = { x: width * 0.2, y: height * 0.5 };
            const endPoint = { x: width * 0.8, y: height * 0.5 };

            // 绘制起点
            const dragStart = d3.drag()
                .on("drag", (event) => {
                    startPoint.x = Math.max(0, Math.min(width, event.x));
                    startPoint.y = Math.max(0, Math.min(height, event.y));
                    updatePath();
                });

            svg.append("circle")
                .attr("cx", startPoint.x)
                .attr("cy", startPoint.y)
                .attr("r", 8)
                .attr("fill", "#409EFF")
                .call(dragStart);

            // 绘制终点
            const dragEnd = d3.drag()
                .on("drag", (event) => {
                    endPoint.x = Math.max(0, Math.min(width, event.x));
                    endPoint.y = Math.max(0, Math.min(height, event.y));
                    updatePath();
                });

            svg.append("circle")
                .attr("cx", endPoint.x)
                .attr("cy", endPoint.y)
                .attr("r", 8)
                .attr("fill", "#F56C6C")
                .call(dragEnd);

            // 绘制最短路径
            const path = svg.append("path")
                .attr("fill", "none")
                .attr("stroke", "#67C23A")
                .attr("stroke-width", 3)
                .attr("stroke-dasharray", "5,5");

            // 更新路径函数
            const updatePath = () => {
                // 在曲面上模拟测地线
                const curveFactor = this.curvatureValue / 10;

                if (curveFactor < 0.1) {
                    // 接近平面，使用直线
                    path.attr("d", `M${startPoint.x},${startPoint.y} L${endPoint.x},${endPoint.y}`);
                } else {
                    // 曲面上的路径，使用贝塞尔曲线模拟测地线
                    const dx = endPoint.x - startPoint.x;
                    const dy = endPoint.y - startPoint.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    // 路径弯曲程度基于曲率和点之间的水平距离
                    const bendAmount = Math.sin((startPoint.x + endPoint.x) / 2 / width * Math.PI * 2) *
                        dist * 0.3 * curveFactor;

                    // 控制点垂直于起点和终点连线
                    const cx = (startPoint.x + endPoint.x) / 2;
                    const cy = (startPoint.y + endPoint.y) / 2 + bendAmount;

                    path.attr("d", `M${startPoint.x},${startPoint.y} Q${cx},${cy} ${endPoint.x},${endPoint.y}`);
                }
            };

            // 初始化路径
            updatePath();

            // 存储更新函数供外部调用
            this.updateRiemannPath = updatePath;
        },

        updateRiemannViz() {
            this.initRiemannViz(); // 重新初始化可视化
        },

        initManifoldViz() {
            // // 创建可视化元素
            // const width = this.$refs.manifoldViz.clientWidth;
            // const height = 300;

            // // 清除可能存在的旧SVG
            // d3.select(this.$refs.manifoldViz).selectAll("*").remove();

            // d3.select(this.$refs.manifoldViz)
            //     .append("svg")
            //     .attr("width", width)
            //     .attr("height", height);

            // // 生成3D数据 - 模拟一个扭曲的平面
            // const points3D = [];
            // for (let i = 0; i < 100; i++) {
            //     const u = Math.random() * 2 - 1; // -1 to 1
            //     const v = Math.random() * 2 - 1; // -1 to 1

            //     // 生成一个扭曲的2D流形，嵌入在3D空间中
            //     const x = u;
            //     const y = v;
            //     const z = Math.sin(u * Math.PI) * Math.cos(v * Math.PI) * 0.5;

            //     // 添加点和原始参数化坐标
            //     points3D.push({
            //         x: x,
            //         y: y,
            //         z: z,
            //         u: u,
            //         v: v,
            //         id: i,
            //         cluster: (u > 0 ? (v > 0 ? 0 : 1) : (v > 0 ? 2 : 3)) // 分配到4个簇
            //     });
            // }
            // // 存储数据供更新函数使用
            // this.manifoldData = points3D;
            // // 绘制3D数据的投影
            // this.updateManifoldViz();


        },

        updateManifoldViz() {
            // if (!this.manifoldData) return;

            // const width = this.$refs.manifoldViz.clientWidth;
            // const height = 300;

            // // 清除现有点
            // d3.select(this.$refs.manifoldViz).select("svg").selectAll("circle").remove();

            // const svg = d3.select(this.$refs.manifoldViz).select("svg");

            // // 基于投影类型计算2D坐标
            // const points2D = this.manifoldData.map(p => {
            //     let x, y;

            //     if (this.projectionType === 'pca') {
            //         // PCA投影 - 简单地使用原始的u、v参数化坐标
            //         x = p.u;
            //         y = p.v;
            //     } else {
            //         // UMAP投影 - 模拟非线性投影
            //         // 注意：这里只是一个简化的模拟，不是真正的UMAP算法
            //         // 使点基于簇分散开来
            //         const angle = Math.atan2(p.v, p.u);
            //         const r = Math.sqrt(p.u * p.u + p.v * p.v);

            //         // 非线性变换，使聚类更明显
            //         const r2 = Math.pow(r, 0.8);
            //         x = Math.cos(angle) * r2;
            //         y = Math.sin(angle) * r2;

            //         // 根据簇添加额外的分离
            //         if (p.cluster === 0) { x += 0.2; y += 0.2; }
            //         else if (p.cluster === 1) { x += 0.2; y -= 0.2; }
            //         else if (p.cluster === 2) { x -= 0.2; y += 0.2; }
            //         else if (p.cluster === 3) { x -= 0.2; y -= 0.2; }
            //     }

            //     return {
            //         id: p.id,
            //         x: x,
            //         y: y,
            //         cluster: p.cluster
            //     };
            // });

            // // 缩放到视图范围
            // const xExtent = d3.extent(points2D, d => d.x);
            // const yExtent = d3.extent(points2D, d => d.y);

            // const xScale = d3.scaleLinear()
            //     .domain([xExtent[0] - 0.1, xExtent[1] + 0.1])
            //     .range([50, width - 50]);

            // const yScale = d3.scaleLinear()
            //     .domain([yExtent[0] - 0.1, yExtent[1] + 0.1])
            //     .range([height - 50, 50]);

            // // 定义颜色比例尺
            // const colorScale = d3.scaleOrdinal()
            //     .domain([0, 1, 2, 3])
            //     .range(["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]);

            // // 绘制点
            // svg.selectAll("circle")
            //     .data(points2D)
            //     .enter()
            //     .append("circle")
            //     .attr("cx", d => xScale(d.x))
            //     .attr("cy", d => yScale(d.y))
            //     .attr("r", 6)
            //     .style("fill", d => colorScale(d.cluster))
            //     .style("opacity", 0.7)
            //     .style("stroke", "#fff")
            //     .style("stroke-width", 0.5);

            // // 添加坐标轴
            // svg.selectAll(".axis").remove();

            // // X轴
            // svg.append("line")
            //     .attr("class", "axis")
            //     .attr("x1", 40)
            //     .attr("y1", height / 2)
            //     .attr("x2", width - 40)
            //     .attr("y2", height / 2)
            //     .attr("stroke", "#999")
            //     .attr("stroke-width", 1);

            // // Y轴
            // svg.append("line")
            //     .attr("class", "axis")
            //     .attr("x1", width / 2)
            //     .attr("y1", 40)
            //     .attr("x2", width / 2)
            //     .attr("y2", height - 40)
            //     .attr("stroke", "#999")
            //     .attr("stroke-width", 1);

            // // 轴标签
            // svg.selectAll(".axis-label").remove();

            // svg.append("text")
            //     .attr("class", "axis-label")
            //     .attr("x", width - 30)
            //     .attr("y", height / 2 - 10)
            //     .text("维度1")
            //     .attr("font-size", "12px")
            //     .attr("fill", "#666");

            // svg.append("text")
            //     .attr("class", "axis-label")
            //     .attr("x", width / 2 + 10)
            //     .attr("y", 30)
            //     .text("维度2")
            //     .attr("font-size", "12px")
            //     .attr("fill", "#666");

            // // 添加标题
            // svg.selectAll(".viz-title").remove();

            // svg.append("text")
            //     .attr("class", "viz-title")
            //     .attr("x", width / 2)
            //     .attr("y", 20)
            //     .attr("text-anchor", "middle")
            //     .attr("font-size", "14px")
            //     .attr("font-weight", "bold")
            //     .attr("fill", "#333")
            //     .text(this.projectionType === 'pca' ? "PCA线性投影" : "UMAP非线性投影");
        },

        checkAnswers() {
            this.quizCompleted = true;
            this.questionResults = this.questions.map(
                (q, i) => this.userAnswers[i] === q.answer
            );
            this.allCorrect = this.questionResults.every(result => result);

            if (this.allCorrect || ++this.retries >= 2) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },

        resetQuiz() {
            this.quizCompleted = false;
            this.userAnswers = [];
            this.questionResults = [];
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    },
    watch: {
        curvatureValue() {
            this.updateRiemannViz();
        },
        projectionType() {
            this.updateManifoldViz();
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

.markdown-content img {
    max-width: 100%;
    margin: 20px 0;
    border-radius: 5px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.tab-content {
    padding: 15px;
}

.math-viz-container {
    width: 100%;
    height: 300px;
    margin: 20px 0;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
}

.controls {
    display: flex;
    align-items: center;
    margin: 15px 0;
}

.controls span {
    width: 120px;
    margin-right: 15px;
}

.quiz-container {
    margin-top: 30px;
    padding: 15px;
    border-top: 1px dashed #dcdfe6;
}

.quiz-question {
    margin-bottom: 20px;
}

.quiz-question .el-radio-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
    margin-left: 20px;
}

.submit-btn {
    margin-top: 20px;
}

.response-container {
    margin-top: 20px;
}

.quiz-results {
    margin-top: 20px;
    padding: 15px;
    background-color: #f2f6fc;
    border-radius: 4px;
}

.question-result {
    margin-bottom: 15px;
}

.explanation {
    margin-top: 5px;
    margin-left: 20px;
    color: #606266;
    font-size: 0.9rem;
}

.retry-btn {
    margin-top: 15px;
}

.next-section {
    margin-top: 20px;
    text-align: center;
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
</style>