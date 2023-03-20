<template>
  <q-page class="row">
    <div class="col-3">
      <img
        :src="queryImage"
        class="q-pa-lg"
        style="width: 100%"
        @click="enlargeImageDialog"
      />

      <div class="flex">
        <q-btn
          color="primary"
          class="q-mb-lg"
          label="New search"
          :to="{ name: 'Index' }"
        />
      </div>
      <q-separator inset />

      <h4 class="q-my-lg text-center">analysis</h4>
      <div class="q-pa-lg" style="width: 100%">
        <q-img
          :src="'data:image/png;base64, ' + resultImage"
          class="clickable"
          @click="enlargeImageDialog()"
        >
          <q-icon
            class="absolute all-pointer-events"
            size="50px"
            name="zoom_in"
            color="white"
            style="top: 10px; left: 10px"
          />
        </q-img>
      </div>
      <div class="text-subtitle1 text-center">Extracted colors</div>
      <div class="row q-mx-md">
        <div
          class="col-4"
          style="display: flex; align-items: center"
          v-for="(color, index) in queryColors"
          v-bind:key="index"
        >
          <div
            class="box q-ma-sm"
            :style="{
              backgroundColor:
                'rgb(' + color[0] + ',' + color[1] + ',' + color[2] + ')',
            }"
          ></div>
          <div class="text-weight-bold" style="font-size: 10px">
            ({{ color[0] }}, {{ color[1] }}, {{ color[2] }})
          </div>
        </div>
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
      <div class="row q-gutter-sm q-ma-sm justify-left">
        <q-card
          v-for="(result, i) in results"
          :key="i"
          @click="openDialog(result)"
          class="image-card"
        >
          <img
            :src="
              'https://stthesis.blob.core.windows.net/assets/assets/' +
              result.image_name
            "
            fit
            style="height: 140px"
          />
        </q-card>
      </div>
      <q-dialog v-model="dialogOpen">
        <q-card style="width: 1200px; max-width: 110vw">
          <q-card-section class="row">
            <div class="col-6">
              <q-img
                class="dialog-img"
                :src="dialogImage"
                width="100%"
                v-show="!showAnalysis"
              >
                <q-icon
                  class="absolute all-pointer-events clickable"
                  size="50px"
                  name="psychology_alt"
                  color="white"
                  style="top: 10px; left: 10px"
                  @click="showDetails()"
                >
                  <q-tooltip>
                    Click this icon to reveal the details of the analysis
                  </q-tooltip></q-icon
                >
              </q-img>

              <q-img
                class="dialog-img"
                :src="analysisImage"
                width="100%"
                v-show="showAnalysis"
              >
                <q-icon
                  class="absolute all-pointer-events clickable"
                  size="50px"
                  name="arrow_back"
                  color="white"
                  style="top: 10px; left: 10px"
                  @click="showNormal()"
                >
                  <q-tooltip>
                    Click this icon to go back
                  </q-tooltip></q-icon
                >
              </q-img>
            </div>

            <div class="col-6 q-pa-md">
              <div class="row">
                <div class="text-h2">{{ title }}</div>
                <q-space />
                <q-btn icon="close" flat round v-close-popup />
              </div>
              <div class="row q-pa-xs text-h5">By {{ artist }}</div>
              <div class="column justify-center" style="height: 60%">
                <div class="text-overline">Pose</div>
                <q-linear-progress :value="poseMatch" class="q-my-xs" />

                <div class="text-overline">Color</div>
                <q-linear-progress :value="colorMatch" class="q-my-xs" />

                <!-- <div class="text-overline">Style</div>
                <q-linear-progress :value="styleMatch" class="q-my-xs" /> -->

                <div class="text-overline">Objects</div>
                <q-linear-progress :value="objectMatch" class="q-my-xs" />
              </div>
              <!-- <div class="row justify-center">
                <q-btn color="primary" label="search this image" />
              </div> -->
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
    </div>
    <q-dialog v-model="enlargeImage">
      <img
        :src="'data:image/png;base64, ' + resultImage"
        style="width: 70rem"
      />
    </q-dialog>
  </q-page>
</template>

<style scoped>
.clickable {
  cursor: pointer;
}
.clickable:hover {
  opacity: 0.5;
}
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

export default defineComponent({
  name: "IndexPage",
  setup() {
    const queryImage = localStorage.getItem("queryImage");

    const result = history.state.results;
    const results = result.results;
    const resultImage = result.queryImage.result_image;
    const queryColors = result.queryImage.colorpalette;

    const selected = ref("Artist");
    const options = ["Artist", "Artstyle", "Date", "Relevance"];
    const dialogImage = ref(null);
    const poseMatch = ref(0.0);
    const colorMatch = ref(0.0);
    const styleMatch = ref(0.0);
    const objectMatch = ref(0.0);
    const dialogOpen = ref(false);
    const enlargeImage = ref(false);
    const showAnalysis = ref(false);
    const title = ref("Title");
    const artist = ref("Artist");
    return {
      options,
      selected,
      dialogImage,
      dialogOpen,
      results,
      poseMatch,
      colorMatch,
      styleMatch,
      objectMatch,
      queryImage,
      resultImage,
      queryColors,
      enlargeImage,
      showAnalysis,
      title,
      artist,
    };
  },
  methods: {
    openDialog(result) {
      this.dialogImage =
        "https://stthesis.blob.core.windows.net/assets/assets/" +
        result.image_name;
      this.colorMatch = result.color_score;
      this.poseMatch = result.pose_score;
      this.styleMatch = result.style_score;
      this.objectMatch = result.object_score;
      this.title = result.metadata.title;
      this.artist = result.metadata.artist;
      this.dialogOpen = true;
      this.showAnalysis = false;
      this.analysisImage =
      "https://stthesis.blob.core.windows.net/assets/analysis/" +
      result.image_name;
    },
    closeDialog() {
      this.dialogOpen = false;
    },
    enlargeImageDialog() {
      this.enlargeImage = true;
    },
    closeImageDialog() {
      this.enlargeImage = false;
    },
    showDetails() {
      this.showAnalysis = true;
    },
    showNormal() {
      this.showAnalysis = false;
    },
  },
});
</script>
