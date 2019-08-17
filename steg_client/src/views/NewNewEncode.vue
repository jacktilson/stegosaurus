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
            b-card.mt-3
              File-Input(
                v-model="dataFile"
                @isValid="validDataFile = $event"
                label="Data File"
                description="Enter a data file to hide your data inside"
                placeholder="Choose a data file..."
                dropPlaceholder="Drop a data file here..."
                :filesizeLimit="134217728")
                //- The filesize here is equivalent to 128MiB
              b-collapse(:visible='showImgOption', id="showImg")
                b-row
                  b-col(sm="auto")
                    b-form-group
                      b-form-checkbox(v-model="encodeFilename" ) Encode data file name
                  b-col(sm="auto")
                    b-form-group
                      b-form-checkbox(v-model="encodeFileExt" ) Encode data file extension
                b-form-group(
                    label="Password"
                    label-class="font-weight-bold"
                    description="This is optional, you do not have to give the data a password"
                  )
                    b-form-input(
                      v-model="password"
                      type="password"
                      placeholder="Enter a password to encrypt the data"
                      size="lg"
                    )
            b-collapse(:visible='showImgOption', id="showImg")
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
                  b-card(no-body).overflow-hidden
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
                          div(v-show="!spaceWaiting")
                            b-row
                              b-col(md="auto")
                                b-card-text Estimated Space: {{space}} Bytes
                          div(v-show="imageUploading || spaceWaiting").pt-5
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
                  b-button(v-on:click="submit" :disabled='!enableSubmit') Encode
        b-collapse(v-model="showWaiting")
          scaling-squares-spinner(animation-duration="1024" size="128" color="#3F7F3F").mx-auto.my-4
          b-card-title.text-center Encoding Your Data...
        b-collapse(v-model="showResult")
          b-card-title Download your file below
          b-button(v-on:click="downloadResult") Download

</template>
<script>
import FileInput from "@/components/FileInput.vue";
import ImageFileViewer from "@/components/ImageFileViewer.vue";
import StockImageGetter from "@/components/StockImageGetter.vue";
import { ScalingSquaresSpinner } from "epic-spinners";
import axios from 'axios';

export default {
  name: "Encode",
  components: { FileInput, ImageFileViewer, StockImageGetter, ScalingSquaresSpinner },
  data() {
    return {
      trans_id: "",
      dataFile: null,
      validDataFile: false,
      encodeFilename: true,
      encodeFileExt: true,
      imgFile: null,
      validImgFile: false,
      password: "",
      imgMeta: {
        width: 0,
        height: 0,
        channels: 0,
        bitDepth: 8
      },
      space: 0,
      required: 0,
      nlsb: 1,
      imageUploading: false,
      spaceWaiting: false,
      imgInfoWaiting: false,
      imgFileUploaded: false,
      dataFileUploaded: false,
      readyDownload: false
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
    }
  },
  watch: {
    dataFile() {
      this.dataFileUploaded = false;
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
          this.updateRequired();
        })
        .catch(error => {
          alert(error);
        })
    },
    imgFile() {
      this.imgFileUploaded = false;
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
          this.updateSpace();
        })
        .catch(error => {
          alert(error);
        })
    }
  },
  methods: {
    updateSpace() {
      this.spaceWaiting = true;

      var params = { trans_id: this.trans_id };
      var ext = path.extname(this.dataFile.name);
      var filename = path.basename(this.dataFile.name, ext);
      if(this.encodeFilename) 
        params.filename = filename;
      if(this.encodeFileExt) 
        params.extension = ext.slice(ext.length > 0 ? 1 : 0); // remove the dot from the extension
      if(this.nlsb > 1)
        params.n_lsb = this.nlsb;

      axios
        .get("/encode/image/space", { params })
        .then(response => {
          this.space = response.data.space;
          this.spaceWaiting = false;
        })
        .catch(error => {
          alert(error);
        })
    },
    updateRequired() {
      this.spaceWaiting = true;

      var params = { 
        trans_id: this.trans_id,
        size: this.dataFile.size()
      };
      var ext = path.extname(this.dataFile.name);
      var filename = path.basename(this.dataFile.name, ext);
      if(this.encodeFilename)
        params.filename = filename;
      if(this.encodeFileExt) 
        params.extension = ext.slice(ext.length > 0 ? 1 : 0); // remove the dot from the extension

      axios
        .get("/encode/data/space", { params })
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
      formData.append("data_file", this.dataFile);
      formData.append("trans_id", this.trans_id);
      formData.append("n_lsb", this.nBits);
      if (this.password) {
        formData.append("password", this.password);
      }
      var extension = path.extname(this.dataFile.name);
      var filename = path.basename(this.dataFile.name, extension);
      if (this.encodeFileExt) {
        formData.append(
          "extension",
          extension.slice(extension.length > 0 ? 1 : 0)
        );
      }
      if (this.encodeFilename) {
        formData.append("filename", filename);
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
