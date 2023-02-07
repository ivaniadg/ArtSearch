<template>
  <q-layout view="lHh Lpr lFf">
    <!-- <q-btn
          round
          icon="menu"
          aria-label="Menu"
          @click="drawer = !drawer"
        /> -->

    <q-drawer
        v-model="drawer"
        show-if-above
        :width="200"
        :breakpoint="500"
        bordered
        class="bg-grey-2"
      >
        <q-scroll-area class="fit">
          <q-list>

            <template v-for="(menuItem, index) in menuList" :key="index">
              <q-item clickable v-ripple>
                <q-item-section avatar>
                  <q-icon :name="menuItem.icon" />
                </q-item-section>
                <q-item-section>
                  {{ menuItem.label }}
                </q-item-section>
              </q-item>
              <q-separator :key="'sep' + index"  v-if="menuItem.separator" />
            </template>

          </q-list>
        </q-scroll-area>
      </q-drawer>

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
