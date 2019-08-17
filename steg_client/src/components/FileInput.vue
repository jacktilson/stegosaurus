<template lang="pug">
  b-form-group(
    label-for="input"
    label-class="font-weight-bold"
    :label="label"
    :description="file?'':description"
    :state="isValid"
    :invalid-feedback="invalidFeedback"
    :valid-feedback="validFeedback")
      b-form-file(
        id="input"
        ref="input"
        v-model="file"
        :placeholder="placeholder"
        :drop-placeholder="dropPlaceholder"
        :state="isValid"
        size="lg")
</template>
<script>
import path from "path";
/*
    This component is a file input with builtin validation of filesize and filetype and responsive feedback.

    It also allows custom validation. If the customValidation prop is externally set to false, it will make the input
    invalid. The invalid feedback message from this only needs to define cases for those in the custom validation prop
    and take precedence over the build in validation messages.
*/
export default {
  name: "File-Input",
  props: {
    label: {
      // The label that will be displayed above the file input
      type: String,
      default: "File Input"
    },
    description: {
      // The description that will be displayed when nothing has been input
      type: String,
      default: "Please input a file"
    },
    placeholder: {
      // The placeholder text in the file input
      type: String,
      default: "Choose a file..."
    },
    dropPlaceholder: {
      // The placeholder text in the file input for drag and drop
      type: String,
      default: "Drop a file here..."
    },
    customValidation: {
      // Optional validation in addition to the builtin
      type: Boolean,
      default: null
    },
    invalidFeedbackMessage: {
      // Feedback to handle the optional validation
      type: String,
      default: "Invalid!"
    },
    validFeedbackMessage: {
      // The message displayed on a valid feedback.
      type: String,
      default: "Awesome!"
    },
    filesizeLimit: {
      type: Number,
      default: 0, //e.g 134217728 is 128 MiB in Bytes. 0 means no limit
      validator: function(val) {
        return val >= 0;
      }
    },
    fileTypes: {
      // An array of allowed filetypes. Leave null to not apply
      type: Array,
      default: null
    },
    mimeTypes: {
      // An array of allowed mimetypes. Leave null to not apply.
      type: Array,
      default: null
    }
  },
  data() { return {
    file: null
  }},
  computed: {
    isValid() {
      // check file is uploaded
      if (!this.file) return false;
      // check custum validation
      if (this.customValidation !== null) return Boolean(this.customValidation);
      // check filetype
      var extension = path.extname(this.file.name).toLowerCase();
      if (this.fileTypes !== null && !this.fileTypes.includes(extension))
        return false;
      // check mimetype
      if (this.mimeTypes !== null && !this.mimeTypes.includes(this.file.type))
        return false;
      // check filesize limit
      if (this.filesizeLimit !== 0 && this.file.size > this.filesizeLimit)
        return false;
      return true;
    },
    validFeedback() {
      return this.isValid ? this.validFeedbackMessage : "";
    },
    invalidFeedback() {
      if (this.valid || !this.file) return "";
      // check custom validation
      if (this.customValidation !== null && !this.customValidation)
        return this.invalidFeedbackMessage;
      // check filetype
      var extension = path.extname(this.file.name).toLowerCase();
      if (this.fileTypes !== null && !this.fileTypes.includes(extension))
        return "Invalid filetype!";
      // check mimetype
      if (this.mimeTypes !== null && !this.mimeTypes.includes(this.file.type))
        return "Filetype valid but invalid data format!";
      // check filesize limit
      if (this.filesizeLimit !== 0 && this.file.size > this.filesizeLimit)
        return "Invalid filesize!";
      return "";
    }
  },
  model: {
    prop: "file",
    event: "change"
  },
  methods: {
    reset() {
      this.$refs["input"].reset();
    }
  },
  watch: {
    file(val) {
      this.$emit("change", val);
    },
    isValid(val, oldVal) {
      if (val != oldVal) {
        this.$emit("isValid", val);
      }
    }
  }
};
</script>
