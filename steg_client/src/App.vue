<template lang="pug">
  #app
    #background(data-origin-y="1.0")
      .layer(data-depth="0.025")
        .layer-6
      .layer(data-depth="0.05")
        .layer-5
      .layer(data-depth="0.1")
        .layer-4
      .layer(data-depth="0.15")
        .layer-3
      .layer(data-depth="0.2")
        .layer-2
      .layer(data-depth="0.25")
        .layer-1
    .content
      Navbar
      router-view
</template>
<script>
import Navbar from "@/components/Navbar.vue";
import Parallax from "parallax-js";
export default {
  components: { Navbar },
  mounted() {
    var parallax = new Parallax(document.getElementById("background"));
  }
};
</script>
<style lang="scss">
body {
  min-height: 100vh;
  background-color: #1b092d;
  font-family: "Gill Sans MT", sans-serif;
  color: #eeeeee;
}

.text-col-brand {
  color: #3f7f3f;
}

.card {
  background: rgba(31, 31, 31, 0.8);
}

.btn {
  border: 1px solid rgb(63, 127, 63);
  background-color: rgb(63, 127, 63);
  border-radius: 5px;
  padding: 14px 28px;
  font-size: 16px;
  cursor: pointer;
  &:hover {
    transition: 256ms;
    background-color: rgb(31, 95, 31);
    border-color: rgb(31, 95, 31);
  }
}

.content {
  position: absolute;
  width: 100%;
  top: 0;
  left: 0;
}

#background {
  background-color: transparent;
  overflow: hidden;
  position: fixed;
}

.layer {
  position: absolute;
  width: 100vw;
  height: 100vh;
  & div {
    background-size: cover;
    background-position: center top;
    position: relative;
    height: 110%;
    width: 110%;
    top: -5%;
    left: -5%;
  }
}
.layer-1 {
  background: url(./assets/1.svg);
}
.layer-2 {
  background: url(./assets/2.svg);
}
.layer-3 {
  background: url(./assets/3.svg);
}
.layer-4 {
  background: url(./assets/4.svg);
}
.layer-5 {
  background: url(./assets/5.svg);
}
.layer-6 {
  background: url(./assets/6.svg);
}
</style>
