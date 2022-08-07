<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Store"
    sub-title="This is a subtitle of create store page" />
    <a-layout-content style="padding: 0 50px">
        <a-form
            :model="store"
            name="nest-messages"
            :label-col="{ span: 4 }"
            :wrapper-col="{ span: 16 }"
            @finish="onFinish"
        >
            <a-form-item
                :name="['store_name']"
                label="Name Store"
                :rules="[{ required: true, message: 'Please input name store!' }]"
                :validateStatus="errors.store_name ? 'error': ''"
            >
                <a-input v-model:value="store.store_name" />
                <a-typography-text v-if="errors.store_name" type="danger">
                    {{errors.store_name[0]}}
                </a-typography-text>
            </a-form-item>

            <a-form-item
                :name="['title']"
                label="Title"
                :rules="[{ required: true, message: 'Please input title!' }]"
            >
                <a-input v-model:value="store.title" />
            </a-form-item>

            <a-form-item
                :name="['logo']"
                label="Logo"
                :rules="[{ required: true, message: 'Please input logo!' }]"
            >
                <a-input v-model:value="store.logo" />
            </a-form-item>

            <a-form-item
                :name="['website']"
                label="Website"
                :rules="[{ required: true, message: 'Please input website!' }]"
            >
                <a-input v-model:value="store.website" />
            </a-form-item>

            <a-form-item
                :name="['domain']"
                label="Domain"
                :rules="[{ required: true, message: 'Please input your domain!' }]"
            >
                <a-input v-model:value="store.domain" />
            </a-form-item>

            <a-form-item
                :name="['message']"
                label="Message"
                :rules="[{ required: true, message: 'Please input message!' }]"
            >
                <a-textarea v-model:value="store.message" />
            </a-form-item>

            <a-form-item
                :name="['url_map_store']"
                label="Url map"
                :rules="[{ required: true, message: 'Please input url map review!' }]"
            >
                <a-input v-model:value="store.url_map_store" />
            </a-form-item>

            <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
                <a-button type="primary" html-type="submit" >Submit</a-button>
            </a-form-item>
        </a-form>
    </a-layout-content>
</template>

<script>
import BaseRequest from '@/core/BaseRequest.js'
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
            validateMessages: {},
            errors: {
            }
        }
    },

    methods: {
        onFinish: function() {
            BaseRequest.post('store/create/', this.store)
            .then(response => {
                    this.errors = {}
                    this.addSuccessNotification()
                    this.$router.push({ name: 'store.list'});
                }
            )
            .catch(error=> {
                this.errors = error.response.data
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