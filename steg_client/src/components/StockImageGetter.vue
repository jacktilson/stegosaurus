<template lang="pug">
    b-btn(v-on:click="getImage()") Get Stock Image
</template>
<script>
import axios from "axios";

export default {
    name: "StockImageGetter",
    props: ["width", "height"],
    data(){return {
        imgFile: null
    }},
    model: {prop: "imgFile", event: "change"},
    methods: {
      getImage(){
        axios
          .get(`https://picsum.photos/${this.width}/${this.height}`, {
            responseType: "blob"
          })
          .then(response => {
            this.imgFile = new File(
              [response.data],
              `img_${this.width}_${this.height}.${response.headers["content-type"].split("/")[1]}`,
              {type: response.headers["content-type"]});
            this.$emit("clear");

          })
          .catch(error => {
            alert(error);
          })
      }
    },
    watch: {
      imgFile(val) {
        this.$emit("change", val);
      }
    }   
}
</script>