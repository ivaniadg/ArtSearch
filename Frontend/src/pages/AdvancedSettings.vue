<template>
  <q-page >
    <div class="row q-gutter-lg" >
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
          :to="{ name: 'Index' }"
        />
      </div>
      </div>
      <div class="col-md-5 col-sm-12 q-gutter-lg">
        <PoseCard :persons="analyzed_pose.persons" />
        <ColorCard :colors="analyzed_colors" />
        <ObjectsCard :objects="analyzed_objects" />
        <StyleCard/>
      </div>
    </div>
  </q-page>
</template>

<script>
import PoseCard from "../components/PoseCard.vue";
import ColorCard from "../components/ColorCard.vue";
import StyleCard from "../components/StyleCard.vue";
import ObjectsCard from "../components/ObjectsCard.vue";

export default {
  components: { PoseCard, ColorCard, StyleCard, ObjectsCard },
  data() {
    const analyzed_pose = history.state.advancedSettings.pose;
    const analyzed_colors = history.state.advancedSettings.colors;
    // const analyzed_style = history.state.advancedSettings.style;
    const analyzed_objects = history.state.advancedSettings.objects;
    const image = analyzed_pose.image
    return {
      analyzed_pose,
      analyzed_colors,
      // analyzed_style,
      analyzed_objects,
      image
    };
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
  height: 25%
}
</style>
