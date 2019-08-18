<template lang="pug">
b-container
  b-row
    b-col(sm="12")
      b-card.mt-3
        b-card-title Decode Data
        b-card-text Decode data from your encoded image which you created on the other page. 
          | Once you have uploaded the image, you are presented with a button to download the contents.
        b-collapse(v-model="showForm")
          form
            b-row
              b-col(md="6")
                b-form-group(
                  label="Encoded Image File"
                  label-for="input-imgFile"
                  label-class="font-weight-bold"
                  :description="validInputImgFile?'':'Enter your encoded image file to decode the data inside'"
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
              b-col(md="6")
                b-form-group(
                  label="Password"
                  description="Only required if encoded with a password"
                )
                  b-form-input(
                    v-model="password"
                    type="password"
                    placeholder="Enter password to decrypt data"
                  )
            b-collapse(id="imgFilePreviewCollapse" v-model="imgFile")
              b-card(no-body).overflow-hidden.mb-3
                b-card-img(:src="imgFileDataString").rounded-0
            b-button.btn-brand(v-on:click="submit") Decode
        b-card-body(v-show="imgDownloadWaiting")
          scaling-squares-spinner.mx-auto.my-auto(
            v-show="imgDownloadWaiting"
            animation-duration="1024"
            size="128"
            color="#3F7F3F")
          b-card-text.text-center Decoding Your Data...
        b-collapse(v-model="showResult")
            b-card-text Download your file below
            b-button.btn-brand(v-on:click="downloadResult()") Download
</template>
<script>
import axios from "axios";
import { saveAs } from "file-saver";
import { ScalingSquaresSpinner } from "epic-spinners";
// Page States

let states = {
  IMG_FILE_INPUT: 0,
  FORM_SUBMITTED: 1,
  FORM_RESULT: 2
};

export default {
  name: "Decode",
  components: { ScalingSquaresSpinner },
  data() {
    return {
      pageState: states.DATA_FILE_INPUT,
      imgFile: null,
      imgFileDataString: "",
      imgDownloadWaiting: false,
      showForm: true,
      showResult: false,
      dataFile: null,
      fileName: null,
      password: ""
    };
  },
  methods: {
    submit() {
      this.imgDownloadWaiting = true;
      this.showForm = false;
      let formData = new FormData();
      formData.append("img_file", this.imgFile);
      if (this.password) {
        formData.append("password", this.password);
      }
      axios
        .post("/decode/process", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          responseType: "arraybuffer"
        })
        .then(response => {
          this.imgDownloadWaiting = false;
          this.showResult = true;
          this.dataFile = new Blob([response.data]);
          this.fileName = /filename=(?<filename>.*)$/g.exec(
            response.headers["content-disposition"]
          ).groups.filename;
          this.downloadResult();
        })
        .catch(error => {
          alert(error);
        });
    },
    downloadResult() {
      saveAs(this.dataFile, this.fileName);
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
    }
  }
};
</script>
<style lang="scss"></style>
