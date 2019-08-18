<template lang="pug">
b-container
  b-row
    b-col(sm="12")
      AccordionQA.mt-3(title="Decode" :visible="showAbout" accordionID="acc" answerID="qa1")
        b-card-body
          b-card-text Decode data from your encoded image which you created on the other page. 
            | Once you have uploaded the image, you are presented with a button to download the contents.
      b-collapse(v-model="showForm" id="showForm")
        form
          b-card.mt-3
            b-row
              b-col(md="6")
                File-Input(
                  v-model="img"
                  ref="imgFileInput"
                  :isValid="imgValid"
                  label="Image Upload"
                  description="Upload your encoded image here to decode"
                  placeholder="Choose an image..."
                  dropPlaceholder="Drop an image here.."
                  :filesizeLimit="134217728"
                  :fileTypes="['.png']"
                  :mimeTypes="['image/png']")
              b-col(md="6")
                b-form-group(
                  label="Password"
                  description="Only required if encoded with a password")
                  b-form-input(
                    size="lg"
                    v-model="password"
                    type="password"
                    placeholder="Enter password to decrypt data")
            b-collapse(v-model="showImgPreview" id="showImgPreview")
                  ImageFileViewer(:imgFile="img").rounded-0.card-img
          b-collapse(v-model="showSubmitButton" id="showSubmitButton")
            b-row
              b-col(sm="12").d-flex
                b-btn.m-4.w-100.btn-brand(v-on:click="submit" size="lg") Decode
      b-collapse(v-model="showLoading" id="showLoading")
          b-card.mt-3
            scaling-squares-spinner(:animation-duration="1024" :size="128" color="#3F7F3F").mx-auto.my-4
            b-card-title.text-center Decoding Your Data...
      b-collapse(v-model="showResult" id="showResult")
          b-card.mt-3
            b-card-title Download your decoded file below
            b-btn.btn-brand.btn-lg.w-100(v-on:click="downloadResult") Download
</template>
<script>
import FileInput from "@/components/FileInput.vue";
import ImageFileViewer from "@/components/ImageFileViewer.vue";
import AccordionQA from "@/components/AccordionQA.vue";
import axios from "axios";
import { saveAs } from "file-saver";
import { ScalingSquaresSpinner } from "epic-spinners";

export default {
  name: "Decode",
  components: { ScalingSquaresSpinner, FileInput, ImageFileViewer, AccordionQA },
  data() {
    return {
      //- Img file
      img: null,
      imgValid: false,

      //- Options
      password: "",

      //- Status
      showForm: true,
      showLoading: false,
      showResult: false
    };
  },
  computed: {
    showImgPreview() {
      return Boolean(this.img);
    },
    showSubmitButton() {
      return Boolean(this.img);
    },
    showAbout() {
      return Boolean(!this.img);
    }
  },
  methods: {
    submit() {
      this.showResult = false;
      this.showForm = false;
      this.showLoading = true;
      //- Build formdata
      let formData = new FormData();
      formData.append("img_file", this.img);
      if (this.password)
        formData.append("password", this.password);
      axios
        .post("/decode/process", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          responseType: "arraybuffer"
        })
        .then(response => {
          this.dataFile = new Blob([response.data]);
          this.fileName = /filename=(?<filename>.*)$/g.exec(
            response.headers["content-disposition"]
          ).groups.filename;
          this.showForm = false;
          this.showLoading = false;
          this.showResult = true;
        })
        .catch(error => {
          this.showForm = true;
          this.showLoading = false;
          this.showResult = false;
          alert(error);
        });
    },
    downloadResult() {
      saveAs(this.dataFile, this.fileName);
    }
  }
};
</script>
<style lang="scss"></style>
