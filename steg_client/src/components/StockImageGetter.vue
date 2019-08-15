<template lang="pug">
    btn(v-on:click="getImage")
</template>
<script>
import axios from "axios";

export default {
    name: "StockImageGetter",
    props: ["width", "height"],
    data(){return {
        imgFile: null
    }},
    model: {prop: "imgFile", event: "change"},
    methods: {
        getImage(){
            axios.get(`https://picsum.photos/${this.width}/${this.height}`).then(response => {
                this.imgFile = new File(
                    new Blob([response.data]),
                    `img_${this.width}_${this.height}.${response.headers["content-type"].split("/")[1]}`)
            }).catch(error => {
                alert("Could not retrieve an image")
            })
        }
    }
    
}
</script>