<template lang="pug">
  div(id="app")
    Navbar
    router-view
</template>
<script>
import Navbar from "@/components/Navbar.vue";
export default {
  components: { Navbar }
};
</script>
<style lang="scss">
body {
  min-height: 100vh;
  background-color: rgb(29, 29, 29);
  font-family: "Gill Sans MT", sans-serif;
  color: #eeeeee;
  background-image: url(/error_background.svg);
  background-size: cover;
}

.card {
  background: rgba(31, 31, 31, 0.8);
}

</style>
