<template>
  <q-card class="" style="height">
    <q-card-section class="q-pb-none">
        <div class="text-h6 text-center">Pose</div>
        <space/>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <Slider
          :axis="pose"
          @update:value="updateValue"
        ></Slider>
        <div class="row">
          <q-checkbox class="col-4" v-for="(person, index) in persons" :key="index" :label="person.name" v-model="person.bool" keep-color :color="index" />

        </div>
    </q-card-section>
  </q-card>
</template>

<style>
/* define colors */


</style>

<script>
import { defineComponent, ref } from "vue";
import Slider from "../components/Slider.vue";

export default defineComponent({
  components: { Slider },
  props: {
    persons: {
      type: Object,
      required: true,
    },
    weight: {
      type: Number,
      required: true}
  },
  name: "PoseCard",
  setup() {
    const pose = ref({
      name: "",
      value: 0.5,
    });
    const colors = []

      return {
      pose,
      colors
    };
  },
  methods: {
    updateValue(axis) {
      this.$emit("update:value", { value: axis.value });
      this.pose.value = axis.value;
    },
  },
});
</script>
