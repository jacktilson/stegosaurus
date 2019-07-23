<template lang="pug">
  div(id="app")
    Navbar
    router-view.container.bg-info.h-100
</template>
<script>
import Navbar from "@/components/Navbar.vue";
export default {
  components: { Navbar }
};
</script>
<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 4096px;
}
</style>
