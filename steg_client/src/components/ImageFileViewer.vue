<template lang="pug">
    img(:src="imgSrc" :alt="imgFile?imgFile.name:'No Image'")
</template>
<script>
export default {
    name: "ImageFileViewer",
    props: {
        imgFile: {
            type: File,
            required: true
        }
    },
    data() { return {
        reader: new FileReader(),
        imgSrc = ""
    }},
    watch: {
        imgFile(val){
            this.reader.readAsDataUrl(val)   
        }
    },
    created(){
        this.reader.onload = event => {
            this.imgSrc = event.target.result
        }
    }
}
</script>
