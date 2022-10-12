<template>
	
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Message Log"
    sub-title="This is a messages log of store " />

    <a-layout-content style="padding: 0 50px">
    <a-cascader v-model:value="value" :options="options" placeholder="Please select" :allowClear="false" />
        <a-table class="ant-table-striped" :columns="columns" :data-source="data" :scroll="{ x: 1000, y: 500 }" :row-class-name="(_record, index) => (_record.status === 1 ? 'table-striped' : null)">
            <template #bodyCell="{ column, record }">
              <template v-if="column.dataIndex === 'id'">
                  <a>{{ record.id }}</a>
              </template>
              <template v-if="column.dataIndex === 'status'">
				  <span v-if="record.status === 1" style="color:red">Fail</span>
                  <span v-if="record.status === 0" style="color:greenyellow">Success</span>
			  </template>
            </template>
        </a-table>
    </a-layout-content>

</template>

<script>
import BaseRequest from '@/core/BaseRequest.js';
import { authStore } from '@/store/auth.store';
import { mapState } from 'pinia';

export default({
	data() {
		return {
			options: [],
			value: [],
			columns: [],
			messages: [],
			store: [],
			errors: {},
			data: [],
			visible: false,
		}
	},

	mounted() {
		this.getData()
	},

	watch: {
		value: function() {
		    this.getMessages()
		}
	},

	computed: {
		...mapState(authStore, ['isLoggedIn', 'user'])
	},

	methods: {
		getData: function() {
			this.columns = [
				{
				title: 'Id',
				dataIndex: 'id',
				key: 'id'
				},
				{
				title: 'From phone',
				dataIndex: 'from_phone',
				key: 'from_phone'
				},
				{
				title: 'To phone',
				dataIndex: 'to_phone',
				key: 'to_phone'
				},
				{
				title: 'Content',
				dataIndex: 'content',
				key: 'content',
                ellipsis: true
				},
				{
				title: 'Status',
				dataIndex: 'status',
				key: 'status'
				},
                {
				title: 'Sid',
				dataIndex: 'sid',
				key: 'sid'
				},
				{
				title: 'Created',
				dataIndex: 'created',
				key: 'created',
				ellipsis: true
				},
			];

			BaseRequest.get('store/')
			.then(response => {
			this.store = response.data;
			if (this.store.length > 0) {
				this.value.push(this.store[0].store_slug)
				this.data = []

				BaseRequest.get('messageLog/' + this.store[0].store_slug)
				.then(response => {
					this.messages = response.data;
					this.data = []
					for (const num in this.messages) {
						this.data.push({
                            id: this.messages[num].id,
                            from_phone: this.messages[num].from_phone,
                            to_phone: this.messages[num].to_phone,
                            content: this.messages[num].content,
                            status: this.messages[num].status,
                            sid: this.messages[num].sid,
                            created: this.messages[num].created
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

		getMessages: function() {
			this.data = []
			BaseRequest.get('messageLog/' + this.value[0])
			.then(response => {
				this.messages = response.data
				for (const num in this.messages) {
					this.data.push({
                        id: this.messages[num].id,
                        from_phone: this.messages[num].from_phone,
                        to_phone: this.messages[num].to_phone,
                        content: this.messages[num].content,
                        status: this.messages[num].status,
                        sid: this.messages[num].sid,
                        created: this.messages[num].created
					})
				}
			})
			.catch(error=> {
				this.errors = error.response.data
			});
		}
	}
})

</script>

<style scoped>
.ant-table-striped :deep(.table-striped) td {
  background-color: #f3d6849c;
}
.ant-table-striped :deep(.table-striped) .ant-table-cell-row-hover {
    background-color: #f3d6849c;
}

</style>