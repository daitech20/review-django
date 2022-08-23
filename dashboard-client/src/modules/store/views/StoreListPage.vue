<template>
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240)"
    title="Store"
    sub-title="This is a subtitle of stores page" />
    <a-layout-content style="padding: 0 50px">
        <a-button class="editable-add-btn" style="margin-bottom: 8px" @click="handleAdd">Add</a-button>
        <a-table :columns="columns" :data-source="data">
            <template #bodyCell="{ column, record }">
              <template v-if="column.dataIndex === 'name'">
                  <a>{{ record.name }}</a>
              </template>
              <template v-else-if="column.key === 'action'">
                <span>
                  <router-link :to="{ name: 'store.detail', params: { store_slug: record.slug }}" >
                    <a-button type="primary" size="small">Edit</a-button>
                  </router-link>    
                </span>
                <span>
                    <a-button type="primary" danger size="small" @click="showModalDelete(record.name, record.slug)">Delete</a-button>
                </span>
              </template>
            </template>
        </a-table>
        <a-modal v-model:visible="visible" title="Delete" @ok="handleDelete()">
          <p>
            Do you want to delete {{name_store_del}}?
          </p>
        </a-modal>
    </a-layout-content>
</template>

<script lang="ts">
import BaseRequest from '@/core/BaseRequest'
import { notification } from 'ant-design-vue';


export default({
  data() {
    return {
        // data: [{ message: 'Foo' }, { message: 'Bar' }],
        columns: [],
        store: [],
        errors: {

        },
        data: [],
        colums: [],
        visible: false,
        name_store_del: '',
        slug_store_del: '',
    }
  },

  mounted() {
    this.getData()
  },

  methods: {
    getData: function() {
      this.columns = [
          {
            title: 'Name Store',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: 'Title',
            dataIndex: 'title',
            key: 'title',
          },
          {
            title: 'Domain',
            dataIndex: 'domain',
            key: 'domain',
            ellipsis: true,
          },
          {
            title: 'Website',
            dataIndex: 'website',
            key: 'website',
            ellipsis: true,
          },
          {
            title: 'Action',
            dataIndex: 'action',
            key: 'action',
          },
        ];

      

      BaseRequest.get('store/')
        .then(response => {
            this.data = []
            this.store = response.data;
            for (const key in this.store) {
              this.data.push({
                key: key,
                name: this.store[key].store_name,
                title: this.store[key].title,
                domain: this.store[key].domain,
                website: this.store[key].website,
                slug: this.store[key].store_slug
              })
            }
        })
        .catch(error=> {
            this.errors = error.response.data
        });
    },
    handleAdd: function() {
      this.$router.push({ name: 'store.create'});
    },

    showModalDelete: function(name: any, slug: any) {
      this.name_store_del = name
      this.slug_store_del = slug
      this.visible = true
    },

    handleDelete: function() {
      this.visible = false
      BaseRequest.delete('store/update/' + this.slug_store_del)
            .then(response => {
                this.errors = {}
                this.delSuccessNotification()
                for (let key=0; key<this.data.length; key++) {
                  if (this.data[key].slug === this.slug_store_del) {
                    this.data.splice(key, 1)
                    break
                  }
                }
              }
          )
          .catch(error=> {
              this.errors = error.response.data
              console.log(this.errors)
          });
    },

    delSuccessNotification: function() {
        notification['success']({
            message: 'Delete successfully!',
            description:
            'Store was deleted! ',
        });
    }
  }
});
</script>