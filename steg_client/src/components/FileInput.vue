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
            v-model="file"
            placeholder="Choose a file..."
            drop-placeholder="Drop a file here..."
            :state="validFile")
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
        file: { // Any file will be propagated here
            type: File,
            default: null,
            required: false
        },
        label: { // The label that will be displayed above the file input
            type: String,
            default: "File Input",
            required: false
        },
        description: { // The description that will be displayed when nothing has been input
            type: String,
            default: "Please input a file",
            required: false
        },
        customValidation: { // Optional validation in addition to the builtin
            type: Boolean,
            default: True,
            required: false
        },
        customInvalidFeedback: { // Feedback to handle the optional validation
            type: String,
            default: "Invalid!",
            required: false
        },
        validFeedbackMessage: { // The message displayed on a valid feedback.
            type: String,
            default: "Awesome!",
            required: false
        },
        filesizeLimit: {
            type: Number,
            default: 0, //e.g 134217728 is 128 MiB in Bytes. 0 means no limit
            required: false,
            validator: function(val){
                return val >= 0
            }
        },
        fileTypes: { // A regex matching filetypes.
            type: RegExp,
            default: /.*/g,
            required: false
        }
    },
    computed: {
        isValid(){
            var valid = true; // assume valid

            // check custum validation
            if (this.customValidation !== null){ 
                valid &= this.customValidation;
            }

            // check filetype
            var extension = path.extname(this.file.name).toLowerCase();
            if (this.fileTypes.exec(extension) === null){
                valid &= false;
            }

            // check filesize limit
            if (!(this.filesizeLimit && this.file.size < this.filesizeLimit)){
                valid &= false;
            }

            return valid
        },
        validFeedback(){
            return isValid?validFeedbackMessage:""
        },
        invalidFeedback(){
            if (!isValid){
                // check custom validation
                if (!this.customValidation){
                    return this.customInvalidFeedback
                }
                
                // check filetype
                var extension = path.extname(this.file.name);
                if (this.fileTypes.exec(extension) === null){
                    return "Invalid filetype!";
                }

                // check filesize limit
                if (!(this.filesizeLimit && this.file.size < this.filesizeLimit)){
                    return "Invalid filesize"
                }
            }
            return ""
        }
    },
    model: {
        prop: "validFile",
        event: "change"
    },
    watch: {
        file(val) {
            this.$emit("change", val);
        }
    }
};
</script>

