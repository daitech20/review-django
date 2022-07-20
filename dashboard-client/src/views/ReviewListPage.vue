<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Reviews"
    sub-title="This is a reviews of store " />
    <a-layout-content style="padding: 0 50px">
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

<script lang="ts">
import { defineComponent } from 'vue';
import BaseRequest from '../core/BaseRequest.js'
import { notification } from 'ant-design-vue';


export default({
  data() {
    return {
        // data: [{ message: 'Foo' }, { message: 'Bar' }],
        columns: [],
        review: [],
        errors: {

        },
        data: [],
        colums: [],
        visible: false
    }
  },

  mounted() {
    this.getData()
  },

  updated() {
    this.getData()
  },

  methods: {
    getData: function() {
      this.columns = [
          {
            title: 'Name Customer',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: 'Phone Number',
            dataIndex: 'phone',
            key: 'phone',
          },
          {
            title: 'Review Score',
            dataIndex: 'score',
            key: 'score',
          },
          {
            title: 'Review Content',
            dataIndex: 'content',
            key: 'content',
            ellipsis: true,
          },
          {
            title: 'Email',
            dataIndex: 'email',
            key: 'email',
            ellipsis: true,
          },
          {
            title: 'Created',
            dataIndex: 'created',
            key: 'created',
            ellipsis: true,
          },
        ];

      
      BaseRequest.get('review/' + this.$route.params.store_slug)
        .then(response => {
            this.review = response.data;
            this.data = []
            for (const key in this.review) {
              this.data.push({
                name: this.review[key].customer_name,
                phone: this.review[key].phone_number,
                score: this.review[key].review_score,
                content: this.review[key].review_content,
                email: this.review[key].review_email,
                created: this.review[key].created_at
              })
            }
        })
        .catch(error=> {
            this.errors = error.response.data
        });
    },
    // handleAdd: function() {
    //   this.$router.push({ name: 'store.create'});
    // },

    // showModalDelete: function(name: any, slug: any) {
    //   this.name_store_del = name
    //   this.slug_store_del = slug
    //   this.visible = true
    // },

    // handleDelete: function() {
    //   this.visible = false
    //   BaseRequest.delete('store/update/' + this.slug_store_del)
    //         .then(response => {
    //             this.errors = {}
    //             this.delSuccessNotification()
    //             for (let key=0; key<this.data.length; key++) {
    //               if (this.data[key].slug === this.slug_store_del) {
    //                 this.data.splice(key, 1)
    //                 break
    //               }
    //             }
    //           }
    //       )
    //       .catch(error=> {
    //           this.errors = error.response.data
    //           console.log(this.errors)
    //       });
    // },

    // delSuccessNotification: function() {
    //     notification['success']({
    //         message: 'Delete successfully!',
    //         description:
    //         'Store was deleted! ',
    //     });
    // }
  }
});
</script>