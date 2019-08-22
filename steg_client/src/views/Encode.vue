<template lang="pug">
  b-container
    b-row
      b-col(sm="12")
        AccordionQA.mt-3(title="Encode" :visible="showAbout" accordionID="acc" answerID="qa1")
          b-card-body
            b-card-text Encode some data within a bitmap image file. The algorithm works by changing the colour
              |  values of the pixels of an image, embedding the data within the image. If the encoding is good, the
              | data will be undetectable to the naked eye. It overwrites the least significant bits of each colour
              | channel with the data to be hidden, changing the actual value by the smallest amount.
        b-collapse(v-model="showForm" id="showForm")
          form
            b-card.mt-3
              File-Input(
                v-model="data"
                label="Data File"
                description="Enter a data file to hide your data inside"
                placeholder="Choose a data file..."
                dropPlaceholder="Drop a data file here..."
                :filesizeLimit="134217728")
                //- The filesize here is equivalent to 128MiB
              b-collapse(:visible='dataUploaded' id="showImg")
                b-card-text Size: {{ getDataSize }} Bytes
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
                  description="This is optional, you do not have to give the data a password")
                  b-form-input(
                    v-model="password"
                    type="password"
                    placeholder="Enter a password to encrypt the data"
                    size="lg")
            b-collapse(:visible='dataUploaded' id="showImgOptions")
              b-card.mt-3
                b-row
                  b-col(lg="5")
                    File-Input(
                      v-model="img"
                      ref="imgFileInput"
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
                      StockImageGetter.w-100.btn-lg.btn-brand(v-model="img" v-on:clear="$refs['imgFileInput'].reset()"
                        :width="getStockWidth"
                        :height="getStockHeight")
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
                b-collapse(:visible='showImgPreview' id='showImgPreview')
                  b-card(no-body).overflow-hidden.mb-3
                    b-row(no-gutters)
                      b-col(lg="6")
                        ImageFileViewer(:imgFile="img").rounded-0.card-img
                      b-col(lg="6")
                        b-card-body(:title="imgMeta.name")
                          div(v-show="!imgUploading")
                            b-row
                              b-col(md="auto")
                                b-card-text Width: {{ imgMeta.width }} px
                              b-col(md="auto")
                                b-card-text Height: {{ imgMeta.height }} px
                              b-col(md="auto")
                                b-card-text Channels: {{ imgMeta.channels }}
                              b-col(md="auto")
                                b-card-text Bit Depth: {{ imgMeta.bitDepth }}
                            b-row
                              b-col(md="auto")
                                b-card-text Estimated data space: {{ numberWithCommas(spaceAvailable) }} Bytes
                            b-row
                              b-col(md="auto")
                                b-card-text.text-danger(v-if="!dataFits") Image is too small for the data file.
                          div(v-show="imgUploading").pt-5
                            scaling-squares-spinner.mx-auto(
                              :animation-duration="1024"
                              :size="64"
                              color="#3F7F3F")
                            b-card-text.text-center Loading...
              b-collapse(:visible="showSubmitButton" id="showSubmitButton")
                b-row
                  b-col(sm="12").d-flex
                    b-btn.m-4.w-100.btn-brand(v-on:click="submit" :disabled="!isFormValid" size="lg") Encode
        b-collapse(v-model="showLoading" id="showLoading")
          b-card.mt-3
            scaling-squares-spinner(:animation-duration="1024" :size="128" color="#3F7F3F").mx-auto.my-4
            b-card-title.text-center Encoding Your Data...
        b-collapse(v-model="showResult" id="showResult")
          b-card.mt-3
            b-card-title Download your encoded file below
            b-btn.btn-brand.btn-lg.w-100(v-on:click="downloadResult") Download
</template>
<script>
import FileInput from "@/components/FileInput.vue";
import ImageFileViewer from "@/components/ImageFileViewer.vue";
import StockImageGetter from "@/components/StockImageGetter.vue";
import AccordionQA from "@/components/AccordionQA.vue";
import { ScalingSquaresSpinner } from "epic-spinners";
import path from "path";
import { saveAs } from "file-saver";
import axios from "axios";

export default {
  name: "Encode",
  components: { 
    FileInput, 
    ImageFileViewer, 
    StockImageGetter, 
    ScalingSquaresSpinner, 
    AccordionQA 
  },
  data() {
    return {
      trans_id: "",

      //- Data file
      data: null,
      dataUploaded: false,
      dataUploading: false,
      pixelsRequired: 0,

      //- Img file
      img: null,
      imgUploaded: false,
      imgUploading: false,
      imgMetaWaiting: false,
      spaceAvailable: 0,
      imgMeta: {
        name: "",
        width: 0,
        height: 0,
        channels: 0,
        bitDepth: 8
      },

      //- Options
      encodeFilename: true,
      encodeFileExt: true,
      password: "",
      nlsb: 1,
      minlsb: 1,
      //- Status
      showForm: true,
      showLoading: false,
      showResult: false
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
      });
  },
  computed: {
    showImgPreview() {
      return Boolean(this.img);
    },
    showSubmitButton() {
      return Boolean(this.img);
    },
    enableSubmit() {
      return this.imgUploaded && this.dataUploaded;
    },
    filename() {
      var extension = path.extname(this.data.name);
      return path.basename(this.data.name, extension);
    },
    extension() {
      var extension = path.extname(this.data.name);
      return extension.slice(extension.length > 0 ? 1 : 0);
    },
    dataFits() {
      if(this.imgMeta.width * this.imgMeta.height > this.pixelsRequired)
        return true;
      else
        return false;
    },
    getStockWidth() {
      if(this.pixelsRequired > 25000000)
        return 5000;
      if(this.pixelsRequired > 7800000)
        return Math.ceil(Math.sqrt(this.pixelsRequired));
      if(this.pixelsRequired > 129600)
        return Math.ceil(Math.sqrt((16/9)*this.pixelsRequired));
      else
        return 480;
    },
    getStockHeight() {
      if(this.pixelsRequired > 25000000)
        return 5000;
      if(this.pixelsRequired > 7800000)
        return Math.ceil(Math.sqrt(this.pixelsRequired));
      if(this.pixelsRequired > 129600)
        return Math.ceil(Math.sqrt((9/16)*this.pixelsRequired));
      else
        return 270;
    },
    getDataSize() {
      if(this.data)
        return this.numberWithCommas(this.data.size);
      else
        return "";
    },
    showAbout() {
      return Boolean(!this.data);
    },
    isFormValid() {
      if(this.dataFits && this.imgUploaded && this.dataUploaded)
        return true;
      else
        return false;
    }
  },
  watch: {
    data() {
      if(this.data) {
        this.dataUploaded = false;
        this.dataUploading = true;
        // Add the trans_id and the datafile to the formdata
        let formData = new FormData();
        formData.append("trans_id", this.trans_id);
        formData.append("data_file", this.data);
        // Post the data to the server, to associate a data file with the trans_id
        axios
          .post("/encode/data/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          // eslint-disable-next-line
          .then(response => {
            this.dataUploaded = true;
            this.dataUploading = false;
            this.updateRequired();
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    img() {
      if (this.img) {
        this.imgUploaded = false;
        this.imgUploading = true;
        this.imgMeta.name = this.img.name;
        // Add the trans_id and the imgfile to the formdata
        let formData = new FormData();
        formData.append("trans_id", this.trans_id);
        formData.append("img_file", this.img);
        // Post the data to the server, to associate a data file with the trans_id
        axios
          .post("/encode/image/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          // eslint-disable-next-line
          .then(response => {
            this.imgUploaded = true;
            this.imgMeta.width = response.data.width;
            this.imgMeta.height = response.data.height;
            this.imgMeta.channels = response.data.channels;
            this.imgMeta.bitDepth = response.data.bitdepth;
            this.imgUploading = false;
            this.updateSpace();
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    nlsb() {
      if(this.imgUploaded)
        this.updateSpace();
      this.updateRequired();
    }
  },
  methods: {
    updateSpace() {
      var params = { 
        trans_id: this.trans_id,
        n_lsb: this.nlsb
       };
      axios
        .get("/encode/image/space", { params })
        .then(response => {
          this.spaceAvailable = response.data.space_available;
        })
        .catch(error => {
          alert(error);
        });
    },
    updateRequired() {
      var params = { 
        trans_id: this.trans_id,
        filename: this.filename,
        extension: this.extension,
        n_lsb: this.nlsb
      };
      axios
        .get("/encode/data/space", { params })
        .then(response => {
          this.pixelsRequired = response.data.pixels_required;
          this.minlsb = response.data.min_lsb;
        })
        .catch(error => {
          alert(error);
        });
    },
    submit() {
      if(this.isFormValid) {
        this.showResult = false;
        this.showForm = false;
        this.showLoading = true;
        //- Build formdata
        let formData = new FormData();
        formData.append("trans_id", this.trans_id);
        formData.append("n_lsb", this.nlsb);
        if(this.encodeFilename)
          formData.append("filename", this.filename);
        if(this.encodeFileExt)
          formData.append("extension", this.extension);
        if(this.password)
          formData.append("password", this.password);
        axios
          .post("/encode/complete", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(response => {
            this.showForm = false;
            this.showLoading = false;
            this.showResult = true;
          })
          .catch(error => {
            this.showForm = true;
            this.showLoading = false;
            this.showResult = false;
            alert(error);
          })
      }
    },
    delete() {
      axios
        .get("/encode/delete", {
        params: {
            trans_id: this.trans_id
          },
          responseType: "arraybuffer"
        })
        .then(response => {
          window.is_deleted = true
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
          if (window.is_deleted != true){
            this.delete();
          }
        })
        .catch(error => {
          alert(error);
        });
    },
    numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
};
</script>
