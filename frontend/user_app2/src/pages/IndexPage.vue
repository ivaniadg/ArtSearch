<template>
  <q-page class="flex flex-center">
    <q-spinner color="primary" size="3em" v-show="isProcessing" />
    <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-gutter-md q-pb-lg"
      style="width: 500px"
      v-show="!isProcessing"
    >
    <div style="text-align: center;vertical-align: middle;">Select a precalculated image (faster) or upload your own image. (slower)</div>
    <q-scroll-area
      :thumb-style="thumbStyle"
      :bar-style="barStyle"
      style="height: 380px;"

    >
    <div class="row">
      <q-card v-for="(artwork, index) in artworks" :key="index" class="col-5 q-ma-md clickable" id="artwork" @click="selectImage(artwork)">
          <q-img :src="'artwork/' + artwork.name" :ratio="1" :style="[artwork.selected ? {'border': '4px solid rgb(224, 64, 55)'} : {'border': 'none'}]" />
      </q-card>
    </div>


    </q-scroll-area>
      <q-file
        filled
        v-model="picture"
        label="Click to upload image"
        hint="Image must be in .jpg or .png format"
        accept="image/*"
        @update:model-value="onInput"
              />
      <!-- display picture when uploaded -->
      <div v-if="picture">
        <q-img :src="queryImage" style="width: 100%" />
      </div>

      <q-list dense>
      </q-list>
      <div class="center-button">
        <q-btn
          id="submit"
          class="q-mx-lg"
          label="Search"
          type="submit"
          color="primary"
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

.clickable{
  cursor: pointer;
}

.selected{
  border: 4px solid rgb(224, 64, 55);
  border-radius: 10px;
}
</style>

<script>
import { defineComponent, ref } from "vue";
import axios from "axios";
import UserLogger from "../UserLogger";

