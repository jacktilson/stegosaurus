<template lang="pug">
    b-container
        b-row
            b-col(sm="12")
                b-card.mt-3
                    b-card-title Encode Data
                    b-card-text Encode some data within a bitmap image file. The algorithm works by changing the colour
                        |  values of the pixels of an image, embedding the data within the image. If the encoding is good, the
                        | data will be undetectable to the naked eye. It overwrites the least significant bits of each colour
                        | channel with the data to be hidden, changing the actual value by the smallest amount.
                    form
                        b-form-group
                            b-form-file(
                              v-model="imgFile"
                              :state="Boolean(imgFile)" 
                              placeholder="Choose a bitmap file to encode to..."
                              drop-placeholder="Drop a bitmap file here to encode to..."
                              v-on:change="imgFileChange($event)")

                        b-collapse(id="imgFilePreviewCollapse" v-model="imgFile")
                          b-card(no-body).overflow-hidden.mb-3
                            b-row(no-gutters)
                              b-col(lg="6")
                                b-card-img(:src="imgFileDataString").rounded-0
                              b-col(lg="6")
                                b-card-body(title="Image Preview")
                                  b-card-text To be filled with info about image (width, height, channels, bit depth, estimated space available)
                        b-form-group
                            b-form-file(
                              v-model="dataFile"
                              :state="Boolean(dataFile)"
                              placeholder="Choose file to encode on to image..."
                              drop-placeholder="Drop file here to encode onto image...")
                        b-card-text This sets the number of bits to be overwritten per image channel. Higher values start
                            |  to distort the image but allow more data to be encoded within the file.
                        b-form-group
                            b-row
                                b-col(sm="2")
                                    label(for="nBitsInput") Bits: {{nBits}}
                                b-col(sm="10")
                                    b-form-input(id="nBitsInput" type="range" min="1" max="8" v-model="nBits")
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

// Page States

let states = {
  IMG_FILE_INPUT: 0,
  DATA_FILE_INPUT: 1,
  SETTINGS_INPUT: 2,
  FORM_COMPLETE: 3,
  FORM_SUBMITTED: 4,
  FORM_RESULT: 5
  }

export default {
  name: "Encode",
  data() {
    return {
      pageState: states.IMG_FILE_INPUT,
      nBits: 1,
      dataFile: null,
      imgFile: null,
      imgFileDataString: "",
      encodeFilename: true,
      encodeFileExt: true
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
      axios.post("/encode", formData, {
        headers: {
            "Content-Type": "multipart/form-data"
          }})
        .then(function(response) {
          alert(response);
        })
        .catch(function(error) {
          alert(error);
        });
    },
    imgFileChange(event) { //Triggered when the file on the image element changes.
      let input = event.target; //ref to the input element
      if (input.files && input.files[0]) { // check the input actually has a file in it
        let reader = new FileReader(); // File reader object for converting file to base64
        reader.onload = (event) => {
          this.imgFileDataString = event.target.result;
        }
        reader.readAsDataURL(input.files[0]); // Start the reader, calls above function on completion
      }
    }

  }
};
</script>
<style lang="scss">
</style>
