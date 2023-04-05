<template>
  <q-page class="flex flex-center" v-show="isProcessing">
    <q-spinner class="items-center" color="primary" size="3em" />
  </q-page>
  <q-page>
    <q-form @submit="onSubmit" v-show="!isProcessing">
      <div class="row q-gutter-lg">
        <div class="col-md-5 col-sm-12 q-gutter-lg">
          <q-card class="image-card">
            <q-img
              :src="'data:image/png;base64, ' + image"
              spinner-color="white"
            />
          </q-card>

          <div class="items-center">
            <q-btn
              class="q-mx-lg"
              label="Search"
              type="submit"
              color="primary"
            /><q-btn
              class="q-mx-lg"
              label="Back"
              size="sm"
              color="secondary"
              @click="this.userLogger.addAction({'name': 'Back to index page'})"
              :to="{ name: 'Index' }"
            />
          </div>
        </div>
        <div class="col-md-5 col-sm-12 q-gutter-lg">
          <PoseCard
            :persons="analyzed_pose.persons"
            :userLogger="userLogger"
            :weight="0.1"
            @update:value="updatePoseValue"
          />
          <ColorCard
            :colors="analyzed_colors"
            :userLogger="userLogger"
            @update:value="updateColorValue"
          />
          <ObjectsCard
            :objects="analyzed_objects"
            :userLogger="userLogger"
            @update:value="updateObjectsValue"
          />
        </div>
      </div>
    </q-form>
  </q-page>
</template>

<script>
import axios from "axios";
import PoseCard from "../components/PoseCard.vue";
import ColorCard from "../components/ColorCard.vue";
import StyleCard from "../components/StyleCard.vue";
import ObjectsCard from "../components/ObjectsCard.vue";
import { ref } from "vue";
import UserLogger from "../UserLogger";

export default {
  components: { PoseCard, ColorCard, ObjectsCard },
  data() {
    const analytics_server = process.env.ANALYTICS_SERVER;
    const userID = localStorage.getItem("userID");
    var userLogger = new UserLogger(analytics_server,
        10, 20, 'data', {'userID': userID,
            'page': 'AdvancedSettings',
            'condition': 'sliders+advancedoptions'})

    const analyzed_pose = history.state.advancedSettings.pose;
    const analyzed_colors = history.state.advancedSettings.colors;
    // const analyzed_style = history.state.advancedSettings.style;
    const analyzed_objects = history.state.advancedSettings.objects;
    const image = analyzed_pose.image;
    const axes = {
      pose: {
        value: 0.5,
      },
      color: {
        value: 0.5,
      },
      style: {
        value: 0.5,
      },
      objects: {
        value: 0.5,
      },
    };
    return {
      analyzed_pose,
      analyzed_colors,
      // analyzed_style,
      analyzed_objects,
      image,
      axes,
      isProcessing: ref(false),
      userLogger,
    };
  },

  methods: {
    onSubmit() {
      const formData = new FormData();
      formData.append("image", history.state.image);
      formData.append("pose_weight", this.axes.pose.value);
      formData.append("color_weight", this.axes.color.value);
      formData.append("style_weight", this.axes.style.value);
      formData.append("object_weight", this.axes.objects.value);

      formData.append("poses", JSON.stringify(this.analyzed_pose.persons));
      formData.append("colors", JSON.stringify(this.analyzed_colors));
      // formData.append("style", JSON.stringify(this.analyzed_style));
      formData.append("objects", JSON.stringify(this.analyzed_objects));

      this.userLogger.addAction({'name': 'search',
          'pose_weight': this.axes.pose.value,
          'color_weight': this.axes.color.value,
          'style_weight': this.axes.style.value,
          'object_weight': this.axes.objects.value})
      this.isProcessing = true;
      const backend_server = process.env.BACKEND_SERVER;
      axios
        .post(backend_server+"/advancedSearchQuery", formData)
        .then((response) => {
          // handle successful response
          this.isProcessing = false;
          //redirect to results page
          this.$router.push({
            name: "Results",
            state: {
              image: this.picture,
              results: response.data,
            },
          });
        })
        .catch((error) => {
          // handle error
          this.isProcessing = false;
          this.$q.notify({
            message: "Error: " + error,
            color: "negative",
            position: "top",
            timeout: 2000,
          });
        });
    },
    updatePoseValue(axis) {
      this.axes.pose.value = axis.value;
    },
    updateColorValue(axis) {
      this.axes.color.value = axis.value;
    },
    updateStyleValue(axis) {
      this.axes.style.value = axis.value;
    },
    updateObjectsValue(axis) {
      this.axes.objects.value = axis.value;
    },
  },
};
</script>

<style>
.image-card {
  /* max-width: 600px; */
}
.year-card {
  /* width: 100%; */
  height: 25%;
}
.pose-card {
  height: 25%;
}
</style>
