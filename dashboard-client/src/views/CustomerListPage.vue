<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Customers"
    sub-title="This is a subtitle of customers page" />

    

</template>

<script lang="ts">
import { cloneDeep } from 'lodash-es';
import { defineComponent, reactive, ref } from 'vue';
import type { UnwrapRef } from 'vue';
import BaseRequest from '../core/BaseRequest.js'

export default({
    props: {
        storeSlug: {
            type: String,
            required: true
        },
    },
});

</script>

<style scoped>
.editable-row-operations a {
  margin-right: 8px;
}
</style>