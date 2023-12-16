<template>
    <div class="image-container">
        <img :src="image" />
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      image: null
    }
  },
  async created() {
    // chama o método updateImage quando o componente é criado
    this.updateImage();
    // chama o método updateImage a cada 1000 milissegundos (1 segundo)
    setInterval(this.updateImage, 1000);
  },
  methods: {
    async updateImage() {
      // faz a requisição da API e atualiza o valor da imagem
      const response = await axios.get('http://200.235.131.202:5000/get_last_image');
      console.log(response.data)
      this.image = 'data:image/jpeg;base64,' + response.data.image;
    }
  }
}
</script>

<style scoped>
.image-container img {
  width: 100%;
  height: auto;
}
</style>