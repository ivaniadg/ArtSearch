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
          <q-checkbox class="col-4" v-for="(person, index) in persons" :key="index" :label="person.name" v-model="person.bool" />

        </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, ref } from "vue";
import Slider from "../components/Slider.vue";

export default defineComponent({
  components: { Slider },
  name: "PoseCard",
  setup() {
    const pose = ref({
      name: "",
      value: 0.5,
    });
    const persons = ref({
      person1: {
        name: "person1",
        bool: true,
      },
      person2: {
        name: "person2",
        bool: true,
      },
      person3: {
        name: "person3",
        bool: true,
      },
      person4: {
        name: "person4",
        bool: true,
      }})
      return {
      pose,
      persons
     };
  },
  methods: {
    updateValue(axis) {
      this.pose.value = axis.value;
    },
  },
});
</script>
