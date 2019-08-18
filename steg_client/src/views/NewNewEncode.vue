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
        b-collapse(v-model="formStatus != READY")
          form
            b-card.mt-3
              File-Input(
                v-model="data.file"
                @isValid="data.state ? $event VALID : INVALID"
                label="Data File"
                description="Enter a data file to hide your data inside"
                placeholder="Choose a data file..."
                dropPlaceholder="Drop a data file here..."
                :filesizeLimit="134217728")
                //- The filesize here is equivalent to 128MiB
              b-collapse(:visible='data.state == VALID', id="showImg")
                b-row
                  b-col(sm="auto")
                    b-form-group
                      b-form-checkbox(v-model="data.options.filename" ) Encode data file name
                  b-col(sm="auto")
                    b-form-group
                      b-form-checkbox(v-model="data.options.extension" ) Encode data file extension
                b-form-group(
                  label="Password"
                  label-class="font-weight-bold"
                  description="This is optional, you do not have to give the data a password")
                  b-form-input(
                    v-model="data.options.password"
                    type="password"
                    placeholder="Enter a password to encrypt the data"
                    size="lg")
            b-collapse(:visible='data.state == VALID', id="showImgOptions")
              b-card.mt-3
                b-row
                  b-col(lg="5")
                    File-Input(
                      v-model="imgFile"
                      ref="imgFileInput"
                      :isValid="validImgFile"
                      label="Image Upload"
                      description="Upload an image here to encode your data inside"
                      placeholder="Choose an image..."
                      dropPlaceholder="Drop an image here.."
                      :filesizeLimit="134217728"
                      :fileTypes="['.jpg', '.png', '.bmp', '.tiff', '.jpeg']"
                      :mimeTypes="['image/jpeg', 'image/png', 'image/bmp', 'image/tiff']")
                  b-col(lg="2").my-auto.text-center
                    b-card-title or
                  b-col(lg="5")
                    b-form-group(
                      label-for="useStock"
                      label="Use Stock Image"
                      label-class="font-weight-bold"
                      description="Automatically find a stock image to use instead")
                      StockImageGetter.w-100.btn-lg(v-model="imgFile" v-on:clear="$refs['imgFileInput'].reset()"
                        width="1920"
                        height="1080")
                b-collapse(:visible='showImgPreview', id='showImgPreview')
                  b-card(no-body).overflow-hidden.mb-3
                    b-row(no-gutters)
                      b-col(lg="6")
                        ImageFileViewer(:imgFile="imgFile").rounded-0.card-img
                      b-col(lg="6")
                        b-card-body(:title="`Image: ${imgFile?imgFile.name:''}`")
                          div(v-show="!imageUploading")
                            b-row
                              b-col(md="auto")
                                b-card-text Width: {{imgMeta.width}}
                              b-col(md="auto")
                                b-card-text Height: {{imgMeta.height}}
                              b-col(md="auto")
                                b-card-text Channels: {{imgMeta.channels}}
                              b-col(md="auto")
                                b-card-text Bit Depth: {{imgMeta.bitDepth}}
                            b-row
                              b-col(md="auto")
                                b-card-text Estimated Space: {{space}} Bytes
                          div(v-show="imageUploading").pt-5
                            scaling-squares-spinner.mx-auto(
                              :animation-duration="1024"
                              :size="64"
                              color="#3F7F3F")
                            b-card-text.text-center Loading...
                  b-form-group(
                    :label="`Bits: ${nlsb}`"
                    label-for="input-nlsb"
                    label-cols-lg="2"
                    description="The number of bits to overwrite per channel of the image")
                    b-form-input(
                      id="input-nlsb"
                      type="range"
                      min="1"
                      :max="imgMeta.bitDepth" 
                      v-model="nlsb")
              b-collapse(:visible="showImgPreview" id="showSubmitButton")
                b-row
                  b-col(sm="12").d-flex
                    b-button.m-4.w-100(v-on:click="submit" size="lg") Encode
        b-collapse(v-model="formStatus == UPLOADING")
          scaling-squares-spinner(animation-duration="1024" size="128" color="#3F7F3F").mx-auto.my-4
          b-card-title.text-center Encoding Your Data...
        b-collapse(v-model="formStatus == READY")
          b-card-title Download your file below
          b-button(v-on:click="readyDownload") Download

</template>
<script>
import FileInput from "@/components/FileInput.vue";
import ImageFileViewer from "@/components/ImageFileViewer.vue";
import StockImageGetter from "@/components/StockImageGetter.vue";
import { ScalingSquaresSpinner } from "epic-spinners";
import path from "path";
import { saveAs } from "file-saver";
import axios from 'axios';

