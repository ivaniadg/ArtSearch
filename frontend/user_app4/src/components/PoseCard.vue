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
          @change="value=>userLogger.addAction({'name': 'Change weight', 'Axis': 'Pose', 'Value':value })"
        />
        <div class="row">
          <q-checkbox class="col-4" v-for="(person, index) in persons" :key="index" :label="person.name" v-model="person.bool" keep-color
           :color="index" @update:model-value="userLogger.addAction({'name': 'Changed pose','person':person.name, 'value' : person.bool})"  />
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
      required: true},
    userLogger: {
      type: Object,
      required: true
    }
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
