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
        b-card.mt-3
          form
            File-Input(
              v-model="dataFile"
              :isValid="validDataFile"
              label="Data File"
              description="Enter an data file to hide your data inside"
              placeholder="Choose an data file..."
              dropPlaceholder="Drop an data file here..."
              :filesizeLimit="134217728")
              //- The filesize here is equivalent to 128MiB

</template>
<script>
import FileInput from "@/components/FileInput.vue";
export default {
  name: "Encode",
  components: { FileInput },
  data() {
    return {
      dataFile: null,
      validDataFile: false
    };
  }
};
</script>
