<template>
    <div>
        <h1>teste</h1>
        {{ values }}
    </div>
</template>

<script>

export default {
    props: {
        values: {
            type: Object,
            default: () => []
        }
    }
}

</script>