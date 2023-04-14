<template>
     User ID: {{userID}} <br>
     Version: {{appVersion}}

  <router-view />
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App',
  setup(){
    if (!localStorage.getItem("userID")){
        localStorage.setItem("userID", Math.random().toString(16).slice(2));
        console.log("user id does not exist, creating new one" + localStorage.getItem("userID"))
    }
    const userID = localStorage.getItem("userID");
    return {userID, appVersion: "3"}
  }
})
</script>
