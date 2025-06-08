<template>
    <span ref="formula"></span>
</template>

<script>
import katex from 'katex';
import 'katex/dist/katex.min.css';

export default {
    name: 'MathFormula',
    props: {
        expression: String,
        displayMode: {
            type: Boolean,
            default: false
        }
    },
    mounted() {
        this.renderFormula();
    },
    methods: {
        renderFormula() {
            katex.render(this.expression, this.$refs.formula, {
                displayMode: this.displayMode,
                throwOnError: false
            });
        }
    },
    watch: {
        expression() {
            this.renderFormula();
        }
    }
};
</script>