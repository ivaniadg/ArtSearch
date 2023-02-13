<template>
  <q-page>
    <div class="row q-pa-lg">
      <div class="col-md-10 col-xs-0"><h2 class="q-my-none">results</h2></div>
      <q-select
        class="col-md-2 col-xs-12"
        outlined
        v-model="selected"
        :options="options"
        label="Sort by"
      />
    </div>

    <q-list bordered class="rounded-borders">
      <q-expansion-item label="Picasso" default-opened>
        <template v-slot:header>
          <q-item-section>
            <div class="row justify-center">
              <h5 class="q-my-none">Monet</h5>
            </div>
          </q-item-section>
        </template>

        <div class="row q-gutter-sm q-ma-sm justify-center">
          <q-card
            v-for="(painting, i) in paintings"
            :key="i"
            @click="openDialog(painting)"
            class="image-card"
          >
            <img :src="painting" fit style="height: 140px" />
          </q-card>
        </div>
      </q-expansion-item>
      <q-separator />
    </q-list>
    <q-dialog v-model="dialogOpen">
      <q-card style="width: 900px; max-width: 80vw">
        <q-card-section class="row">
          <img
            :src="dialogImage"
            class="col-5 dialog-img"
          />
          <div class="col-7 q-pa-md">
            <div class="row">
              <div class="text-h2">Title</div>
              <q-space />
              <q-btn icon="close" flat round v-close-popup />
            </div>
            <div class="row q-pa-xs text-h5">By Artist</div>
            <div class="column justify-center" style="height: 60%">
              <div class="text-overline">Pose</div>
              <q-linear-progress :value="poseMatch" class="q-my-xs" />

              <div class="text-overline">Color</div>
              <q-linear-progress :value="colorMatch" class="q-my-xs" />

              <div class="text-overline">Style</div>
              <q-linear-progress :value="styleMatch" class="q-my-xs" />

              <div class="text-overline">Objects</div>
              <q-linear-progress :value="objectMatch" class="q-my-xs" />
            </div>
            <div class="row justify-center">
              <q-btn color="primary" label="search this image" />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped>
.image-card:hover {
  /* highlight the hovered item */
  cursor: pointer;
  opacity: 0.5;
}
.dialog-img {
  /* rounded edges */
  border-radius: 10px;
}
</style>

<script>
import { defineComponent, ref } from "vue";
export default defineComponent({
  name: "IndexPage",
  setup() {
    const paintings = [];

    for (let i = 0; i < 30; i++) {
      const random1 = Math.floor(Math.random() * 300) + 50;
      const random2 = Math.floor(Math.random() * 100) + 50;
      //push random image to paintings array
      paintings.push("https://picsum.photos/" + random1 + "/" + random2 + "");
    }
    const selected = ref("Artist");
    const options = ["Artist", "Artstyle", "Date", "Relevance"];
    const dialogImage = ref(null);
    const dialogOpen = ref(false);
    const poseMatch = ref(0.7);
    const colorMatch = ref(0.3);
    const styleMatch = ref(0.5);
    const objectMatch = ref(0.1);
    return { paintings, options, selected, dialogImage, dialogOpen, poseMatch, colorMatch, styleMatch, objectMatch };
  },
  methods: {
    openDialog(image) {
      this.dialogImage = image;
      this.dialogOpen = true;
    },
    closeDialog() {
      this.dialogOpen = false;
    },
  },
});
</script>
