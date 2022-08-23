<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Store"
    sub-title="This is a subtitle of create store page" />
    <a-layout-content style="padding: 0 50px">
        <a-form
            :model="store"
            v-bind="layout"
            name="nest-messages"
            :validate-messages="validateMessages"
            @finish="onFinish"
        >
            <a-form-item :name="['store_name']" label="Name Store" :rules="[{ required: true }]">
            <a-input v-model:value="store.store_name" />
            <a-typography-text v-if="errors.store_name" type="danger">
                {{errors.store_name[0]}}
            </a-typography-text>
            </a-form-item>
            <a-form-item :name="['title']" label="Title" :rules="[{ required: true }]">
            <a-input v-model:value="store.title" />
            </a-form-item>
            <a-form-item :name="['logo']" label="Logo" :rules="[{ required: true }]">
            <a-input v-model:value="store.logo" />
            </a-form-item>
            <a-form-item :name="['website']" label="Website" :rules="[{ required: true }]">
            <a-input v-model:value="store.website" />
            </a-form-item>
            <a-form-item :name="['domain']" label="Domain" :rules="[{ required: true }]">
            <a-input v-model:value="store.domain" />
            </a-form-item>
            <a-form-item :name="['message']" label="Message" :rules="[{ required: true }]">
            <a-textarea v-model:value="store.message" />
            </a-form-item>
            <a-form-item :name="['url_map_store']" label="Url map" :rules="[{ required: true }]">
            <a-input v-model:value="store.url_map_store" />
            </a-form-item>
            <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 8 }">
            <a-button type="primary" html-type="submit" >Submit</a-button>
            </a-form-item>
        </a-form>
    </a-layout-content>
</template>

<script lang="ts">
import BaseRequest from '@/core/BaseRequest'
import { notification } from 'ant-design-vue';

export default({
    data() {
        return {
            store: {
                store_name: '',
                title: '',
                logo: '',
                message: '',
                domain: '',
                website: '',
                url_map_store: ''
            },
            layout: {},
            validateMessages: {},
            errors: {
            }
        }
    },

    mounted() {
        this.getData()
    },

    methods: {
        getData: function() {
            this.layout = {
                labelCol: { span: 4 },
                wrapperCol: { span: 16 },
            }
            this.validateMessages = {
                required: '${label} is required!'
            }
        },
        onFinish: function(values: any) {
            BaseRequest.post('store/create/', this.store)
            .then(response => {
                    console.log(response.data)
                    this.store.store_name = response.data.store_name
                    this.store.title = response.data.title
                    this.store.logo = response.data.logo
                    this.store.message = response.data.message
                    this.store.domain = response.data.domain
                    this.store.website = response.data.website
                    this.store.url_map_store = response.data.url_map_store
                    this.errors = {}
                    this.addSuccessNotification()
                    this.$router.push({ name: 'store.list'});
                }
            )
            .catch(error=> {
                this.errors = error.response.data
                console.log(this.errors)
            });
        },

        addSuccessNotification: function() {
            notification['success']({
                message: 'Add successfully!',
                description:
                'Store was added! ',
            });
        }
    },
})
</script>