<template>
    <div>
        <div class="menuRange">
            <div class="menuRangeButtons">
                <button @click="updateHydrometers(1)" v-bind:class="{ active: activeButton === 1 }">
                    <span>Litros / Dia</span>
                </button>
                <button @click="updateHydrometers(30)" v-bind:class="{ active: activeButton === 30 }">
                    <span>Litros / Mês</span>
                </button>
                <button @click="updateHydrometers(365)" v-bind:class="{ active: activeButton === 365 }">
                    <span>Litros / Ano</span>
                </button>
            </div>
            <div class="menuRangeInfo">
                <span>Número de resultados: {{ hydrometers?.length }}</span>
            </div>
        </div>
        <hr />
        <div class="list-hydrometers">
            <div v-for="hydrometer in hydrometers" 
                :key="hydrometer.id"
                class="item-hydrometer"
            >  
                <div class="circulo">
                    <span class="name">{{ hydrometer.name }}</span>
                    <div class="helice"></div>
                    <div class="mostrador" id="mostrador">
                        <span class="preto" id="preto">{{ String(hydrometer.last_value).slice(0, -3).split('').join('|') }}|</span>
                        <span class="vermelho" id="vermelho">{{ String(hydrometer.last_value).slice(-3).split('').join('|') }}</span>
                    </div>
                </div>
                <div class="consumo">
                    <span class="consumido">{{ hydrometer.consumed }} L</span>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from  'axios';

export default {
    data: () => ({
        hydrometers: null,
        activeButton: 0,
    }),
    async mounted() {
        this.updateHydrometers(1)
    },
    methods: {
        async updateHydrometers(days){
            this.activeButton = days;

            console.log(days)
            try{
                const res = await axios.get(`http://200.235.131.202:5000/get_hydrometers?days=${days}`);
                this.hydrometers = res.data;
            } catch (error){
                console.log(error);
            }
        }
    }
}
</script>

<style scoped>
button {
    background-color: var(--button-color);
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
}

button:hover {
    background-color: var(--action);
}

button.active {
    background-color: var(--action);
}
.list-hydrometers{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 12px;
    justify-content: space-between;
}

.item-hydrometer{
    width: 240px;
    height: 240px;
    
    display: flex;
    flex-direction: column;
    justify-content: center;

    align-items: center;
    
    background-color: #2596be; /* Cor de fundo clara */
    border-radius: 10px; /* Bordas arredondadas */
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24); /* Sombra sutil */
    transition: all 0.3s cubic-bezier(.25,.8,.25,1); /* Transição suave para o hover */
}

.item-hydrometer:hover {
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22); /* Sombra mais profunda no hover */
}
.info-item-hydrometer{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.circulo {
    width: 160px;
    height: 160px;
    border: 10px solid black;
    border-radius: 50%;
    position: relative;
    background-color: white;
}
.name {
    width: 116px;
    position: absolute;
    bottom: 65%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: var(--text-color-black);;
    font-weight: bold;
    font-size: 18px;
    text-align: center;
    line-height: 20px;
}

.helice {
    width: 20px;
    height: 20px;
    background: url("../icons/helice.png"); /* imagem da hélice */
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: girar 2s linear infinite; /* animação para girar a hélice */
}

.mostrador {
    width: 116px;
    height: 20px;
    border: 2px solid var(--text-color-black);
    position: absolute;
    padding-bottom: 2px;
    top: 60%;  /* ajuste conforme necessário */
    left: 50%;
    transform: translateX(-50%);
    font-family: Arial, sans-serif;
    font-size: 20px;
    text-align: center;
    line-height: 20px;
}

.preto {
    color: black;
}

.vermelho {
    color: red;
}

.menuRange{
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 20px;
}

.menuRangeButtons{
    display: flex;
    justify-content: center;
}

.menuRangeInfo{
    display: flex;
    justify-content: center;
}

.consumo {
    width: 100%;
    height: auto;

    text-align: center;

    /* Margem e preenchimento */
    margin-top: 10px;
    padding-top: 5px;
    padding-bottom: 5px;

    /* Outros estilos */
    background-color: #f0f0f0;
    border-radius: 5px;
}

.consumido {
    font-size: 1.2em;
    font-weight: bold;
    color: var(--text-color-black);
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