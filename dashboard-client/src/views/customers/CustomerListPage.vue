<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Customers"
    sub-title="This is a subtitle of customers page" />

    <a-layout-content style="padding: 0 50px">
        <div class="feature">
            <a-cascader v-model:value="value" :options="options" placeholder="Please select" :allowClear="false" />            
            <a-button type="primary" style="margin-left:10px;" @click="showModalAdd" >Add</a-button>
            <a-button type="primary" style="margin-left:10px;" @click="showModalSendMessage">
                <mail-filled />
            </a-button>
        </div>
        <a-table :columns="columns" :data-source="data" :scroll="{ x: 1000, y: 500 }">
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

        <a-modal v-model:visible="visibleAdd" title="Add Customer" @ok="handleAdd()" >
            <a-tabs v-model:activeKey="activeKey">
                <a-tab-pane key="1" tab="Add">
                    <a-form
                        :model="customer"
                        :label-col="{ span: 4 }"
                        :wrapper-col="{ span: 16 }"
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
                </a-tab-pane>

                <a-tab-pane key="2" tab="File">
                    <div class="space-align-container">
                        <a-image
                            :width="200"
                            href="/staticfiles/example.png"
                            style="padding:10px"
                        />
                        <a-space direction="vertical" style="width: 100%" size="large">
                            <a-upload
                                v-model:file-list="fileList"
                                list-type="picture"
                                :max-count="1"
                                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                                accept=".csv"
                                :beforeUpload="beforeUpload"
                                @remove="removeFile"
                            >
                            <a-button>
                                <upload-outlined></upload-outlined>
                                Upload (Max: 1)
                            </a-button>
                            </a-upload>
                        </a-space>
                    </div>
                </a-tab-pane>
            </a-tabs>
        </a-modal>

        <a-modal v-model:visible="visibleEdit" title="Edit" @ok="handleEdit()" >
          <a-form
            :model="customer"
            :label-col="{ span: 4 }"
            :wrapper-col="{ span: 16 }"
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

        <a-modal v-model:visible="visibleSendMessage" title="Message" @ok="handleSendMessage()" >
          <a-form
            :model="content"
            :label-col="{ span: 24 }"
            :wrapper-col="{ span: 24 }"
            name="nest-messages"
            :validate-messages="validateMessages"
            >
                <div>    
                    <a-space size="small" style="margin-bottom:10px">
                        <a-button type="dashed" size="small" @click="insertText(0)">review_link</a-button>
                        <a-button type="dashed" size="small" @click="insertText(1)">full_name</a-button>
                    </a-space>
                </div>

                <a-form-item :name="['message']">
                    <a-textarea v-model:value="content.message" />
                </a-form-item>

            </a-form>
        </a-modal>

    </a-layout-content>
    

</template>

<script lang="ts">
import { notification } from 'ant-design-vue';
import BaseRequest from '@/core/BaseRequest.js'
import { UploadOutlined, StarFilled, MailFilled } from '@ant-design/icons-vue';
import jQuery from 'jquery'



export default({
    data() {
        return {
            options: [],
            value: [],
            errors: {},
            data: [],
            store: [],
            columns: [],
            visibleAdd: false,
            visibleEdit: false,
            visibleDelete: false,
            visibleSendMessage: false,
            customers: [],
            id_customer_edit: '',
            id_customer_del: '',
            name_customer_del: '',
            customer: {
                full_name: '',
                phone: '',
                email: ''
            },
            validateMessages: {},
            activeKey: '1',
            fileList: [],
            lines_file: [],
            content: {
                message: '',
            },
            characters: ['{{review_link}}', '{{full_name}}']
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
                width: '5%'
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

        showModalSendMessage: function() {
            this.content.message = ''
            this.visibleSendMessage = true
        },

        showModalAdd: function() {
            this.customer = {}
            this.visibleAdd = true
        },

        handleAdd: function() {
            if (this.activeKey === '1') {
                BaseRequest.post('store/addCustomer/' + this.value[0], this.customer)
                .then(response => {
                    this.customer = response.data
                    this.getCustomer()
                    this.addSuccessNotification(1)
                    this.visibleAdd = false
                    this.errors = {}
                })
                .catch(error=> {
                    this.errors = error.response.data
                    notification['error']({
                        message: 'Add error!',
                        description: 'Error.',
                    });
                });
            }
            else {
                for (let key in this.lines_file) {
                    this.customer = {
                        phone: this.lines_file[key][0],
                        full_name: this.lines_file[key][1],
                        email: this.lines_file[key][2]
                    }

                    BaseRequest.post('store/addCustomer/' + this.value[0], this.customer)
                    .then(response => {
                        this.customer = response.data
                        this.getCustomer()
                        this.errors = {}
                        console.log('ok')
                    })
                    .catch(error=> {
                        this.errors = error.response.data
                    });  
                }

                this.customer = {}
                this.visibleAdd = false
                this.addSuccessNotification(this.lines_file.length)
            }


        },

        showModalEdit: function(id) {
            this.id_customer_edit = id

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
                this.errors = {}
            })
            .catch(error=> {
                this.errors = error.response.data
                notification['error']({
                    message: 'Update error!',
                    description: this.errors.phone,
                });
            });
        },

        showModalDelete: function(id, name) {
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
                this.errors = {}
            })
            .catch(error=> {
                this.errors = error.response.data
            });
        },

        addSuccessNotification: function(count: any) {
            notification['success']({
                message: 'Add successfully!',
                description:
                count + ' customer was added! ',
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
        },

        beforeUpload: function(file: any) {
            console.log(file)
            const reader = new FileReader();
            let text = []
            reader.onload = e => {
                this.lines_file = []
                text = ((e.target.result as string).split(/\r\n|\r|\n/))
                for (var i=1; i<text.length-1; i++) {
                    var data = text[i].split(',')
                    var tarr = []
                    for (var j=0; j<3; j++) {
                        tarr.push(data[j])
                    }
                    this.lines_file.push(tarr)
                }
                console.log(this.lines_file)
            };
            reader.readAsText(file);

            // Prevent upload

            return false;
        },

        removeFile: function(file: any) {
            this.lines_file = []
        },

        insertText: function(value: any) {
            const $ = jQuery;
            var cursorPosition = $('#nest-messages_message').prop("selectionStart");

            let result = this.content.message.slice(0, cursorPosition )  + this.characters[value] + this.content.message.slice(cursorPosition)            
            this.content.message = result
        }
    },

    components: {
        UploadOutlined,
        StarFilled,
        MailFilled
    }

});

</script>

<style scoped>
.editable-row-operations a {
  margin-right: 8px;
}

.feature {
    margin-bottom: 10px;
}

.space-align-container {
  display: flex;
  flex-wrap: wrap;
  align-content: space-around;
  justify-content: center;
}

</style>