<template>
  <div>
    <div class="text-center q-mt-lg">{{axis.name}}</div>
    <q-item class="q-pt-none">
      <q-item-section side>
        <q-icon name="priority_high" size="xs" />
      </q-item-section>
      <q-item-section>
        <q-slider @change="value => $emit('change', value)" v-model="val" :step="0" :min="0" :max="1" :markers="0.5" label :label-value="'Value: ' + roundedValue"  track-size="6px" thumb-color="grey"/>
      </q-item-section>
      <q-item-section side>
        <q-icon name="priority_high" size="lg" />
      </q-item-section>
    </q-item>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "MySlider",
  props: {
    axis : {
      type: Object,
      required: true,
    },
  },
  computed: {
    val: {
      get() {
        return this.axis.value;
      },
      set(NewValue) {
        this.$emit("update:value", { name: this.axis.name, value: NewValue });
      },
    },
    roundedValue() {
      return Math.round(this.axis.value * 100) / 100;
    },
  },
  }
);
</script>
