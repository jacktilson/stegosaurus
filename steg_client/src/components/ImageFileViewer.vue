<template lang="pug">
    b-img(:src="imgSrc" :alt="imgFile?imgFile.name:'No Image'")
</template>
<script>
export default {
  name: "ImageFileViewer",
  props: {
    imgFile: {
      validator: imgFile => imgFile instanceof File || imgFile === null,
      required: true
    }
  },
  data() {
    return {
      reader: new FileReader(),
      imgSrc: ""
    };
  },
  computed: {
    valid() {
      return this.imgFile && this.imgFile.type.startsWith("image");
    }
  },
  watch: {
    imgFile(val) {
      if (this.valid) this.reader.readAsDataURL(val);
      else this.imgSrc = "";
    }
  },
  created() {
    this.reader.onload = event => {
      this.imgSrc = event.target.result;
    };
  }
};
</script>
