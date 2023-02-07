<template>
  <q-card class="" style="height">
    <q-card-section class="q-pb-none">
        <div class="text-h6 text-center">Style</div>
        <space/>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <Slider
          :axis="pose"
          @update:value="updateValue"
        ></Slider>
        <div class="row">



          <q-chip v-for="(style, index) in detectedStyles" :key="index" removable color="primary" text-color="white">
          {{style}}
         </q-chip>

        </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, ref } from "vue";
import Slider from "../components/Slider.vue";

export default defineComponent({
  components: { Slider },
  name: "StyleCard",
  setup() {
    const pose = ref({
      name: "",
      value: 0.5,
    });
    const detectedStyles = ref(["modernism", "cubsim"])
      return {
      pose,
      detectedStyles
     };
  },
  methods: {
    updateValue(axis) {
      this.pose.value = axis.value;
    },
  },
});
</script>
