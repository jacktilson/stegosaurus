<template lang="pug">
b-container
  b-row
    b-col(sm="12")

      AccordionQA.mt-3(title="What is Stegosaurus?" :visible="true" accordionID="acc" answerID="qa1")
        b-row(no-gutters)
          b-col(lg="6")
            b-card-body
              Vue-Markdown.card-text.text-center(source="Stegosaurus is an image steganography tool allowing users to hide data inside a simple image file. It offers the following features:  \n- **LSB Encoding** of a file in a range of image formats (bmp, png, jpeg and others)  \n- **Encryption** using AES-128-CBC (Cipher Block Chaining) and a password of your choice  \n- Storing the **filename** and **extension** of your data in the image as well as the file contents  \n- Specifying the level of **quality/space tradeoff** in the image")
          b-col(lg="6").d-flex
            b-card-img.rounded-0.my-auto(src="@/assets/ct_logo.svg" height="192px")

      AccordionQA(title="What is steganography?" accordionID="acc" answerID="qa2")
        b-card-body
          Vue-Markdown.card-text.text-center(source="Whereas cryptography is the practice of protecting the contents of a message alone, steganography is concerned both with concealing the fact that a secret message is being sent and its contents. Media files are ideal for hiding data inside them due to their large size.  \n\nLeast Significant Bit Steganography is a technique in which we hide messages inside an image by replacing the last bit of each channel of a pixel in the image with the bits of the message to be hidden.  \n\nBy modifying least significant bits only, we can make the change nearly unnoticeable. However as more significant bits are overwritten the image will start to appear noisy, and someone might notice there is data hidden inside it.")
        .d-flex
          b-img(src="@/assets/stego_explained.svg" fluid).mx-auto

      AccordionQA(title="How was this site built?" accordionID="acc" answerID="qa3")
        b-card-body
          Vue-Markdown.card-text.text-center(source="This single page app was built using the progressive **VueJS** framework for front end development. This means that there is no server-side rendering; the entire site is downloaded once and rendered using client-side **JavaScript**. This reduces server load, and ensures no blank screens when navigating between pages on the site, giving it a snappy feel.")
          b-row
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/vue_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/javascript_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/bootstrap_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/pug_logo.svg" height="128px").mx-auto.my-4 
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/html5_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/css3_logo.svg" height="128px").mx-auto.my-4
      
      AccordionQA(title="What about the back end?" accordionID="acc" answerID="qa4")
        b-card-body
          b-card-text.text-center
            VueMarkdown The backend of the site has been coded in **Python** using the **Flask** framework and our bespoke steganography tool. It is also utilising **Amazon**'s cloud infrastructure for hosting, innovatively using it's FAAS tool **Lambda** (Functions as a servcie) for our compute heavy code.
          b-row
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/python_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/flask_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/aws_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/aws_lambda_logo.svg" height="128px").mx-auto.my-4 
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/opencv_logo.svg" height="128px").mx-auto.my-4
            b-col(cols="6" md="3").d-flex.mx-auto
              b-img(src="@/assets/nginx_logo.svg" width="128px").mx-auto.my-4

</template>
<script>
import VueMarkdown from 'vue-markdown';
import AccordionQA from "@/components/AccordionQA.vue";

export default {
  components: {VueMarkdown, AccordionQA}
}
</script>
<style scoped>
  .cursor-pointer{
    cursor: pointer
  }
</style>
