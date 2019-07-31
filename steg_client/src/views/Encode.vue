<template lang="pug">
    b-container
        b-row
            b-col(sm="12")
                b-card.mt-5
                    b-card-title Encode Data
                    b-card-text Encode some data within a bitmap image file. The algorithm works by changing the colour
                        |  values of the pixels of an image, embedding the data within the image. If the encoding is good, the
                        | data will be undetectable to the naked eye. It overwrites the least significant bits of each colour
                        | channel with the data to be hidden, changing the actual value by the smallest ammount.
                    form
                        b-form-group(

                        )
                            b-form-file(
                                v-model="dataFile"
                                :state="Boolean(dataFile)"
                                placeholder="Choose a data file to encode..."
                                drop-placeholder="Drop a data file here to encode...")
                        b-form-group
                            b-form-file(
                                v-model="imgFile"
                                :state="Boolean(imgFile)" 
                                placeholder="Choose a bitmap file to encode to..."
                                drop-placeholder="Drop a bitmap file here to encode to...")
                        b-card-text This sets the number of bits to be overwritten per image channel. Higher values start
                            |  to distort the image but allow more data to be encoded within the file.
                        b-form-group
                            b-row
                                b-col(sm="2")
                                    label(for="nBitsInput") Bits: {{nBits}}
                                b-col(sm="10")
                                    b-form-input(id="nBitsInput" type="range" min="0" max="8" v-model="nBits")
                        b-form-group
                            b-form-checkbox(
                                v-model="encodeFilename"                                
                            ) Encode filename
                        b-form-group
                            b-form-checkbox(
                                v-model="encodeFileExt"                                
                            ) Encode file extension
                        b-button(v-on:click="submit") Encode

                    



</template>
<script>
import axios from "axios";
export default {
  name: "Encode",
  data() {
    return {
      nBits: 1,
      dataFile: null,
      imgFile: null,
      encodeFilename: false,
      encodeFileExt: false
    };
  },
  methods: {
    submit() {
      let formData = new FormData();
      formData.append("dataFile", this.dataFile);
      formData.append("imgFile", this.imgFile);
      formData.append("nBits", this.nBits);
      formData.append("encodeFilename", this.encodeFilename);
      formData.append("encodeFileExt", this.encodeFileExt);
      axios
        .post("/encode", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(function(response) {
          alert(response);
        })
        .catch(function(error) {
          alert(error);
        });
    }
  }
};
</script>
<style lang="scss">
.container {
  border: 1px solid red;
}
</style>
