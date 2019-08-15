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
          b-card.mt-3
            File-Input(
              v-model="dataFile"
              @isValid="validDataFile = $event"
              label="Data File"
              description="Enter an data file to hide your data inside"
              placeholder="Choose an data file..."
              dropPlaceholder="Drop an data file here..."
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
          b-collapse(:visible='showImgOption', id="showImg")
            b-card.mt-3
              b-row
                b-col(lg="5")
                  File-Input(
                    v-model="imgFile"
                    :isValid="validImgFile"
                    label="Image Upload"
                    description="Upload an image here to encode your data inside"
                    placeholder="Choose an image..."
                    dropPlaceholder="Drop an image here"
                    :filesizeLimit="134217728"
                    :fileTypes="['.jpg', '.png', '.bmp', '.tiff']"
                    :mimeTypes="['image/jpeg', 'image/png', 'image/bmp', 'image/tiff']")
                b-col(lg="2").my-auto.text-center
                  b-card-title or
                b-col(lg="5")
                  b-form-group(
                    label-for="useStock"
                    label="Use Stock Image"
                    label-class="font-weight-bold"
                    description="Automatically find a stock image to use instead")
                    b-btn(id="useStock").w-100 Find a stock image
</template>
<script>
import FileInput from "@/components/FileInput.vue";
export default {
  name: "Encode",
  components: { FileInput },
  data() {
    return {
      dataFile: null,
      validDataFile: false,
      encodeFilename: true,
      encodeFileExt: true,
      imgFile: null,
      validImgFile: false
    };
  },
  computed: {
    showImgOption() {
      return this.validDataFile;
    }
  }
};
</script>
