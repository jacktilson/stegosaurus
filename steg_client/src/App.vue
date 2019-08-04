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
</style>
