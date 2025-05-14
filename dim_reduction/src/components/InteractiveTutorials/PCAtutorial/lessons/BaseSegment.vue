<template>
    <div class="segment">
        <!-- 标题部分 -->
        <h2 class="segment-title">{{ title }}</h2>

        <!-- Markdown内容展示部分 -->
        <div class="markdown-content">
            <div v-html="renderedMarkdown"></div>
        </div>

        <!-- 互动部分 - 只有在未完成状态时显示 -->
        <div class="interactive-section">
            <div class="interaction-container">
                <slot name="interaction"></slot>
            </div>
        </div>

        <!-- 回应部分 - 根据用户互动展示 -->
        <div v-if="hasResponse" class="response-section">
            <el-alert :title="responseTitle" :type="responseType" :description="responseDescription" show-icon>
            </el-alert>
        </div>

        <!-- 继续按钮 - 仅在完成当前片段后显示 -->
        <div v-if="isCompleted && !isLastSegment" class="continue-section">
            <el-button type="primary" @click="continueToNext">继续学习下一部分</el-button>
        </div>

        <!-- 总结按钮 - 仅在最后一个片段完成后显示 -->
        <div v-if="isCompleted && isLastSegment" class="summary-section">
            <el-button type="success" @click="showSummary">查看学习总结</el-button>
        </div>
    </div>
</template>

<script>
import { marked } from 'marked';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}

export default {
    name: 'BaseSegment',
    props: {
        title: {
            type: String,
            required: true
        },
        content: {
            type: String,
            required: true
        },
        segmentId: {
            type: String,
            required: true
        },
        isLastSegment: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            isCompleted: false,
            hasResponse: false,
            responseTitle: '',
            responseDescription: '',
            responseType: 'info', // 'success', 'warning', 'info', 'error'
        };
    },
    computed: {
        renderedMarkdown() {
            // return marked(this.content);
            const withMath = renderMath(this.content);
            return marked(withMath);
        }
        //     renderedHtml() {
        //   const withMath = renderMath(this.rawMarkdown)
        //   return marked(withMath)
        // }
    },
    methods: {
        // 完成当前片段
        completeSegment() {
            this.isCompleted = true;
            console.log("baseSection", this.segmentId);
            // 通知父组件该片段已完成
            this.$emit('segment-completed', this.segmentId);
            // 使用provide/inject进行组件间通信
            // this.$root.$emit('segment-completed', this.segmentId);
        },

        // 显示回应
        showResponse(title, description, type = 'info') {
            this.responseTitle = title;
            this.responseDescription = description;
            this.responseType = type;
            this.hasResponse = true;
        },

        // 隐藏回应
        // hideResponse() {
        //     this.hasResponse = false;
        // },

        // 继续到下一部分
        continueToNext() {
            this.$root.$emit('unlock-next-segment', this.segmentId);
        },

        // 显示学习总结
        showSummary() {
            this.$root.$emit('show-summary');
        }
    },
    inject: {
        unlockNextSegment: {
            default: () => { }
        }
    },
    mounted() {
        // 监听片段完成事件
        // this.$on('segment-completed', this.completeSegment);

        // 设置相应事件侦听器
        this.$root.$on('unlock-next-segment', (segmentId) => {
            if (segmentId === this.segmentId) {
                this.unlockNextSegment(segmentId);
            }
        });
    }
}
</script>

<style scoped>
.segment {
    padding: 15px;
}

.segment-title {
    margin-bottom: 20px;
    color: #409EFF;
    border-bottom: 2px solid #ebeef5;
    padding-bottom: 10px;
}

.markdown-content {
    margin-bottom: 20px;
    line-height: 1.6;
}

.interactive-section {
    background-color: #f7f9fc;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    border-left: 4px solid #409EFF;
}

.response-section {
    margin: 20px 0;
}

.continue-section,
.summary-section {
    margin-top: 30px;
    text-align: center;
}

/* KaTeX 样式覆盖 */
:deep(.katex-block) {
    overflow-x: auto;
    overflow-y: hidden;
    text-align: center;
    padding: 10px 0;
}
</style>