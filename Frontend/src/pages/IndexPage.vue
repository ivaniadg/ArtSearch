<template>
  <q-page class="flex flex-center">
    <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-gutter-md"
      style="width: 500px"
    >
      <q-file
        filled
        v-model="picture"
        label="Click to upload image"
        hint="Image must be in .jpg or .png format"
        accept="image/*"
      />

      <!-- <q-uploader
        bordered
        style="width: 100%; height: 300px"
        hide-upload-btn=True
      /> -->

      <q-list dense>
        <Slider
          v-for="(axis, index) in axes"
          :key="index"
          :axis="axis"
          @update:value="updateValue"
        ></Slider>
      </q-list>
      <div class="center-button">
        <q-btn
          class="q-mx-lg"
          label="Search"
          type="submit"
          color="primary"
          :to="{ name: 'Results' }"
        /><q-btn
          class="q-mx-lg"
          label="Advanced Options"
          size="sm"
          color="secondary"
          :to="{ name: 'AdvancedSettings' }"
        />
      </div>
    </q-form>
  </q-page>
</template>

<style>
.center-button {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

</style>

<script>
import { defineComponent, ref } from "vue";
import Slider from "../components/Slider.vue";

export default defineComponent({
  components: { Slider },
  name: "IndexPage",
  setup() {
    const axes = ref({
      pose: {
        name: "Pose",
        value: 0.5,
      },
      color: {
        name: "Color",
        value: 0.5,
      },
      style: {
        name: "Style",
        value: 0.5,
      },
      objects: {
        name: "Objects",
        value: 0.5,
      },
    });
    return { axes, picture: ref(null) };
  },
  methods: {
    updateValue(axis) {
      this.axes[axis.name.toLowerCase()].value = axis.value;
    },
  },
});
</script>
