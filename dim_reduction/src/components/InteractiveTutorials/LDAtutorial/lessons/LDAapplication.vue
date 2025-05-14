<!-- ApplicationsOfLDA.vue - LDA应用场景教学组件 -->
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

        <!-- 互动区域 - 应用场景探索 -->
        <div v-if="!isCompleted" class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-s-opportunity"></i> 互动练习：LDA应用场景探索
            </h3>

            <div class="applications-explorer">
                <div class="application-categories">
                    <el-menu :default-active="activeCategory" class="category-menu" @select="selectCategory">
                        <el-menu-item index="face-recognition">
                            <i class="el-icon-user"></i>
                            <span>人脸识别</span>
                        </el-menu-item>
                        <el-menu-item index="text-classification">
                            <i class="el-icon-document"></i>
                            <span>文本分类</span>
                        </el-menu-item>
                        <el-menu-item index="bioinformatics">
                            <i class="el-icon-data-analysis"></i>
                            <span>生物信息学</span>
                        </el-menu-item>
                        <el-menu-item index="finance">
                            <i class="el-icon-money"></i>
                            <span>金融领域</span>
                        </el-menu-item>
                        <el-menu-item index="medical">
                            <i class="el-icon-first-aid-kit"></i>
                            <span>医学诊断</span>
                        </el-menu-item>
                    </el-menu>
                </div>

                <div class="application-details">
                    <div class="application-header">
                        <h3>{{ applicationData.title }}</h3>
                        <div class="application-tags">
                            <el-tag v-for="tag in applicationData.tags" :key="tag" size="small" effect="plain">
                                {{ tag }}
                            </el-tag>
                        </div>
                    </div>

                    <div class="application-content">


                        <div class="application-description">
                            <p v-html="applicationData.description"></p>

                            <h4>LDA在此应用中的作用:</h4>
                            <ul>
                                <li v-for="(point, index) in applicationData.ldaRoles" :key="index">
                                    {{ point }}
                                </li>
                            </ul>

                            <h4>相关研究:</h4>
                            <p v-html="applicationData.research"></p>

                            <div class="application-challenges">
                                <h4>挑战与解决方案:</h4>
                                <el-collapse>
                                    <el-collapse-item v-for="(challenge, index) in applicationData.challenges"
                                        :key="index" :title="challenge.title">
                                        <div>{{ challenge.solution }}</div>
                                    </el-collapse-item>
                                </el-collapse>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="case-study-quiz">
                <h4>基于你对LDA应用场景的探索，回答以下问题：</h4>

                <div class="quiz-item">
                    <p class="question">1. 在以下哪个应用场景中，LDA通常会与PCA一起使用，以处理小样本高维数据？</p>
                    <el-radio-group v-model="quizAnswers[0]">
                        <el-radio :label="0">文本分类</el-radio>
                        <el-radio :label="1">人脸识别</el-radio>
                        <el-radio :label="2">金融风险评估</el-radio>
                        <el-radio :label="3">市场细分</el-radio>
                    </el-radio-group>
                </div>

                <div class="quiz-item">
                    <p class="question">2. LDA在医学诊断中的主要优势是什么？</p>
                    <el-radio-group v-model="quizAnswers[1]">
                        <el-radio :label="0">能处理大量医学图像数据</el-radio>
                        <el-radio :label="1">能同时进行特征选择和降维</el-radio>
                        <el-radio :label="2">能基于类别信息提取最具判别力的特征</el-radio>
                        <el-radio :label="3">计算速度快，适合实时诊断</el-radio>
                    </el-radio-group>
                </div>

                <div class="quiz-item">
                    <p class="question">3. 当LDA应用于具有多个类别的数据集时，通常需要：</p>
                    <el-radio-group v-model="quizAnswers[2]">
                        <el-radio :label="0">增加特征数量以确保类别可分</el-radio>
                        <el-radio :label="1">假设所有类别具有相同的协方差矩阵</el-radio>
                        <el-radio :label="2">使用非线性核扩展（Kernel LDA）</el-radio>
                        <el-radio :label="3">将多类问题转化为多个二分类问题</el-radio>
                    </el-radio-group>
                </div>

                <div class="quiz-actions">
                    <el-button type="primary" @click="checkAnswers" :disabled="!allQuestionsAnswered || quizChecked">
                        提交答案
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

            <div class="action-buttons" v-if="quizCorrect">
                <el-button type="primary" @click="completeSection">
                    继续学习 <i class="el-icon-arrow-right"></i>
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
    name: 'ApplicationsOfLDA',
    props: {
        sectionId: {
            type: String,
            default: 'lda-applications'
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
            title: "LDA应用场景",
            markdownContent: `
  # LDA应用场景
  
  线性判别分析（LDA）作为一种强大的监督降维和分类算法，在多个领域有着广泛的应用。本节将探讨LDA在各个领域的实际应用案例，帮助你了解如何将LDA应用于解决实际问题。
  
  ## LDA的应用特点
  
  LDA特别适合以下类型的应用场景：
  
  1. **需要降维的分类问题**：当数据具有高维特征但样本数量有限时，LDA可以有效降低维度并保留类别信息。
  
  2. **需要可解释性的应用**：LDA生成的投影方向具有明确的物理或统计解释，这在医学诊断、风险评估等需要可解释性的领域很有价值。
  
  3. **类内方差小而类间方差大的数据**：当不同类别的数据相对集中且类别间差异明显时，LDA表现最佳。
  
  ## LDA的主要应用领域
  
  ### 1. 人脸识别与生物特征识别
  
  在人脸识别领域，LDA被广泛用于提取脸部图像的判别特征。"Fisherfaces"方法（基于LDA）是经典的人脸识别算法，它能有效处理光照变化问题。
  
  ### 2. 文本分类与文档检索
  
  LDA可以用于从文本数据中提取最具判别力的特征，帮助对文档进行分类。
  
  ### 3. 生物信息学
  
  在基因表达分析、蛋白质分类等生物信息学任务中，LDA常用于高维生物数据的降维和分类。
  
  ### 4. 金融与风险评估
  
  LDA可以用于信用评分、欺诈检测等金融应用，通过分析交易特征帮助识别风险模式。
  
  ### 5. 医学诊断与图像分析
  
  在医学领域，LDA被用于分析医学影像和生物医学数据，帮助疾病诊断和分类。
  
  ## LDA与其他方法的结合
  
  在实际应用中，LDA通常与其他算法结合使用，以获得更好的性能：
  
  - **PCA+LDA**：先用PCA降维以避免奇异性问题，再用LDA进行有监督降维
  - **Kernel LDA**：将LDA扩展到非线性情况，处理线性不可分的数据
  - **Ensemble方法**：将LDA作为集成学习的基分类器之一
  
  在下面的互动练习中，你可以探索LDA在不同领域的具体应用案例，了解LDA如何解决实际问题。
        `,
            isCompleted: false,

            // 应用场景数据
            activeCategory: 'face-recognition',
            applicationData: {
                title: "人脸识别 (Fisherfaces)",
                tags: ["计算机视觉", "生物特征识别", "身份验证"],
                image: "/api/placeholder/400/300",
                description: "Fisherfaces是基于LDA的经典人脸识别方法，由<strong>Belhumeur, Hespanha和Kriegman</strong>在1997年提出。与基于PCA的Eigenfaces相比，Fisherfaces能更好地处理光照变化问题，因为它专注于最大化类间差异（不同人）而最小化类内差异（同一个人在不同条件下）。",
                ldaRoles: [
                    "降低人脸图像的维度（从数千像素到几十个特征）",
                    "提取最能区分不同人脸的特征",
                    "减轻光照变化、表情变化等干扰因素的影响",
                    "在投影空间中构建更有效的分类边界"
                ],
                research: "Yale人脸数据库和ORL人脸数据库的实验表明，在光照条件变化较大的情况下，Fisherfaces的识别率显著高于Eigenfaces。这使得LDA成为人脸识别研究中的基础算法之一。",
                challenges: [
                    {
                        title: "小样本大维度问题",
                        solution: "通常先使用PCA降维以避免类内散布矩阵奇异的问题，然后再应用LDA，这种方法被称为PCA+LDA或Fisherfaces。"
                    },
                    {
                        title: "非线性问题",
                        solution: "对于非线性可分的人脸数据，可以使用核方法扩展LDA（Kernel LDA），将数据映射到高维空间后再进行线性判别。"
                    },
                    {
                        title: "实时处理需求",
                        solution: "通过优化算法实现和利用增量式LDA，可以实现更高效的计算，满足实时识别的需求。"
                    }
                ]
            },
            applicationDataMap: {
                'face-recognition': {
                    title: "人脸识别 (Fisherfaces)",
                    tags: ["计算机视觉", "生物特征识别", "身份验证"],
                    image: "/api/placeholder/400/300",
                    description: "Fisherfaces是基于LDA的经典人脸识别方法，由<strong>Belhumeur, Hespanha和Kriegman</strong>在1997年提出。与基于PCA的Eigenfaces相比，Fisherfaces能更好地处理光照变化问题，因为它专注于最大化类间差异（不同人）而最小化类内差异（同一个人在不同条件下）。",
                    ldaRoles: [
                        "降低人脸图像的维度（从数千像素到几十个特征）",
                        "提取最能区分不同人脸的特征",
                        "减轻光照变化、表情变化等干扰因素的影响",
                        "在投影空间中构建更有效的分类边界"
                    ],
                    research: "Yale人脸数据库和ORL人脸数据库的实验表明，在光照条件变化较大的情况下，Fisherfaces的识别率显著高于Eigenfaces。这使得LDA成为人脸识别研究中的基础算法之一。",
                    challenges: [
                        {
                            title: "小样本大维度问题",
                            solution: "通常先使用PCA降维以避免类内散布矩阵奇异的问题，然后再应用LDA，这种方法被称为PCA+LDA或Fisherfaces。"
                        },
                        {
                            title: "非线性问题",
                            solution: "对于非线性可分的人脸数据，可以使用核方法扩展LDA（Kernel LDA），将数据映射到高维空间后再进行线性判别。"
                        },
                        {
                            title: "实时处理需求",
                            solution: "通过优化算法实现和利用增量式LDA，可以实现更高效的计算，满足实时识别的需求。"
                        }
                    ]
                },
                'text-classification': {
                    title: "文本分类与主题建模",
                    tags: ["自然语言处理", "文档检索", "主题提取"],
                    image: "/api/placeholder/400/300",
                    description: "在文本分析领域，LDA被用于从高维文本特征（如词袋或TF-IDF表示）中提取最具判别力的特征，帮助对文档进行分类。注意，这里的LDA与主题建模中的<strong>潜在狄利克雷分配(Latent Dirichlet Allocation)</strong>不同，尽管它们共享相同的缩写。",
                    ldaRoles: [
                        "从高维文本特征中提取低维判别特征",
                        "降低稀疏性问题的影响",
                        "提高文本分类的准确性和效率",
                        "在多语言文档分类中表现出色"
                    ],
                    research: "研究表明，在新闻文章分类、垃圾邮件过滤等任务中，基于LDA的特征提取方法能显著提高分类性能。特别是当与词向量(Word Embeddings)等现代NLP技术结合时，可以捕获更丰富的语义信息。",
                    challenges: [
                        {
                            title: "高维稀疏性",
                            solution: "文本数据往往是高维稀疏的，可以使用词嵌入等技术降低初始维度，然后应用LDA进一步提取判别特征。"
                        },
                        {
                            title: "类间重叠",
                            solution: "对于主题相近的文档类别，可以使用非线性核扩展LDA或结合深度学习方法。"
                        },
                        {
                            title: "新词/未见词问题",
                            solution: "使用基于字符级别或子词级别的特征，或采用增量学习策略来适应新词汇。"
                        }
                    ]
                },
                // ApplicationsOfLDA.vue (第二部分) - 继续完成应用场景映射

                'bioinformatics': {
                    title: "生物信息学与基因表达分析",
                    tags: ["基因组学", "蛋白质分类", "生物标记物发现"],
                    image: "/api/placeholder/400/300",
                    description: "在生物信息学领域，LDA被广泛应用于分析高维生物数据，如基因表达谱、蛋白质序列特征等。通过LDA，研究人员可以从成千上万个基因或特征中识别出最相关的生物标记物，进行疾病分类或表型预测。",
                    ldaRoles: [
                        "识别与特定疾病或表型相关的关键基因或蛋白质",
                        "降低高通量生物数据的维度以进行可视化和分析",
                        "构建基于分子特征的疾病分类模型",
                        "发现潜在的生物标记物用于诊断和预后预测"
                    ],
                    research: "在癌症研究中，LDA已被用于从基因表达数据中识别出与不同癌症亚型相关的特征，帮助实现更精准的分类和个体化治疗。例如，在乳腺癌、白血病等癌症亚型分类研究中，LDA显示出优于无监督方法的性能。",
                    challenges: [
                        {
                            title: "样本数量远少于特征数",
                            solution: "在基因表达分析中，通常有成千上万个基因但只有几十或几百个样本，可以先使用过滤方法或其他方法（如PCA）进行初步降维，然后再应用LDA。"
                        },
                        {
                            title: "类别不平衡",
                            solution: "生物样本中某些疾病类型可能样本数很少，可以采用加权LDA或结合过采样/欠采样技术来处理类别不平衡问题。"
                        },
                        {
                            title: "非线性关系",
                            solution: "生物系统中的关系往往是非线性的，可以使用核LDA或将LDA与非线性方法（如神经网络）结合使用。"
                        }
                    ]
                },
                'finance': {
                    title: "金融风险评估与欺诈检测",
                    tags: ["信用评分", "欺诈检测", "市场细分"],
                    image: "/api/placeholder/400/300",
                    description: "在金融领域，LDA被应用于信用评分、欺诈检测和客户细分等任务。通过分析交易历史、客户行为和财务指标等特征，LDA可以帮助识别风险模式和差异化客户群体。",
                    ldaRoles: [
                        "从多维金融特征中提取最具判别力的风险指标",
                        "将客户分类为不同的信用风险级别",
                        "识别异常交易模式进行欺诈检测",
                        "对客户进行细分以实现精准营销"
                    ],
                    research: "研究表明，基于LDA的信用评分模型在预测借款人违约风险方面表现出色。在欺诈检测领域，LDA与其他机器学习方法结合使用，可以有效减少虚假交易，提高金融安全。",
                    challenges: [
                        {
                            title: "类别严重不平衡",
                            solution: "欺诈案例通常很少，可以使用加权LDA、代价敏感学习或结合采样技术来处理严重不平衡问题。"
                        },
                        {
                            title: "实时决策需求",
                            solution: "金融系统通常需要实时决策，可以优化LDA实现或使用增量学习方法以满足低延迟要求。"
                        },
                        {
                            title: "模型可解释性要求",
                            solution: "金融监管要求模型具有可解释性，LDA的优势在于其提取的特征具有明确的统计解释，更容易向监管机构和利益相关者解释决策依据。"
                        }
                    ]
                },
                'medical': {
                    title: "医学诊断与医学图像分析",
                    tags: ["疾病诊断", "医学成像", "生物标记物"],
                    image: "/api/placeholder/400/300",
                    description: "在医学领域，LDA被广泛应用于分析医学图像和临床数据，帮助疾病诊断、分类和预后预测。通过提取最相关的特征，LDA可以帮助医生更准确地区分不同疾病或疾病亚型。",
                    ldaRoles: [
                        "从医学影像中提取区分良恶性病变的关键特征",
                        "基于临床特征将患者分类为不同的风险组",
                        "降低高维医学数据的维度以便于可视化和解释",
                        "识别与特定疾病相关的生物标记物模式"
                    ],
                    research: "在肿瘤分类、神经影像学和心脏病学等领域，LDA被证明是有效的分析工具。例如，在阿尔茨海默病研究中，LDA用于从脑磁共振成像(MRI)数据中提取特征，帮助区分健康人群、轻度认知障碍和阿尔茨海默病患者。",
                    challenges: [
                        {
                            title: "数据高维性",
                            solution: "医学图像和基因组数据通常是高维的，可以先使用特征选择或PCA进行初步降维，然后再应用LDA。"
                        },
                        {
                            title: "样本量有限",
                            solution: "在罕见疾病研究中样本量经常有限，可以结合正则化技术或迁移学习来增强LDA的泛化能力。"
                        },
                        {
                            title: "临床决策的不确定性评估",
                            solution: "医学诊断需要评估不确定性，可以基于LDA的概率输出构建置信区间，或结合贝叶斯方法提供更完整的不确定性评估。"
                        }
                    ]
                }
            },

            // 问题回答
            quizAnswers: [null, null, null],
            correctAnswers: [1, 2, 1],
            quizChecked: false,
            quizCorrect: false,

            // 回应部分数据
            showResponse: false,
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
            return this.quizCorrect ? 'el-icon-check correct' : 'el-icon-close incorrect';
        },
        hasNext() {
            return this.sectionIndex < this.totalSections;
        },
        allQuestionsAnswered() {
            return this.quizAnswers.every(answer => answer !== null);
        }
    },
    created() {
        // 检查该部分是否已完成
        const completedSections = this.getCompletedSections();
        this.isCompleted = completedSections.includes(this.sectionId);
    },
    methods: {
        selectCategory(key) {
            this.activeCategory = key;
            this.applicationData = this.applicationDataMap[key];
        },
        checkAnswers() {
            this.quizChecked = true;

            // 检查答案是否全部正确
            const allCorrect = this.quizAnswers.every((answer, index) => answer === this.correctAnswers[index]);
            this.quizCorrect = allCorrect;

            // 生成回应
            if (allCorrect) {
                this.response = `
### 🎉 太棒了！所有答案都正确！

你已经很好地理解了LDA在各个领域的应用特点：

1. 在人脸识别领域，确实常将LDA与PCA结合使用（Fisherfaces方法），以处理小样本高维数据，避免类内散布矩阵奇异的问题。

2. LDA在医学诊断中的主要优势确实是能基于类别信息提取最具判别力的特征，这有助于区分不同疾病类型或病变阶段。

3. 当LDA应用于多类别数据集时，确实通常假设所有类别具有相同的协方差矩阵，这是LDA的基本假设之一。

通过本节学习，你应该已经了解了LDA在不同领域的实际应用方式，以及如何针对不同应用场景处理LDA的局限性。
  `;
            } else {
                // 找出错误的答案
                let errorMessages = "请仔细回顾以下问题的答案：\n\n";

                if (this.quizAnswers[0] !== this.correctAnswers[0]) {
                    errorMessages += "- 问题1：请回顾人脸识别（Fisherfaces）案例，在这种小样本高维数据场景下，常将LDA与PCA结合使用。\n\n";
                }

                if (this.quizAnswers[1] !== this.correctAnswers[1]) {
                    errorMessages += "- 问题2：LDA在医学诊断中的主要优势是能基于类别信息提取最具判别力的特征，而不仅仅是能处理大量数据或计算速度快。\n\n";
                }

                if (this.quizAnswers[2] !== this.correctAnswers[2]) {
                    errorMessages += "- 问题3：LDA的一个基本假设是所有类别具有相同的协方差矩阵，这在多类别场景下尤为重要。\n\n";
                }

                this.response = `
### 有些答案不正确

${errorMessages}

请再次浏览各个应用场景的详细信息，特别注意每个领域应用LDA时的关键假设、优势和挑战。
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