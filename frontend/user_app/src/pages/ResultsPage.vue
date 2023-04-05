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
          @click="userLogger.addAction({ name: 'New search' })"
        />
      </div>
      <q-separator inset />
      <div v-show="stage==1">
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

    </div>
    <div class="col-9">
      <div class="row q-pa-lg">
        <div class="col-md-7 col-xs-0"><h2 class="q-my-none">results</h2></div>
        <q-toggle v-model="selectionMode" label="selection mode" v-show="!sent_top10"/>
        <q-btn class="q-ma-md" v-if="selectionMode" label="Submit top 10" color="primary" @click="submitTop10" :disabled="!complete"/>
        <q-btn class="q-ma-md" v-if="selectionMode" label="Reset top 10" color="primary" @click="resetTop10"/>
      </div>

      <div class="row q-gutter-sm q-ma-sm justify-left">
        <q-card
          v-for="(result) in results"
          :id="result.image_name"
          :key="result.image_name"
          @click="handleClick(result)"
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
          <div class="centered" v-show="selectionMode">{{ result.selected }}</div>
        </q-card>
      </div>
      <q-dialog v-model="dialogOpen" @hide="this.userLogger.addAction({'name': 'CloseDialog', 'image': this.title})">
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
                  v-show="stage == 1"
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
              <div class="column justify-center" style="height: 60%" v-show="stage==1">
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

.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 7em;
  color:red;
  text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
}
</style>

<script>
import { defineComponent, ref } from "vue";
import  UserLogger  from "../UserLogger";

export default defineComponent({
  name: "IndexPage",
  setup() {

    const analytics_server = process.env.ANALYTICS_SERVER;
    const userID = 1;

    var userLogger = new UserLogger( analytics_server ,
        10, 20, 'data', {'user': userID,
            'page': 'AdvancedSettings',
            'condition': 'sliders+advancedoptions'});

    const queryImage = localStorage.getItem("queryImage");

    const result = history.state.results;
    const results = ref(result.results);
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
    const stage = ref(0); // 0: before selecting top 10, 1: after selecting top 10
    const s0_top10 = ref([]);
    const s1_top10 = ref([]);
    const counter = ref(1);
    const selectionMode = ref(false);
    const complete = ref(false);
    const sent_top10 = ref(false);
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
      userLogger,
      stage,
      s0_top10,
      s1_top10,
      selectionMode,
      counter,
      complete,
      sent_top10,
      userID,
      analytics_server
    };
  },
  methods: {
    submitTop10(){
      // SUBMIT TOP 10 together with the user's data
      if (this.stage==0 && this.s0_top10.length == 10) {
        this.complete = false;
        this.stage = 1;
        this.selectionMode = false;
        this.counter = 1
        this.results.forEach((result) => {
        result["selected"] = "";
        });
      }
      if (this.stage==1 && this.s1_top10.length == 10) {
        this.complete = false;
        this.selectionMode = false;
        this.send_top10()
        this.counter = 1
        this.results.forEach((result) => {
        result["selected"] = "";
        });
      }
    },
    send_top10(){
      const top10 = {
        userID: this.userID,
        s0 : this.s0_top10,
        s1 : this.s1_top10
      }
      fetch(this.analytics_server+'/top10', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify(top10),
        })
            .then(response => {
                if (response.status == 200) {
                    console.log("")
                    this.sent_top10 = true;
                }
            })
            .catch(err => {
                console.log(err)
            })
    },
    resetTop10(){
      this.counter = 1;
      if (this.stage == 0) {
        this.s0_top10 = [];
      }
      if (this.stage == 1) {
        this.s1_top10 = [];
      }
      this.results.forEach((result) => {
        result["selected"] = "";
      });
    },
    handleClick(result) {
      if (this.selectionMode) {
        if (this.stage == 0 && !this.s0_top10.some(obj => obj.image_name === result.image_name) && this.counter <= 10) {
          this.s0_top10.push({"image_name":result.image_name, "personal_rank": this.counter, "real_rank": this.results.indexOf(result)+1});
          console.log("select")
          result["selected"] = this.counter;
          this.counter++;
          if (this.counter == 11) {
            this.complete = true;
          }
        }
        if (this.stage == 1 &&  !this.s1_top10.some(obj => obj.image_name === result.image_name) && this.counter <= 10) {
          this.s1_top10.push({"image_name":result.image_name, "personal_rank": this.counter, "real_rank": this.results.indexOf(result)+1});
          result["selected"] = this.counter;
          this.counter++;
          if (this.counter == 11) {
            this.complete = true;
          }
        }
      } else {
        this.openDialog(result);
      }
    },
    openDialog(result) {
      this.userLogger.addAction({'name': 'openDialog', 'image': result.metadata.title})
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
      this.userLogger.addAction({'name': 'enlargeAnalysisImage'})
      this.enlargeImage = true;
    },
    closeImageDialog() {
      this.userLogger.addAction({'name': 'closeAnalysisImage', 'image': this.title})
      this.enlargeImage = false;
    },
    showDetails() {
      this.userLogger.addAction({'name': 'switchToDetails', 'image': this.title})
      this.showAnalysis = true;
    },
    showNormal() {
      this.userLogger.addAction({'name': 'switchToNormal', 'image': this.title})
      this.showAnalysis = false;
    },
  },
});
</script>