let INVALID = 0;
let VALID = 1;
let UPLOADING = 2;
let READY = 3;

export default {
  name: "Encode",
  components: { FileInput, ImageFileViewer, StockImageGetter, ScalingSquaresSpinner },
  data() {
    return {
      trans_id: "",
      formStatus: INVALID,
      img: {
        file: null,
        state: INVALID,
        spaceAvailable: 0,
        meta: {
          waiting: false,
          width: 0,
          height: 0,
          channels: 0,
          bitDepth: 8
        },
        options: {
          nlsb: 1
        }
      },
      data: {
        file: null,
        state: INVALID,
        spaceRequired: 0,
        options: {
          password: "",
          filename: true,
          extension: true
        }
      }
    };
  },
  created() {
    axios
      .get("/encode/init")
      .then(response => {
        this.trans_id = response.data.trans_id;
      })
      .catch(error => {
        alert(error);
      })
  },
  computed: {
    showImgOption() {
      return this.validDataFile;
    },
    showImgPreview() {
      return Boolean(this.imgFile);
    },
    enableSubmit() {
      return this.imgFileUploaded && this.dataFileUploaded;
    }
  },
  watch: {
    dataFile() {
      this.dataFileUploaded = false;
      if(this.validDataFile) {
        this.dataFileUploading = true;
        // Add the trans_id and the datafile to the formdata
        let formData = new FormData();
        formData.append("trans_id", this.trans_id);
        formData.append("data_file", this.dataFile);
        // Post the data to the server, to associate a data file with the trans_id
        axios
          .post("/encode/data/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          // eslint-disable-next-line
          .then(response => {
            this.dataFileUploaded = true;
            this.dataFileUploading = false;
            this.updateRequired();
          })
          .catch(error => {
            alert(error);
          })
      }
    },
    imgFile() {
      this.imgFileUploaded = false;
      this.imageUploading = true;
      // Add the trans_id and the imgfile to the formdata
      let formData = new FormData();
      formData.append("trans_id", this.trans_id);
      formData.append("img_file", this.imgFile);
      // Post the data to the server, to associate a data file with the trans_id
      axios
        .post("/encode/image/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        // eslint-disable-next-line
        .then(response => {
          this.imgFileUploaded = true;
          this.imgMeta.width = response.data.width;
          this.imgMeta.height = response.data.height;
          this.imgMeta.channels = response.data.channels;
          this.imgMeta.bitDepth = response.data.bitdepth;
          this.imgFileUploaded = true;
          this.imageUploading = false;
          this.updateSpace();
        })
        .catch(error => {
          alert(error);
        })
    },
    nlsb() {
      this.updateSpace();
    },
    encodeFilename() {
      this.updateSpace();
    }
  },
  methods: {
    updateSpace() {
      this.spaceWaiting = true;

      var params = { trans_id: this.trans_id };
      if(this.nlsb > 1)
        params.n_lsb = this.nlsb;
      axios
        .get("/encode/image/space", { params })
        .then(response => {
          this.space = response.data.space_available;
          this.spaceWaiting = false;
        })
        .catch(error => {
          alert(error);
        })
    },
    updateRequired() {
      this.spaceWaiting = true;

      axios
        .get("/encode/data/space", { trans_id: this.trans_id })
        .then(response => {
          this.required = response.data.space;
          this.spaceWaiting = false;
        })
        .catch(error => {
          alert(error);
        })
    },
    submit() {
      this.readyDownload = false;
      // Build formdata
      let formData = new FormData();
      formData.append("trans_id", this.trans_id);
      formData.append("n_lsb", this.nlsb);
      formData.append("encode_filename", this.encodeFilename);
      formData.append("encode_extension", this.encodeFileExt);
      if (this.password) {
        formData.append("password", this.password);
      }
      axios
        .post("/encode/complete", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.readyDownload = true;
        })
        .catch(error => {
          alert(error);
        })
    },
    downloadResult() {
      axios
        .get("/encode/download", {
          params: {
            trans_id: this.trans_id
          },
          responseType: "arraybuffer"
        })
        .then(response => {
          let filename = /filename=(?<filename>.*)$/g.exec(
            response.headers["content-disposition"]
          ).groups.filename;
          saveAs(new Blob([response.data]), filename);
        })
        .catch(error => {
          alert(error);
        });
    },
  }
};
</script>
