<template>
  <q-page >
    <div class="row q-gutter-lg" >
      <div class="col-md-5 col-sm-12 q-gutter-lg">
        <q-card class="image-card">
          <q-img
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png"
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
        <PoseCard/>
        <ColorCard/>
        <StyleCard/>
        <ObjectsCard/>
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
    return {};
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
