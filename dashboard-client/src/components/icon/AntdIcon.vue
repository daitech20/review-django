<template>
    <component v-if="isLoaded" :is="icon" />
</template>

<script>
import * as AntdIcons from '@ant-design/icons-vue/lib/icons'

export default {
    data() {
        return {
            isLoaded: false,
            iconCollection: {}
        }
    },
    props: {
        name: {
            type: String,
            require: true
        }
    },
    computed: {
        icon() {
            return this.iconCollection[this.name] ?? null;
        }
    },
    mounted() {
        this.isLoaded = true
        this.iconCollection = AntdIcons;
    }
}
</script>