<template>
  <q-page class="flex flex-center">
    <q-spinner color="primary" size="3em" v-show="isProcessing" />
    <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-gutter-md"
      style="width: 500px"
      v-show="!isProcessing"
    >
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
        <Slider
          v-for="(axis, index) in axes"
          :key="index"
          :axis="axis"
          @update:value="updateValue"
          @change="value=>userLogger.addAction({'name': 'Change weight', 'Axis': axis.name, 'Value': value })"
        ></Slider>
      </q-list>
      <div class="center-button">
        <q-btn
          id="submit"
          class="q-mx-lg"
          label="Search"
          type="submit"
          color="primary"
        /><q-btn
          class="q-mx-lg"
          label="Advanced Options"
          size="sm"
          color="secondary"
          @click="onAdvancedSettings()"
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
</style>

<script>
import { defineComponent, ref } from "vue";
import Slider from "../components/Slider.vue";
import axios from "axios";
import UserLogger from "../UserLogger";

export default defineComponent({
  components: { Slider },
  name: "IndexPage",
  setup() {
    const analytics_server = process.env.ANALYTICS_SERVER;
    var userLogger = new UserLogger(analytics_server,
        10, 20, 'data', {'user': 'expert',
            'page': 'index',
            'condition': 'sliders+advancedoptions'})
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

    return { axes, picture: ref(null), isProcessing: ref(false), queryImage: ref(null), userLogger };
  },
  methods: {
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
    },
    onSubmit() {
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
    onAdvancedSettings() {
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
  },
});
</script>
