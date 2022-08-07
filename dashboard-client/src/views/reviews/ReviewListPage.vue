<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Reviews"
    sub-title="This is a reviews of store " />
    <a-layout-content style="padding: 0 50px">
    <a-cascader v-model:value="value" :options="options" placeholder="Please select" :allowClear="false" />
        <a-table :columns="columns" :data-source="data">
            <template #bodyCell="{ column, record }">
              <template v-if="column.dataIndex === 'name'">
                  <a>{{ record.name }}</a>
              </template>
              <template v-if="column.dataIndex === 'score'">
                  <a-icon v-for="key in record.score" :key="key" name="StarOutlined" :style="{color: 'yellow'}" fill="currentColor"></a-icon>
              </template>
            </template>
        </a-table>
    </a-layout-content>
</template>

<script>
import BaseRequest from '@/core/BaseRequest.js'
import { authStore } from '@/store/auth.store';
import { mapState } from 'pinia'

export default({
	data() {
		return {
			options: [],
			value: [],
			columns: [],
			reviews: [],
			store: [],
			errors: {

			},
			data: [],
			visible: false,
		}
	},

	mounted() {
		this.getData()
	},

	watch: {
		value: function() {
		this.getReview()
		}
	},

	computed: {
		...mapState(authStore, ['isLoggedIn', 'user'])
	},

	methods: {
		getData: function() {
			this.columns = [
				{
				title: 'Name Customer',
				dataIndex: 'name',
				key: 'name'
				},
				{
				title: 'Phone Number',
				dataIndex: 'phone',
				key: 'phone'
				},
				{
				title: 'Review Score',
				dataIndex: 'score',
				key: 'score'
				},
				{
				title: 'Review Content',
				dataIndex: 'content',
				key: 'content'
				},
				{
				title: 'Email',
				dataIndex: 'email',
				key: 'email'
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

				BaseRequest.get('review/' + this.store[0].store_slug)
				.then(response => {
					this.reviews = response.data;
					this.data = []
					for (const num in this.reviews) {
						this.data.push({
						name: this.reviews[num].customer_name,
						phone: this.reviews[num].phone_number,
						score: this.reviews[num].review_score,
						content: this.reviews[num].review_content,
						email: this.reviews[num].review_email,
						created: this.reviews[num].created_at
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

		getReview: function() {
			this.data = []
			BaseRequest.get('review/' + this.value[0])
			.then(response => {
				this.reviews = response.data
				for (const num in this.reviews) {
					this.data.push({
					name: this.reviews[num].customer_name,
						phone: this.reviews[num].phone_number,
						score: this.reviews[num].review_score,
						content: this.reviews[num].review_content,
						email: this.reviews[num].review_email,
						created: this.reviews[num].created_at
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