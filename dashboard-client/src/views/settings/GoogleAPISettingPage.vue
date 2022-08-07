<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Google APIs"
    sub-title="This is a subtitle of Google API settings page" />

    <a-layout-content style="padding: 0 50px">
        <a-form
            :model="google_api"
            v-bind="layout"
            name="nest-messages"
            :validate-messages="validateMessages"
            @finish="onFinish"
        >
            <a-form-item :name="['name']" label="Name" :rules="[{ required: true }]" >
                <a-input v-model:value="google_api.name"/>
            </a-form-item>

            <a-form-item :name="['client_id']" label="Client id" :rules="[{ required: true }]">
                <a-input v-model:value="google_api.client_id" />
            </a-form-item>

            <a-form-item :name="['secret']" label="Secret" :rules="[{ required: true }]">
                <a-input v-model:value="google_api.secret" />
            </a-form-item>

            <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 8 }">
                <a-button type="primary" html-type="submit" >Submit</a-button>
            </a-form-item>
        </a-form>

    </a-layout-content>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import BaseRequest from '../../core/BaseRequest.js'
import { notification } from 'ant-design-vue';

export default({
    data() {
        return {
            google_api: {
                name: '',
                client_id: '',
                secret: ''
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

            BaseRequest.get('social/application/1/')
            .then(response => {
                    this.google_api.name = response.data.name
                    this.google_api.client_id = response.data.client_id
                    this.google_api.secret = response.data.secret
                }
            )
            
        },

        onFinish: function(values: any) {
            BaseRequest.put('social/application/1/', this.google_api)
            .then(response => {
                    this.errors = {}
                    this.updateSuccessNotification()   
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
                'Social application was updated! ',
            });
        }
    }
})
</script>