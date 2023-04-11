<template>
  <q-layout view="lHh Lpr lFf">
       <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const menuList = [
  {
    icon: 'star',
    label: 'Favourites',
    separator: false
  },
  {
    icon: 'history',
    label: 'History',
    separator: true
  },
  {
    icon: 'settings',
    label: 'Settings',
    separator: false
  },
  {
    icon: 'logout',
    label: 'Logout',
    separator: true
  }]

export default defineComponent({
  name: 'MainLayout',

  components: {
  },

  setup () {

    return {
      drawer: ref(false),
      menuList
    }
  }
})
</script>
