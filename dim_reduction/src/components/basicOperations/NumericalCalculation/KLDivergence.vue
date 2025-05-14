<template>
    <div>
        <el-card shadow="hover">
            <h3>计算 KL 散度</h3>
            <el-form label-width="150px">
                <el-form-item label="启用早停">
                    <el-switch v-model="enableEarlyStop"></el-switch>
                </el-form-item>
                <el-form-item label="容忍误差" v-if="enableEarlyStop">
                    <el-input-number v-model="tolerance" :min="0.001" :max="0.1" step="0.001" />
                </el-form-item>
                <el-button type="primary" @click="applyKLDivergence">计算</el-button>
            </el-form>
        </el-card>
    </div>
</template>

<script>
export default {
    data() {
        return {
            enableEarlyStop: false,
            tolerance: 0.01
        };
    },
    methods: {
        applyKLDivergence() {
            this.$emit('applyKLDivergence', {
                operation: '计算 KL 散度',
                parameters: {
                    enableEarlyStop: this.enableEarlyStop,
                    tolerance: this.enableEarlyStop ? this.tolerance : null
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