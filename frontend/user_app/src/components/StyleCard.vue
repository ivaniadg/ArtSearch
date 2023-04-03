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
        <div class="row q-px-md">
          <div class="col-8">
            <q-chip v-for="(style, index) in detectedStyles" v-model="style.bool" :key="index" removable color="primary" text-color="white">
              {{style.artstyle}}
            </q-chip>
            </div>
         <q-select class="col-4" outlined v-model="this.selected" :options="allArtstyles" label="Add more artstyles" @update:model-value="addChip" />
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
    const allArtstyles = ref([
      "Modernism",
      "Cubism",
      "Impressionism",
      "Expressionism",
      "Surrealism",
      "Abstract Expressionism",
    ]);
    const detectedStyles = ref([
      {
        artstyle: "Modernism",
        bool: true,
      },
     {
        artstyle: "Cubism",
        bool: true,
      },
      {
        artstyle: "Impressionism",
        bool: true,
      },
      {
        artstyle: "Expressionism",
        bool: true,
      },
    ]);
      return {
      pose,
      detectedStyles,
      selected: ref(null),
      allArtstyles,
     };
  },
  methods: {
    updateValue(axis) {
      this.pose.value = axis.value;
    },
    addChip(artstyle) {
      console.log(artstyle)
      this.detectedStyles.push({
        artstyle: artstyle,
        bool: true,
      });
      this.selected = null;
    },
  },
});
</script>
