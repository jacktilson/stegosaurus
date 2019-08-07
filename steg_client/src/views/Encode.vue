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
                :description="validImgFile?'':'Enter a image file to hide your data inside.'"
                :state="validImgFile"
                :invalid-feedback="feedbackInvalidImgFile"
                :valid-feedback="feedbackValidImgFile")
                  b-form-file(
                    id="input-imgFile"
                    v-model="imgFile"
                    placeholder="Choose a bmp/png file..."
                    drop-placeholder="Drop a bmp/png file here to encode to..."
                    :state="validInputImgFile")
              b-collapse(v-model="showImgInfo").mb-3
                b-card(no-body).overflow-hidden
                  b-row(no-gutters)
                    b-col(lg="6")
                      b-card-img(:src="imgFileDataString").rounded-0
                    b-col(lg="6")
                      b-card-body(:title="`Image: ${imgFile?imgFile.name:''}`")
                        b-row
                          b-col(md="auto")
                            b-card-text Dimensions: {{imgMeta.width}} x {{imgMeta.height}}
                          b-col(md="auto")
                            b-card-text Channels: {{imgMeta.channels}}
                          b-col(md="auto")
                            b-card-text Bit Depth: {{imgMeta.bitDepth}}
                        b-card-text Estimated Space: {{space}} Bytes
              b-collapse(v-model="showDataInput")
                b-form-group(
                  label="Data File"
                  label-for="input-dataFile"
                  label-class="font-weight-bold"
                  :description="dataFile?'':'Enter a data file to encode onto the image'"
                  :state="validDataFile"
                  :invalid-feedback="feedbackInvalidDataFile"
                  :valid-feedback="feedbackValidDataFile"
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
                    b-form-input(
                      id="nBitsInput"
                      type="range"
                      min="1"
                      :max="imgMeta.bitDepth" 
                      v-model="nBits")
                  b-form-group
                    b-form-checkbox(v-model="encodeFilename" ) Encode filename
                  b-form-group
                    b-form-checkbox(v-model="encodeFileExt" ) Encode file extension
              b-button(v-on:click="submit" :disabled='!enableSubmit') Encode
          b-collapse(v-model="showWaiting")
            b-card-text Waiting for a result...
          b-collapse(v-model="showResult")
            b-card-text Result and download to go here
</template>
<script>
import axios from "axios";
import path from "path";

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
      imgMeta: {
        width: 0,
        height: 0,
        channels: 0,
        bitDepth: 0
      },
      encodeFilename: false,
      encodeFileExt: false,
      transactionID: "",
      space: 0
    };
  },
  computed: {
    validImgFile() {
      return (
        Boolean(this.imgFile) &&
        ["image/bmp", "image/png"].includes(this.imgFile.type)
      );
    },
    feedbackValidImgFile() {
      return this.validInputImgFile ? "Awesome!" : "";
    },
    feedbackInvalidImgFile() {
      if (this.imgFile) {
        if (!["image/bmp", "image/png"].includes(this.imgFile.type)) {
          return "Needs to be a .bmp or a .png";
        }
      }
      return "";
    },
    validDataFile() {
      return Boolean(this.dataFile) && this.dataFile.size <= this.space;
    },
    feedbackValidDataFile() {
      return this.validDataFile?"Awesome":"";
    },
    feedbackInvalidDataFile() {
      if (this.dataFile) {
        if (this.dataFile.size > this.space){
          return "Data file too large for that image on these settings.";
        }
      }
      return "";
    },
    showForm() {
      return [INVALID, VALID].includes(this.formState);
    },
    enableSubmit() {
      return (this.validInputImgFile && this.validDataFile);
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
  watch: {
    imgFile(val, oldval) {
      if (this.validInputImgFile) {
        // check the input actually has a valid file in it
        let reader = new FileReader(); // File reader object for converting file to base64
        reader.onload = event => {
          this.imgFileDataString = event.target.result;
        };
        reader.readAsDataURL(this.imgFile); // Start the reader, calls above function on completion
      }

      //also trigger upload of file to server
      let formData = new FormData();
      formData.append("img_file", this.imgFile);
      axios
        .post("/encode/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.transactionID = response.data.trans_id;
          this.imgMeta.width = response.data.width;
          this.imgMeta.height = response.data.height;
          this.imgMeta.channels = response.data.channels;
          this.imgMeta.bitDepth = response.data.bitdepth;
          this.updateSpace();
        })
        .catch(error => {
          alert(error);
        });
    },
    dataFile(val, oldval){
      this.updateSpace();
    },
    nBits(val, oldval){
      this.updateSpace();
    },
    encodeFilename(val, oldval){
      this.updateSpace();
    },
    encodeFileExt(val, oldval){
      this.updateSpace();
    }
  },
  methods: {
    submit() {
      this.formState = SUBMITTED;

      // Build formdata
      let formData = new FormData();
      formData.append("data_file", this.dataFile);
      formData.append("trans_id", this.transactionID);
      formData.append("n_lsb", this.nBits);
      if (this.encodeFilename){
        formData.append("filename", this.dataFile.name);
      }
      if (this.encodeFileExt){
        formData.append("extension", this.dataFile.type);
      }

      // Post it
      axios
        .post("/encode/complete", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.formState = RESULT;
          alert(response);
        })
        .catch(error => {
          alert(error);
        });
    },

    updateSpace() {

      // Build params
      var params = { trans_id: this.transactionID };
      if (this.dataFile) {
        var ext = path.extname(this.dataFile.name);
        var filename = path.basename(this.dataFile.name, ext);
        if (this.encodeFilename) {
          params.filename = filename;
        }
        if (this.encodeFileExt) {
          params.extension = ext;
        }
      }
      if (this.nBits > 1) {
        params.n_lsb = this.nBits;
      }

      // Post it
      axios
        .get("/encode/space", { params })
        .then(response => {
          this.space = response.data.space_available;
          this.validateForm();
        })
        .catch(error => {
          alert(error);
        });
    },

    validateForm() {
      if (this.validInputImgFile && this.validDataFile) {
        this.formState = VALID;
      } else {
        this.formState = INVALID;
      }
    }
  }
};
</script>
<style lang="scss"></style>
d
