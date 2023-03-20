<template>
  <q-page class="row">
    <div class="col-3">
      <img id="img" src="" class="q-pa-lg" style="width:100%"/>
      <div class="flex">
        <q-btn color="primary" label="New search" :to="{ name: 'Index' }" />
      </div>
    </div>
    <div class="col-9">
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

    <!-- <q-list bordered class="rounded-borders">
      <q-expansion-item label="Picasso" default-opened>
        <template v-slot:header>
          <q-item-section>
            <div class="row justify-left">
              <h5 class="q-my-none">Monet</h5>
            </div>
          </q-item-section>
        </template>


      </q-expansion-item>
      <q-separator />
    </q-list> -->
    {{ result }}
    <div class="row q-gutter-sm q-ma-sm justify-left">
          <q-card
            v-for="(result, i) in results"
            :key="i"
            @click="openDialog(result)"
            class="image-card"
          >
            <img :src="'https://stthesis.blob.core.windows.net/assets/assets/' + result.image_name" fit style="height: 140px" />
          </q-card>
        </div>
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
  </div>
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

.flex {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "IndexPage",
  setup() {
    const result = history.state.results;
    // const queryImage = history.state.image;
    // const reader = new FileReader();
    // reader.readAsDataURL(queryImage);
    // reader.onload = function(event) {
		// 	document.getElementById('img').src = event.target.result;
		// };

    const results = result.result;

    const selected = ref("Artist");
    const options = ["Artist", "Artstyle", "Date", "Relevance"];
    const dialogImage = ref(null);
    const poseMatch = ref(0.0);
    const colorMatch = ref(0.0);
    const styleMatch = ref(0.0);
    const objectMatch = ref(0.0);
    const dialogOpen = ref(false);
    return {options, selected, dialogImage, dialogOpen , results, poseMatch, colorMatch, styleMatch, objectMatch, result};
  },
  methods: {
    openDialog(result) {

      this.dialogImage = "https://stthesis.blob.core.windows.net/assets/assets/"+result.image_name;
      this.colorMatch = result.color_score;
      this.poseMatch = result.pose_score;
      this.styleMatch = result.style_score;
      this.objectMatch = result.object_score;
      this.dialogOpen = true;
    },
    closeDialog() {
      this.dialogOpen = false;
    },
  },
});
</script>
