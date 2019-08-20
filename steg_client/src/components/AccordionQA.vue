<template lang="pug">
  b-card.mb-2.overflow-hidden(no-body)
    b-card-header.d-flex.cursor-pointer(v-b-toggle="answerID")
      font-awesome-icon.my-auto.icon(icon="arrow-circle-down" size="2x")
      b-card-title.my-auto.ml-3 {{title}}
    b-collapse(:id="answerID" :accordion="accordionID" :visible="visible" role="tabpanel")
      slot
        b-card-body
          b-card-text No answer given
</template>
<script>
export default {
  name: "AccordionQA",
  props: {
    title: {
      type: String,
      required: true
    },
    accordionID: {
      type: String,
      required: true
    },
    answerID: {
      type: String,
      required: true
    },
    visible: {
      type: Boolean,
      required: false,
      default: false
    }
  }
};
</script>
<style lang="scss">
.cursor-pointer {
  cursor: pointer;
}
svg {
  transition: 256ms;
  transform: rotate(0deg);
}
.collapsed > svg {
  transition: 256ms;
  transform: rotate(-90deg);
}
</style>
