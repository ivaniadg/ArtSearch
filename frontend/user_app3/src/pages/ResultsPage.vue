<template>
  <q-page class="row">
    <div class="col-3">
      <h5 class="q-pa-xs q-ma-xs text-center">selected options</h5>
      <div class="q-px-lg">
      <div class="text-overline">Pose weight</div>
      <q-linear-progress :value="poseWeight" class="q-my-xs" />

      <div class="text-overline">Color weight</div>
      <q-linear-progress :value="colorWeight" class="q-my-xs" />

      <div class="text-overline">Objects weight</div>
      <q-linear-progress :value="objectWeight" class="q-my-xs" />
      </div>
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
    </div>
    <div class="col-9">
      <div class="row q-pa-lg">
        <div class="col-md-3"><h2 class="q-my-none">results</h2> </div>
        <div class="col-md-3 q-pa-md"><q-btn round color="primary" icon="info" @click="showInfo"/></div>
        <q-toggle v-model="selectionMode" label="selection mode" v-show="!sent_top10"/>
        <q-btn class="q-ma-md" v-if="selectionMode" :label="'Submit top ' + this.topX " color="primary" @click="submitTop10" :disabled="!complete"/>
        <q-btn class="q-ma-md" v-if="selectionMode" :label="'Reset top ' +  this.topX " color="primary" @click="resetTop10"/>
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
        <q-card style="width: 1200px; max-width: 90vw">
          <q-card-section >
            <div class="row">
              <q-space />
                <q-btn icon="close" flat round v-close-popup />
            </div>
            <div class="row">
              <div class="col-6 q-pa-lg">
              <div class="row q-pa-xs text-h5 row justify-center"> "{{ title }}" by {{ artist }}</div>
              <q-img
                class="dialog-img"
                :src="dialogImage"
                width="100%"
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
            <div class="col-6">

                <div class="text-h5 row justify-center">Your image</div>
              <div class="row q-py-lg">
                <q-img class="dialog-img" :src="queryImage" height="100%"/>
                </div>
            </div>
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

    <q-dialog v-model="info" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Instructions</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          You've now landed on the result page, here you will be asked to select your top {{ this.topX }} images that you think are the most similar to the query image considering your weights.
          <br><br>
          You can click on an image to enlarge it to inspect it more closely. To select images you can click on the togglebutton "selectionmode" in the top right corner of this page and click on an image to select it (in order).
          <br><br>
          When you're done selecting your top {{ this.topX }}, you can click on the "submit top {{ this.topX }}" button in the top right corner.
          <br><br>
          If there are duplicate images in the result set, you just pick the first one you see.
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="sent_top10" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Instructions</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
         You've now completed the task, if you want to do one more search with different weights (which is greatly appreciated), you can click here: <br>
         <q-btn
          color="primary"
          class="q-mb-lg"
          label="New search"
          :to="{ name: 'Index' }"
          @click="userLogger.addAction({ name: 'New search' })"
         /><br>

          If you want to proceed to the final questionnaire, you can click here (copy your userID: <b>{{ this.userID }}</b> ): <br>
          <q-btn
          color="primary"
          class="q-mb-lg"
          label="Questionnaire"
          href="https://forms.office.com/Pages/ResponsePage.aspx?id=m1hzOUCetU6ADrC2OD0WIUyTP6SV9olHtQpLK8rv5JpUQzUwM1FSS1U1RVVJQUlNWkc1NUtTMkIwVS4u"
          @click="userLogger.addAction({ name: 'To questionnaire' })"
         />

        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
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
    const userID = localStorage.getItem("userID");
    const analytics_server = process.env.ANALYTICS_SERVER;

    var userLogger = new UserLogger( analytics_server ,
        10, 20, 'data', {'user': userID,
            'page': 'AdvancedSettings',
            'version': '1'});

    const queryImage = localStorage.getItem("queryImage");

    const poseWeight = localStorage.getItem("PoseWeight");
    const colorWeight = localStorage.getItem("ColorWeight");
    const objectWeight = localStorage.getItem("ObjectWeight");

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
    const topXList = ref([]);
    const counter = ref(1);
    const selectionMode = ref(false);
    const complete = ref(false);
    const sent_top10 = ref(false);
    const info = ref(true);
    const selectedPalette = ref([]);
    const topX = 6;
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
      topXList,
      selectionMode,
      counter,
      complete,
      sent_top10,
      userID,
      analytics_server,
      info,
      selectedPalette,
      colorWeight,
      poseWeight,
      objectWeight,
      topX,
      timer: ref(0),
      timerInterval: null,
    };
  },
  mounted(){
    this.timerInterval = setInterval(() => {
      this.timer++;
    }, 1000)
  },
  methods: {
    showInfo(){
        this.info= true;
    },
    submitTop10(){
      // SUBMIT TOP 10 together with the user's data
      if (this.topXList.length == this.topX) {
        this.userLogger.addAction({'name': 'Submit Top 10'})
        this.complete = false;
        this.selectionMode = false;
        this.send_top10()
      }
    },
    send_top10(){
      const top10 = {
        secondsSpend: this.timer,
        userID: this.userID,
        topX : this.topXList,
        poseWeight: this.poseWeight,
        colorWeight: this.colorWeight,
        objectWeight: this.objectWeight,
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
                    this.sent_top10 = true;
                }
            })
            .catch(err => {
                console.log(err)
            })
    },
    resetTop10(){
      this.counter = 1;

      this.userLogger.addAction({'name': 'resetTopX'})
      this.topXList = [];

      this.results.forEach((result) => {
        result["selected"] = "";
      });
    },
    handleClick(result) {
      if (this.selectionMode) {
        if (!this.topXList.some(obj => obj.image_name === result.image_name) && this.counter <= this.topX) {
          this.userLogger.addAction({'name': 'addToTop10', 'image': result.image_name, 'rank': this.counter})
          this.topXList.push({"image_name":result.image_name, "personal_rank": this.counter, "real_rank": this.results.indexOf(result)+1});
          result["selected"] = this.counter;
          this.counter++;
          if (this.counter == this.topX+1) {
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
      this.selectedPalette = result.palette
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
