<template lang="pug">
    b-container
        b-row
            b-col(sm="12")
                b-card.mt-3
                    b-card-title Decode Data
                    b-card-text Decode data from your encoded image which you created on the other page. 
                      | Once you have uploaded the image, you are presented with a button to download the contents.
                    form
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
                        b-collapse(id="imgFilePreviewCollapse" v-model="imgFile")
                          b-card(no-body).overflow-hidden.mb-3
                            b-card-img(:src="imgFileDataString").rounded-0
                        b-button(v-on:click="submit") Decode
</template>
<script>
import axios from "axios";

// Page States

let states = {
  IMG_FILE_INPUT: 0,
  FORM_SUBMITTED: 1,
  FORM_RESULT: 2
  }

export default {
  name: "Decode",
  data() {
    return {
      pageState: states.DATA_FILE_INPUT,
      imgFile: null,
      imgFileDataString: "",
    };
  },
  methods: {
    submit() {
      let formData = new FormData();
      formData.append("imgFile", this.imgFile);
      axios.post("/decode", formData, {
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
