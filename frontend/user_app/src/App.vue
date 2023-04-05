<template>
     User ID: {{userID}}

  <router-view />
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App',
  setup(){
    const userID = localStorage.getItem("userID");
    return {userID}
  }
})
</script>
