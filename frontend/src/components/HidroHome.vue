<template>
    <div>
        <div>
            <button @click="updateHydrometers(1)">
                <span>Dia</span>
            </button>
            <button @click="updateHydrometers(30)">
                <span>Mes</span>
            </button>
            <button @click="updateHydrometers(365)">
                <span>Ano</span>
            </button>
            <div>
                <span>Núemro de resultados: {{ hydrometers?.length }}</span>
            </div>
        </div>
        <div class="list-hydrometers">
            <div v-for="hydrometer in hydrometers" 
                :key="hydrometer.id"
                class="item-hydrometer"
            >  
                <div class="info-item-hydrometer" >
                    <!-- <span>{{ hydrometer.code }}</span> -->
                    <span>Nome: {{ hydrometer.name }}</span>
                    <span>Última Leitura: {{ hydrometer.predictions[0].value }}</span>
                </div>
                <!-- <HydrometerValues :values="hydrometer.predictions" /> -->
            </div>
        </div>
        <div>
            <div class="circulo">
                <div class="helice"></div>
                <div class="mostrador" id="mostrador">
                <!-- números pretos do mostrador -->
                <span class="preto" id="preto">00000</span>
                <!-- números vermelhos do mostrador -->
                <span class="vermelho" id="vermelho">000</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from  'axios';
import HydrometerValues from './HydrometerValues.vue'

export default {
    data: () => ({
        hydrometers: null,
    }),
    async mounted() {
        this.updateHydrometers(1)
    },
    methods: {
        async updateHydrometers(days){
            try{
                const res = await axios.get(`http://localhost:5000/get_hydrometers?days=${days}`);
                
                this.hydrometers = res.data;
            } catch (error){
                console.log(error);
            }
        }
    }
}
</script>

<style scoped>
.list-hydrometers{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 12px;
    justify-content: space-between;
}

.item-hydrometer{
    width: 200px;
    height: 100px;
    
    display: flex;
    justify-content: center;
    
    align-items: center;

    background-color: white;
    color: black;
}

.info-item-hydrometer{
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Estilo do círculo do relógio de água */
.circulo {
    width: 200px;
    height: 200px;
    border: 10px solid black;
    border-radius: 50%;
    position: relative;
    background-color: white;
}

/* Estilo da hélice do relógio de água */
.helice {
    width:80px;
    height: 80px;
    /* background: url("https://th.bing.com/th/id/OIP.1zMQXywLnvbBhR7IvF7SiwHaF4?rs=1&pid=ImgDetMain"); imagem da hélice */
    background: url("helice.png"); /* imagem da hélice */
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: girar 2s linear infinite; /* animação para girar a hélice */
}

/* Estilo do mostrador do relógio de água */
.mostrador {
    width: 100px;
    height: 50px;
    border: 2px solid black;
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    font-family: Arial, sans-serif;
    font-size: 20px;
    text-align: center;
    line-height: 50px;
}

/* Estilo dos números pretos do mostrador */
.preto {
    color: black;
}

/* Estilo dos números vermelhos do mostrador */
.vermelho {
    color: red;
}

/* Estilo da animação para girar a hélice */
@keyframes girar {
    from {
    transform: translate(-50%, -50%) rotate(0deg);
    }
    to {
    transform: translate(-50%, -50%) rotate(360deg);
    }
}
</style>