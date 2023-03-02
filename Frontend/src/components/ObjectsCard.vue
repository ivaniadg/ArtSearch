<template>
  <q-card class="" style="height">
    <q-card-section class="q-pb-none">
      <div class="text-h6 text-center">Objects</div>
      <space />
    </q-card-section>
    <q-card-section class="q-pt-none">
      <Slider :axis="pose" @update:value="updateValue"></Slider>
      <div class="row">
        <q-checkbox
          class="col-4"
          v-for="(object, index) in objects"
          :key="index"
          :label="object.label"
          v-model="object.bool"
        />
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, ref } from "vue";
import Slider from "../components/Slider.vue";

export default defineComponent({
  components: { Slider },
  name: "ObjectsCard",
  props: {
    objects: {
      required: true,
    },
  },
  setup() {
    const pose = ref({
      name: "",
      value: 0.5,
    });
    return {
      pose,
    };
  },
  methods: {
    updateValue(axis) {
      this.pose.value = axis.value;
    },
  },
});
</script>
