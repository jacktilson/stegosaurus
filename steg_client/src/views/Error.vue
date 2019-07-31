<template lang="pug">
    .container
        .row.mt-5
            .col-md-12.text-center
                .card
                    h1.card-header.text-uppercase oops
                    .card-body
                        h2 This page went extinct by the looks of things...
                        h2 Are you sure you meant to come here?
                        router-link.btn.my-3(to="/encode") Go Back In Time

</template>
<style lang="scss">

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
