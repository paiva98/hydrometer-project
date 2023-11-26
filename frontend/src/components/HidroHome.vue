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
</style>