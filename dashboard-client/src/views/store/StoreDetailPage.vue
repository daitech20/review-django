<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Store"
    sub-title="This is a subtitle of detail store page" />
    <div style="padding:10px; margin-left:50px">
        <a-button type="primary" size="small" @click="getLinkStore" >Get link store</a-button>
    </div>
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
                :rules="[{ required: true, message: 'Please input store name!' }]"
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

            <a-form-item :name="['logo']" label="Logo" :rules="[{ required: true }]">
            <a-input v-model:value="store.logo" />
            </a-form-item>

            <a-form-item
                :name="['website']"
                label="Website"
                :rules="[{ required: true, message: 'Please input your website!' }]"
            >
                <a-input v-model:value="store.website" />
            </a-form-item>

            <a-form-item
                :name="['domain']"
                label="Domain"
                :rules="[{ required: true, message: 'Please input your domain website!' }]"
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
const reviewUrl = import.meta.env.VITE_API_BASE_URL.trimEnd('/')+'/review/';


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
                url_map_store: '',
                store_slug: ''
            },
            errors: {}
        }
    },

    mounted() {
        this.getData()
    },

    methods: {
        getData: function() {
            BaseRequest.get('store/detail/' + this.$route.params.store_slug)
            .then(response => {
                    this.store.store_name = response.data.store_name
                    this.store.title = response.data.title
                    this.store.logo = response.data.logo
                    this.store.message = response.data.message
                    this.store.domain = response.data.domain
                    this.store.website = response.data.website
                    this.store.url_map_store = response.data.url_map_store
                    this.store.store_slug = response.data.store_slug
                }
            )
        },

        onFinish: function() {
            BaseRequest.put('store/update/' + this.$route.params.store_slug, this.store)
            .then(response => {
                    this.errors = {}
                    this.updateSuccessNotification()
                    this.$router.push({ name: 'store.list'});
                }
            )
            .catch(error=> {
                this.errors = error.response.data
                console.log(this.errors)
            });
        },

        updateSuccessNotification: function() {
            notification['success']({
                message: 'Update successfully!',
                description:
                'Store was updated! ',
            });
        },

        getLinkStore: function() {
            var el = document.createElement('textarea')
            el.value = reviewUrl + this.store.store_slug
            el.setAttribute('readonly', '')
            document.body.appendChild(el)
            el.select();
            // Copy text to clipboard
            document.execCommand('copy')
            // Remove temporary element
            document.body.removeChild(el)

            notification['success']({
                message: 'Get link store successfully!'
            });
        }
    },
})
</script>