export default defineComponent({
  name: "IndexPage",
  setup() {
    // Get all image names from assets/artwork
    const artwork = require.context("../../public/artwork", false, /\.(png|jpe?g|svg)$/);
    var artworks = artwork.keys().map((key) => key.match(/[^/]+$/)[0]);

    // give every artwork a bool selected
    artworks = ref(artworks.map((artwork) => {
      return {
        name: artwork,
        selected: false,
      };
    }));

    const userID = localStorage.getItem("userID");
    const analytics_server = process.env.ANALYTICS_SERVER;
    var userLogger = new UserLogger(analytics_server,
        10, 20, 'data', {'userID': userID,
            'page': 'index',
            'condition': 'No sliders + No advancedoptions'})
    const axes = ref({
      pose: {
        name: "Pose",
        value: 0.5,
      },
      color: {
        name: "Color",
        value: 0.5,
      },
      objects: {
        name: "Objects",
        value: 0.5,
      },
    });

    return { axes, picture: ref(null), isProcessing: ref(false), queryImage: ref(null), userLogger, artworks, custom: ref(false) };
  },
  methods: {
    selectImage(artwork) {
      this.artworks.forEach((artwork) => {
        artwork.selected = false;
      });
      artwork.selected = true;
      this.userLogger.addAction({'name': 'Select precalculated image', 'Image': artwork.name})
      this.custom = false;
    },
    updateValue(axis) {
      this.axes[axis.name.toLowerCase()].value = axis.value;
    },
    saveToLocalStorage() {
      const reader = new FileReader();
      reader.addEventListener(
        "load",
        function () {
          // convert image file to base64 string and save to localStorage
          localStorage.setItem("queryImage", reader.result);
        },
        false
      );
      reader.readAsDataURL(this.picture);
    },
    onInput() {
        const reader = new FileReader();
        reader.addEventListener(
          "load",
          function () {
            // convert image file to base64 string and save to localStorage
            this.queryImage = reader.result;
          }.bind(this),
          false
      );
      reader.readAsDataURL(this.picture);
      // log image upload
      this.userLogger.addAction({'name': 'Upload image', 'Image': this.picture.name})
      this.custom = true;
      // deselect precalculated images
      this.artworks.forEach((artwork) => {
        artwork.selected = false;
      });
    },
    sumitPrecalculated(){
      const formData = new FormData();
      formData.append("image_name", this.artworks.find((artwork) => artwork.selected).name);
      formData.append("pose_weight", this.axes.pose.value);
      formData.append("color_weight", this.axes.color.value);
      formData.append("object_weight", this.axes.objects.value);
      this.isProcessing = true;
      localStorage.setItem("queryImage", "artwork/"+this.artworks.find((artwork) => artwork.selected).name);
      const backend_server = process.env.BACKEND_SERVER;
      // log submission
      this.userLogger.addAction({'name': 'Submit search', 'Pose weight': this.axes.pose.value, 'Color weight': this.axes.color.value, 'Object weight': this.axes.objects.value})
      axios
        .post(backend_server+'/precalcsearch', formData)
        .then(response => {
          // handle successful response
          // log success
          this.userLogger.addAction({'name': 'Search success'})
          this.isProcessing = false;
          //redirect to results page
          this.$router.push({
            name: "Results",
            state: {
              image: this.picture,
              results: response.data
            },
          });
        })
        .catch(error => {
          // handle error
          this.isProcessing = false;
          this.$q.notify({
            message: "Error: " + error,
            color: "negative",
            position: "top",
            timeout: 2000,
          });
          // log error
          this.userLogger.addAction({'name': 'Search error', 'Error': error})
        });
    },
    submitCustomImage(){
      const formData = new FormData();
      formData.append("image", this.picture);
      formData.append("pose_weight", this.axes.pose.value);
      formData.append("color_weight", this.axes.color.value);
      // formData.append("style_weight", this.axes.style.value);
      formData.append("object_weight", this.axes.objects.value);
      this.isProcessing = true;
      this.saveToLocalStorage();
      const backend_server = process.env.BACKEND_SERVER;
      // log submission
      this.userLogger.addAction({'name': 'Submit search', 'Pose weight': this.axes.pose.value, 'Color weight': this.axes.color.value, 'Object weight': this.axes.objects.value})
      axios
        .post(backend_server+'/search', formData)
        .then(response => {
          // handle successful response
          // log success
          this.userLogger.addAction({'name': 'Search success'})
          this.isProcessing = false;
          //redirect to results page
          this.$router.push({
            name: "Results",
            state: {
              image: this.picture,
              results: response.data
            },
          });
        })
        .catch(error => {
          // handle error
          this.isProcessing = false;
          this.$q.notify({
            message: "Error: " + error,
            color: "negative",
            position: "top",
            timeout: 2000,
          });
          // log error
          this.userLogger.addAction({'name': 'Search error', 'Error': error})
        });
    },
    onSubmit() {
      if (this.custom) {
        this.submitCustomImage();
      } else {
        this.sumitPrecalculated();
      }
    },
    onAdvancedSettingsCustom(){
      const formData = new FormData();
      this.isProcessing = true;
      // log advanced settings
      this.userLogger.addAction({'name': 'Advanced settings'})
      formData.append("image", this.picture);
      const backend_server = process.env.BACKEND_SERVER;
      axios
        .post(
          backend_server+"/advancedSearch",
          formData
        )
        .then((response) => {
          // handle successful response
          console.log(response);
          this.isProcessing = false;
          //redirect to results page
          this.$router.push({
            name: "AdvancedSettings",
            state: {
              image: this.picture,
              advancedSettings: response.data,
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
          console.log(error);
        });
    },
    onAdvancedSettings() {
      if (this.custom) {
        this.onAdvancedSettingsCustom();
      } else {
        this.onAdvancedSettingsPrecalculated();
      }
    },
    onAdvancedSettingsPrecalculated(){
      const selected = this.artworks.find((artwork) => artwork.selected);
      const formData = new FormData();
      this.isProcessing = true;
      // log advanced settings
      this.userLogger.addAction({'name': 'clicked on advanced settings', 'Image': selected.name})
      formData.append("image_name", selected.name);
      const backend_server = process.env.BACKEND_SERVER;
      axios
        .post(
          backend_server+"/precalcadvancedSearch",
          formData
        )
        .then((response) => {
          // handle successful response
          this.isProcessing = false;
          //redirect to results page
          this.$router.push({
            name: "AdvancedSettings",
            state: {
              image: this.picture,
              advancedSettings: response.data,
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
          console.log(error);
        });
    },
  },
});
</script>
