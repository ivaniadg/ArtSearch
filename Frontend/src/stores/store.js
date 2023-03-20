import { defineStore } from 'pinia';

export const useStore = defineStore('store', {
  state: () => ({
    queryImage: null
  }),
  actions: {
    setQueryImage(queryImage) {
      console.log('setQueryImage', queryImage);
      this.queryImage = queryImage;
    }
  },
  getters: {
    getQueryImage() {
      return this.queryImage;
    }
  }
})
