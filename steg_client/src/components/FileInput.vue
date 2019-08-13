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
*/


export default {
    name: "File-Input",
    props: {
        validFile: { // Any valid file will be propagated here
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
            default: null,
            required: false
        },
        customInvalidFeedback: { // Feedback to handle the optional validation
            type: String,
            default: "",
            required: false
        },
        customValidFeedback: { // Feedback to handle the optional validation
            type: String,
            default: "",
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
    data(){ return {
        file: null
    }},
    computed: {
        isValid(){
            var valid = true; // assume valid

            // check custum validation
            if (this.customValidation !== null){ 
                valid &= this.customValidation;
            }

            // check filetype
            var extension = path.extname(this.file.name);
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
            if (isValid){
                // check custom validation
                if (this.customValidation !== null && this.customValidation){
                    return this.customValidFeedback
                }
                return "Awesome!"
            }
            return ""
        },
        invalidFeedback(){
            if (!isValid){
                // check custom validation
                if (this.customValidation !== null && !this.customValidation){
                    return this.customValidFeedback
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
            if (this.isValid){
                this.$emit("change", val);
            }
        }
    }
};
</script>

