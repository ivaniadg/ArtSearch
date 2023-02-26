<template>
  <q-card class="" style="height">
    <q-card-section class="q-pb-none">
      <div class="text-h6 text-center">Color</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <Slider :axis="pose" @update:value="updateValue"></Slider>
      <div class="row">
        <div
          class="col-4"
          style="display: flex; align-items: center"
          v-for="(color, index) in colors"
          v-bind:key="index"
        >
          <q-checkbox v-model="color.bool" />
          <div class="box" :style="{ backgroundColor: color.color }"></div>
        </div>
        <!-- <q-btn dense color="primary" icon="add" size="md"/> -->
      </div>
    </q-card-section>
  </q-card>
</template>

<style scoped>
.box {
  width: 35px;
  height: 35px;
  border-radius: 10px;
  justify-content: center;
  align-items: center;
}
</style>

<script>
import { defineComponent, ref } from "vue";
import Slider from "../components/Slider.vue";

export default defineComponent({
  components: { Slider },
  name: "ColorCard",
  setup() {
    const pose = ref({
      name: "",
      value: 0.5,
    });
    const colors = ref({
      color1: {
        color: "#7415",
        bool: true,
      },
      color2: {
        color: "#789615",
        bool: true,
      },
      color3: {
        color: "#654321",
        bool: true,
      },
      color4: {
        color: "#852369",
        bool: true,
      },
    });
    return {
      pose,
      colors,
      color: "red",
    };
  },
  methods: {
    updateValue(axis) {
      this.pose.value = axis.value;
    },
  },
});
</script>
