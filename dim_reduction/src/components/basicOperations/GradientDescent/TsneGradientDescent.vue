<template>
    <div>
        <el-card shadow="hover">
            <h3>梯度下降优化</h3>
            <el-form label-width="150px">
                <el-form-item label="学习率">
                    <el-input-number v-model="learningRate" :min="1" :max="1000" :step="1" />
                </el-form-item>
                <el-form-item label="迭代次数">
                    <el-input-number v-model="iterations" :min="10" :max="1000" :step="10" />
                </el-form-item>
                <el-form-item label="困惑度">
                    <el-input-number v-model="perplexity" :min="5" :max="50" />
                </el-form-item>
                <el-button type="primary" @click="applyGradientDescent">开始优化</el-button>
            </el-form>
        </el-card>
    </div>
</template>

<script>
export default {
    data() {
        return {
            learningRate: 200,
            iterations: 100,
            perplexity: 30
        };
    },
    methods: {
        applyGradientDescent() {
            this.$emit('applyGradientDescent', {
                operation: '梯度下降优化',
                parameters: {
                    learningRate: this.learningRate,
                    iterations: this.iterations,
                    perplexity: this.perplexity
                }
            });
        }
    }
};
</script>

<style scoped>
.el-card {
    margin-bottom: 20px;
}
</style>