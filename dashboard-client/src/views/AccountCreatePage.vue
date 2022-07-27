<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Accounts"
    sub-title="This is a subtitle of create account page" />
    <a-layout-content style="padding: 0 50px">
        <a-form
            :model="user"
            name="basic"
            :label-col="{ span: 8 }"
            :wrapper-col="{ span: 16 }"
            @finish="onFinish"
        >
            <a-form-item
                label="Username"
                name="username"
                :rules="[{ required: true, message: 'Please input your username!' }]"
                :validateStatus="errors.username ? 'error': ''"
            >
                <a-input v-model:value="user.username" />
                <a-typography-text v-if="errors.username" type="danger">
                    {{errors.username}}
                </a-typography-text>
            </a-form-item>

            <a-form-item
                label="Password"
                name="password"
                :rules="[{ required: true, message: 'Please input your password!' }]"
                :validateStatus="errors.password ? 'error': ''"
            >
                <a-input-password v-model:value="user.password" />
                <a-typography-text v-if="errors.password" type="danger">
                    {{errors.password[0]}}
                </a-typography-text>
            </a-form-item>

            <a-form-item
                label="Password 2"
                name="password2"
                :rules="[{ required: true, message: 'Please input your password 2!' }]"
                :validateStatus="errors.password     ? 'error': ''"
            >
                <a-input-password v-model:value="user.password2" />
            </a-form-item>

            <a-form-item
                label="Email"
                name="email"
                :rules="[{ required: true, message: 'Please input your Email!' }, { type: 'email' }]"
                :validateStatus="errors.email ? 'error': ''"
            >
                <a-input v-model:value="user.email" />
                <a-typography-text v-if="errors.email" type="danger">
                    {{errors.email}}
                </a-typography-text>
            </a-form-item>

            <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
            </a-form-item>
        </a-form>
    </a-layout-content>
</template>

<script lang="ts">
import BaseRequest from '../core/BaseRequest.js'
import { notification } from 'ant-design-vue';

export default {
    data() {
        return {
            user: {
                username: '',
                password: '',
                password2: '',
                email: ''
            },
            errors: {
            }
        }
    },

    methods: {
        onFinish: function(values: any) {
            BaseRequest.post('register/', this.user)
            .then(response => {
                    console.log(response.data)
                    this.errors = {}
                    this.addSuccessNotification()
                    this.$router.push({ name: 'account.list'});
                }
            )
            .catch(error=> {
                this.errors = error.response.data
                console.log(this.errors)
            });
        },

        addSuccessNotification: function() {
            notification['success']({
                message: 'Create successfully!',
                description:
                'User was created! ',
            });
        }
    }
}
</script>

<style scoped>

</style>