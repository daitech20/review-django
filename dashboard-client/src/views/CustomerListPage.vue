<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Customers"
    sub-title="This is a subtitle of customers page" />

    <a-layout-content style="padding: 0 50px">
        <a-cascader v-model:value="value" :options="options" placeholder="Please select" :allowClear="false" />            
        <a-table :columns="columns" :data-source="data">
            <template #bodyCell="{ column, record }">
              <template v-if="column.dataIndex === 'name'">
                  <a>{{ record.name }}</a>
              </template>
              <template v-else-if="column.key === 'action'">
                <span>
                    <a-button type="primary" size="small" @click="showModalEdit(record.id)" >Edit</a-button>
                </span>
                <span>
                    <a-button type="primary" danger size="small" @click="showModalDelete(record.id, record.name)">Delete</a-button>
                </span>
              </template>
            </template>
        </a-table>
        <a-modal v-model:visible="visibleEdit" title="Edit" @ok="handleEdit()" >
          <a-form
            :model="customer"
            v-bind="layout"
            name="nest-messages"
            :validate-messages="validateMessages"
            >
                <a-form-item :name="['full_name']" label="Full name">
                    <a-input v-model:value="customer.full_name" />
                </a-form-item>

                <a-form-item :name="['phone']" label="Phone">
                    <a-input v-model:value="customer.phone" />
                </a-form-item>

                <a-form-item :name="['email']" label="Email">
                    <a-input v-model:value="customer.email" />
                </a-form-item>

            </a-form>
        </a-modal>

        <a-modal v-model:visible="visibleDelete" title="Delete" @ok="handleDelete()">
          <p>
            Do you want to delete {{ name_customer_del }}?
          </p>
        </a-modal>

    </a-layout-content>
    

</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { CascaderProps } from 'ant-design-vue';
import { notification } from 'ant-design-vue';
import BaseRequest from '../core/BaseRequest.js'

export default({
    data() {
        return {
            options: [],
            value: [],
            errors: {},
            data: [],
            store: [],
            columns: [],
            visibleEdit: false,
            visibleDelete: false,
            customers: [],
            id_customer_edit: '',
            id_customer_del: '',
            name_customer_del: '',
            customer: {
                full_name: '',
                phone: '',
                email: ''
            },
            layout: {},
            validateMessages: {}
        }
    },

    mounted() {
        this.getData()
    },

    watch: {
        value: function() {
            this.getCustomer()
        }
    },

    methods: {
        getData: function() {
            this.columns = [
            {
                title: 'Id',
                dataIndex: 'id',
                key: 'id',
            },
            {
                title: 'Full name',
                dataIndex: 'name',
                key: 'name',
            },
            {
                title: 'Phone',
                dataIndex: 'phone',
                key: 'phone',
            },
            {
                title: 'Email',
                dataIndex: 'email',
                key: 'email',
            },
            {
                title: 'Action',
                dataIndex: 'action',
                key: 'action',
            },
            ];

            BaseRequest.get('store/')
            .then(response => {
                this.store = response.data;
                if (this.store.length > 0) {
                    this.value.push(this.store[0].store_slug)
                    this.data = []
                    BaseRequest.get('customer/' + this.store[0].store_slug)
                    .then(response => {
                        this.customers = response.data
                        for (const num in this.customers) {
                            this.data.push({
                                id: this.customers[num].id,
                                name: this.customers[num].full_name,
                                phone: this.customers[num].phone,
                                email: this.customers[num].email,
                            })
                        }
                    })
                    .catch(error=> {
                        this.errors = error.response.data
                    });
                } 
                
                for (let num in this.store) {
                    this.options.push({
                        value: this.store[num].store_slug,
                        label: this.store[num].store_name,
                    })
                }
            })
            .catch(error=> {
                this.errors = error.response.data
            });



        },

        getCustomer: function() {
            this.data = []
            BaseRequest.get('customer/' + this.value[0])
            .then(response => {
                this.customers = response.data
                for (const num in this.customers) {
                    this.data.push({
                        id: this.customers[num].id,
                        name: this.customers[num].full_name,
                        phone: this.customers[num].phone,
                        email: this.customers[num].email,
                    })
                }
            })
            .catch(error=> {
                this.errors = error.response.data
            });
        },

        showModalEdit: function(id: any) {
            this.id_customer_edit = id
            this.layout = {
                labelCol: { span: 4 },
                wrapperCol: { span: 16 },
            }

            BaseRequest.get('customer/update/' + this.id_customer_edit)
            .then(response => {
                this.customer = response.data
                
            })
            .catch(error=> {
                this.errors = error.response.data
            });
            this.visibleEdit = true
        },

        handleEdit: function() {
            BaseRequest.put('customer/update/' + this.id_customer_edit + '/', this.customer)
            .then(response => {
                this.customer = response.data
                this.getCustomer()
                this.updateSuccessNotification()
                this.visibleEdit = false
            })
            .catch(error=> {
                this.errors = error.response.data
            });
        },

        showModalDelete: function(id: any, name: any) {
            this.id_customer_del = id
            this.name_customer_del = name
            this.visibleDelete = true
        },

        handleDelete: function() {
            BaseRequest.delete('customer/update/' + this.id_customer_del)
            .then(response => {
                this.getCustomer()
                this.delSuccessNotification()
                this.visibleDelete = false
            })
            .catch(error=> {
                this.errors = error.response.data
                console.log(this.errors)
            });
        },

        updateSuccessNotification: function() {
            notification['success']({
                message: 'Update successfully!',
                description:
                'Customer was updated! ',
            });
        },

        delSuccessNotification: function() {
            notification['success']({
                message: 'Delete successfully!',
                description:
                'Customer was deleted! ',
            });
        }

    },

});

</script>

<style scoped>
.editable-row-operations a {
  margin-right: 8px;
}
</style>