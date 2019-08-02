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
          b-collapse(v-model="showForm")
            form
              b-form-group(
                label="Image File"
                label-for="input-imgFile"
                label-class="font-weight-bold"
                :description="validInputImgFile?'':'Enter a image file to hide your data inside.'"
                :state="validInputImgFile"
                :invalid-feedback="feedbackInvalidInputImgFile"
                :valid-feedback="feedbackValidInputImgFile")
                  b-form-file(
                    id="input-imgFile"
                    v-model="imgFile"
                    placeholder="Choose a bmp/png file..."
                    drop-placeholder="Drop a bmp/png file here to encode to..."
                    :state="validInputImgFile" 
                    v-on:change="imgFileChange($event)")
              b-collapse(v-model="showImgInfo").mb-3
                b-card(no-body).overflow-hidden
                  b-row(no-gutters)
                    b-col(lg="6")
                      b-card-img(:src="imgFileDataString").rounded-0
                    b-col(lg="6")
                      b-card-body(title="Image Preview")
                        b-card-text To be filled with info about image (width, height, channels, bit depth, estimated space available)
              b-collapse(v-model="showDataInput")
                b-form-group(
                  label="Data File"
                  label-for="input-dataFile"
                  label-class="font-weight-bold"
                  :description="dataFile?'':'Enter a data file to encode onto the image'"
                  :state="Boolean(dataFile)"
                  :valid-feedback="dataFile?'Awesome!':''"
                )
                  b-form-file(
                    v-model="dataFile"
                    :state="dataFile"
                    placeholder="Choose file to encode on to image..."
                    drop-placeholder="Drop file here to encode onto image...")
              b-collapse(v-model="showEncodeSettings")
                b-form-group(
                  label="Encoding Settings"
                  label-class="font-weight-bold"
                )
                  b-form-group(
                    :label="`Bits: ${nBits}`"
                    label-for="input-nBits"
                    label-cols-lg="2"
                    description="The number of bits to overwrite per channel of the image"
                  )
                    b-form-input(id="nBitsInput" type="range" min="1" max="8" v-model="nBits")
                  b-form-group
                    b-form-checkbox(v-model="encodeFilename") Encode filename
                  b-form-group
                    b-form-checkbox(v-model="encodeFileExt") Encode file extension
              b-button(v-on:click="submit" :disabled='!enableSubmit') Encode
          b-collapse(v-model="showWaiting")
            b-card-text Waiting for a result...
          b-collapse(v-model="showResult")
            b-card-text Result and download to go here
</template>
<script>
import axios from "axios";

let INVALID = 0;
let VALID = 1;
let SUBMITTED = 2;
let RESULT = 3;

export default {
  name: "Encode",
  data() {
    return {
      formState: INVALID,
      nBits: 1,
      dataFile: null,
      imgFile: null,
      imgFileDataString: "",
      encodeFilename: false,
      encodeFileExt: false
    };
  },
  computed: {
    validInputImgFile() {
      return (
        Boolean(this.imgFile) &&
        ["image/bmp", "image/png"].includes(this.imgFile.type)
      );
    },
    feedbackValidInputImgFile() {
      return this.validInputImgFile ? "Awesome!" : "";
    },
    feedbackInvalidInputImgFile() {
      if (this.imgFile) {
        if (!["image/bmp", "image/png"].includes(this.imgFile.type)) {
          return "Needs to be a .Needs to be a .bmp or a .png";
        }
      }
      return "";
    },
    showForm() {
      return [INVALID, VALID].includes(this.formState);
    },
    enableSubmit() {
      return this.formState === VALID;
    },
    showImgInfo() {
      return this.showForm && this.validInputImgFile;
    },
    showDataInput() {
      return this.showForm && this.validInputImgFile;
    },
    showEncodeSettings() {
      return this.showForm && this.showDataInput && this.dataFile;
    },
    showWaiting() {
      return this.formState === SUBMITTED;
    },
    showResult() {
      return this.formState === RESULT;
    }
  },
  methods: {
    submit() {
      this.formState = SUBMITTED;
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
        .then(response => {
          this.formState = RESULT;
          alert(response);
        })
        .catch(function(error) {
          alert(error);
        });
    },

    imgFileChange(event) {
      //Triggered when the file on the image element changes.
      let input = event.target; //ref to the input element
      if (input.files && input.files[0]) {
        // check the input actually has a file in it
        let reader = new FileReader(); // File reader object for converting file to base64
        reader.onload = event => {
          this.imgFileDataString = event.target.result;
        };
        reader.readAsDataURL(input.files[0]); // Start the reader, calls above function on completion
      }
    },

    formChanged(event) {}
  }
};
</script>
<style lang="scss"></style>
